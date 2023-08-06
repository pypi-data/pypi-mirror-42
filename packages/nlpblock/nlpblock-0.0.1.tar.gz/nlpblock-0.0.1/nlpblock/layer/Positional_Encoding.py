import torch.nn as nn

class Positional_Encoding(nn.Module):
    def __init__(self, d_model, d_k, d_v, n_heads):
        super(Positional_Encoding, self).__init__()

    def forward(self, input):
        return 1