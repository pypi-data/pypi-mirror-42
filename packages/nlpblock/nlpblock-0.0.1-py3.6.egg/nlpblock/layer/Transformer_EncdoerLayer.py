import torch
import torch.nn as nn
import nlpblock as nb

class SelfEncdoerLayer(nn.Module):
    def __init__(self, n_enc_vocab):
        super(SelfEncdoerLayer, self).__init__()

        self.n_enc_vocab = n_enc_vocab
        self.
        self.enc_emb = nn.Embedding(src_vocab_size, d_model)
        self.pos_emb = nn.Embedding.from_pretrained(get_sinusoid_encoding_table(src_len + 1, d_model), freeze=True)


    def forward(self, *input):
        return 1
