import torch
import torch.nn as nn

class MusicGenerator(nn.Module):
    def __init__(self, vocab_size, embed_dim=512, num_heads=8, num_layers=6):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        embed = self.embedding(x) * (self.embedding.embedding_dim ** 0.5)
        out = self.transformer(embed)
        logits = self.fc_out(out)
        return logits
    
