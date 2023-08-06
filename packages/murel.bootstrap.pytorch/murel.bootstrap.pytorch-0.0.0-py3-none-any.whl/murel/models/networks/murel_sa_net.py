from copy import deepcopy
import itertools
import os
import numpy as np
import scipy
import torch
import torch.nn as nn
import torch.nn.functional as F
from bootstrap.lib.options import Options
from bootstrap.lib.logger import Logger
import block
from block.models.networks.vqa_net import factory_text_enc
from block.models.networks.vqa_net import mask_softmax
from block.models.networks.mlp import MLP
from .murel_cell import MuRelCell

class MuRelSelfAttNet(nn.Module):

    def __init__(self,
            txt_enc={},
            self_q_att=False,
            n_step=3,
            shared=False,
            cell={},
            agg={},
            classif={},
            wid_to_word={},
            word_to_wid={},
            aid_to_ans=[],
            ans_to_aid={}):
        super(MuRelSelfAttNet, self).__init__()
        self.self_q_att = self_q_att
        self.n_step = n_step
        self.shared = shared
        self.cell = cell
        self.agg = agg
        assert self.agg['type'] in ['max', 'mean']
        self.classif = classif
        self.wid_to_word = wid_to_word
        self.word_to_wid = word_to_wid
        self.aid_to_ans = aid_to_ans
        self.ans_to_aid = ans_to_aid
        # Modules
        self.txt_enc = factory_text_enc(self.wid_to_word, txt_enc)

        self.self_q_att_module = block.factory_fusion(self.self_q_att['fusion'])

        if self.shared:
            self.cell = MuRelCell(**cell)
        else:
            self.cells = nn.ModuleList([MuRelCell(**cell) for i in range(self.n_step)])

        # self.n_params = sum(p.numel() for p in self.fusion_modules.parameters() \
        #                     if p.requires_grad)

        if 'fusion' in self.classif:
            self.classif_module = block.factory_fusion(self.classif['fusion'])
        elif 'mlp' in self.classif:
            self.classif_module = MLP(self.classif['mlp'])
        else:
            raise ValueError(self.classif.keys())

        #Logger().log_value('nparams', self.n_params, should_print=True)
        #Logger().log_value('all_params', sum(p.numel() for p in self.parameters() if p.requires_grad), should_print=True)

        self.buffer = None
        #self.entropies = {}

    def set_buffer(self):
        self.buffer = {}
        if self.shared:
            self.cell.pairwise.set_buffer()
        else:
            for i in range(self.n_step):
                self.cell[i].pairwise.set_buffer()

    def forward(self, batch):
        v = batch['visual']
        q = batch['question']
        l = batch['lengths']
        c = batch['norm_coord']
        # l contains the number of words for each question
        # in case of multi-gpus it must be a Tensor
        # thus we convert it into a list during the forward pass
        l = list(l.data[:,0])
        q, q_words = self.process_question(q, l)

        # cell
        mm = v
        for i in range(self.n_step):
            q = self.process_self_q_att(q, q_words, l)

            cell = self.cell if self.shared else self.cells[i]
            mm = cell(q, mm, c)

            if self.buffer is not None: # for visualization
                self.buffer[i] = deepcopy(cell.pairwise.buffer)

        if self.agg['type'] == 'max':
            mm = torch.max(mm, 1)[0]
        elif self.agg['type'] == 'mean':
            mm = mm.mean(1)

        if 'fusion' in self.classif:
            logits = self.classif_module([q, mm])
        elif 'mlp' in self.classif:
            logits = self.classif_module(mm)

        out = {'logits': logits}
        return out

    def process_self_q_att(self, q, q_words, l):
        bsize = q_words.shape[0]
        n_regions = q_words.shape[1]
        q = q[:,None,:].expand(bsize, n_regions, q.shape[1])
        q = q.contiguous().view(bsize*n_regions, -1)
        q_w_r = q_words.contiguous().view(bsize*n_regions, -1)
        scorer = self.self_q_att_module([q, q_w_r])
        scorer = scorer.view(bsize, n_regions, -1)
        weights = (scorer * q_words).sum(2)
        weights = mask_softmax(weights[:,:,None], l)
        q = q_words * weights
        q = q.sum(1)
        return q

    def process_question(self, q, l):
        q_emb = self.txt_enc.embedding(q)
        q_mask = (q!=0).view(-1,q.size(1), 1).expand_as(q_emb)
        q_mask = q_mask.float()
        q_emb = q_emb*q_mask

        q_words, _ = self.txt_enc.rnn(q_emb)

        # if self.self_q_att:
        #     q_att = self.q_att_linear0(q)
        #     q_att = F.relu(q_att)
        #     q_att = self.q_att_linear1(q_att)
        #     q_att = mask_softmax(q_att, l)
        #     #self.q_att_coeffs = q_att
        #     if q_att.size(2) > 1:
        #         q_atts = torch.unbind(q_att, dim=2)
        #         q_outs = []
        #         for q_att in q_atts:
        #             q_att = q_att.unsqueeze(2)
        #             q_att = q_att.expand_as(q)
        #             q_out = q_att*q
        #             q_out = q_out.sum(1)
        #             q_outs.append(q_out)
        #         q = torch.cat(q_outs, dim=1)
        #     else:
        #         q_att = q_att.expand_as(q)
        #         q = q_att * q
        #         q = q.sum(1)
        # else:
        q = self.txt_enc._select_last(q_words, l)

        return q, q_words

    def process_answers(self, out):
        batch_size = out['logits'].shape[0]
        _, pred = out['logits'].data.max(1)
        pred.squeeze_()
        out['answers'] = [self.aid_to_ans[pred[i]] for i in range(batch_size)]
        out['answer_ids'] = [pred[i] for i in range(batch_size)]
        return out
