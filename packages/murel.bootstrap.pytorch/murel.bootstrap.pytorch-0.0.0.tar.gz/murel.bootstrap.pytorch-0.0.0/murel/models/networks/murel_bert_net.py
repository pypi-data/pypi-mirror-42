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
from pytorch_pretrained_bert import BertModel
from .murel_cell import MuRelCell

class MuRelBertNet(nn.Module):

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
        super(MuRelBertNet, self).__init__()
        self.txt_enc = txt_enc
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
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.bert.embeddings.sparse = False
        if self.self_q_att:
            self.q_att_linear0 = nn.Linear(768, 512)
            self.q_att_linear1 = nn.Linear(512, 2)

        if self.txt_enc.get('nograd_emb', False):
            Logger()('No gradient in bert.embeddings')
            for p in self.bert.embeddings.parameters():
                p.requires_grad = False

        if self.txt_enc.get('nograd_enc', False):
            Logger()('No gradient in bert.encoder')
            for p in self.bert.encoder.parameters():
                p.requires_grad = False

        if self.txt_enc.get('nograd_pool', False):
            Logger()('No gradient in bert.pooler')
            for p in self.bert.pooler.parameters():
                p.requires_grad = False

        #self.self_q_att_module = block.factory_fusion(self.self_q_att['fusion'])

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

        Logger().log_value('nparams',
            sum(p.numel() for p in self.parameters() if p.requires_grad),
            should_print=True)

        Logger().log_value('nparams_txt_enc',
            self.get_nparams_txt_enc(),
            should_print=True)

        self.buffer = None
        #self.entropies = {}

    def get_nparams_txt_enc(self):
        params = [p.numel() for p in self.bert.parameters() if p.requires_grad]
        if self.self_q_att:
            params += [p.numel() for p in self.q_att_linear0.parameters() if p.requires_grad]
            params += [p.numel() for p in self.q_att_linear1.parameters() if p.requires_grad]
        return sum(params)

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
        q = self.process_question(q, l)

        # cell
        mm = v
        for i in range(self.n_step):
            #q = self.process_self_q_att(q, q_words, l)

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
        bsize = q.shape[0]
        attention_mask = torch.ones_like(q, device=q.device)

        for i in range(bsize):
            attention_mask.data[i][l[i].item():].fill_(0)

        encoded_layers, pooled_output = self.forward_bert(
            q, attention_mask=attention_mask)

        if self.self_q_att:
            q = encoded_layers[-1]
            q_att = self.q_att_linear0(q)
            q_att = F.relu(q_att)
            q_att = self.q_att_linear1(q_att)
            q_att = mask_softmax(q_att, l)
            #self.q_att_coeffs = q_att
            if q_att.size(2) > 1:
                q_atts = torch.unbind(q_att, dim=2)
                q_outs = []
                for q_att in q_atts:
                    q_att = q_att.unsqueeze(2)
                    q_att = q_att.expand_as(q)
                    q_out = q_att*q
                    q_out = q_out.sum(1)
                    q_outs.append(q_out)
                q = torch.cat(q_outs, dim=1)
            else:
                q_att = q_att.expand_as(q)
                q = q_att * q
                q = q.sum(1)
        else:
            q = pooled_output

        return q

    def forward_bert(self, input_ids, token_type_ids=None, attention_mask=None, output_all_encoded_layers=True):
        if attention_mask is None:
            attention_mask = torch.ones_like(input_ids)
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        # We create a 3D attention mask from a 2D tensor mask.
        # Sizes are [batch_size, 1, 1, to_seq_length]
        # So we can broadcast to [batch_size, num_heads, from_seq_length, to_seq_length]
        # this attention mask is more simple than the triangular masking of causal attention
        # used in OpenAI GPT, we just need to prepare the broadcast dimension here.
        extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)

        # Since attention_mask is 1.0 for positions we want to attend and 0.0 for
        # masked positions, this operation will create a tensor which is 0.0 for
        # positions we want to attend and -10000.0 for masked positions.
        # Since we are adding it to the raw scores before the softmax, this is
        # effectively the same as removing these entirely.
        extended_attention_mask = extended_attention_mask.to(dtype=next(self.bert.parameters()).dtype) # fp16 compatibility
        extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0

        if self.txt_enc.get('nograd_emb', False): torch.set_grad_enabled(False)
        embedding_output = self.bert.embeddings(input_ids, token_type_ids)
        if self.txt_enc.get('nograd_emb', False): torch.set_grad_enabled(True)

        if self.txt_enc.get('nograd_enc', False): torch.set_grad_enabled(False)
        encoded_layers = self.bert.encoder(embedding_output,
                                      extended_attention_mask,
                                      output_all_encoded_layers=output_all_encoded_layers)
        if self.txt_enc.get('nograd_enc', False): torch.set_grad_enabled(True)

        sequence_output = encoded_layers[-1]

        if self.txt_enc.get('nopool_emb', False): torch.set_grad_enabled(False)
        pooled_output = self.bert.pooler(sequence_output)
        if self.txt_enc.get('nopool_emb', False): torch.set_grad_enabled(True)

        if not output_all_encoded_layers:
            encoded_layers = encoded_layers[-1]
        return encoded_layers, pooled_output

    def process_answers(self, out):
        batch_size = out['logits'].shape[0]
        _, pred = out['logits'].data.max(1)
        pred.squeeze_()
        out['answers'] = [self.aid_to_ans[pred[i]] for i in range(batch_size)]
        out['answer_ids'] = [pred[i] for i in range(batch_size)]
        return out
