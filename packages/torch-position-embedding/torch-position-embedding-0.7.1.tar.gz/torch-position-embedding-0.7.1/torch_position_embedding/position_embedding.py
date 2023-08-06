import torch
import torch.nn as nn
import torch.nn.functional as F


__all__ = ['PositionEmbedding', 'TrigonometricPositionEmbedding']


class PositionEmbedding(nn.Module):

    MODE_EXPAND = 'MODE_EXPAND'
    MODE_ADD = 'MODE_ADD'
    MODE_CONCAT = 'MODE_CONCAT'

    def __init__(self,
                 num_embeddings,
                 embedding_dim,
                 mode=MODE_ADD):
        super(PositionEmbedding, self).__init__()
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self.mode = mode
        if self.mode == self.MODE_EXPAND:
            self.weight = nn.Parameter(torch.Tensor(num_embeddings * 2 + 1, embedding_dim))
        else:
            self.weight = nn.Parameter(torch.Tensor(num_embeddings, embedding_dim))
        self.reset_parameters()

    def reset_parameters(self):
        torch.nn.init.xavier_normal_(self.weight)

    def forward(self, x):
        if self.mode == self.MODE_EXPAND:
            indices = torch.clamp(x, -self.num_embeddings, self.num_embeddings) + self.num_embeddings
            return F.embedding(indices.type(torch.LongTensor), self.weight)
        batch_size, seq_len = x.size()[:2]
        embeddings = self.weight[:seq_len, :].view(1, seq_len, self.embedding_dim)
        if self.mode == self.MODE_ADD:
            return x + embeddings
        if self.mode == self.MODE_CONCAT:
            return torch.cat((x, embeddings.repeat(batch_size, 1, 1)), dim=-1)
        raise NotImplementedError('Unknown mode: %s' % self.mode)

    def extra_repr(self):
        return 'num_embeddings={}, embedding_dim={}, mode={}'.format(
            self.num_embeddings, self.embedding_dim, self.mode,
        )


class TrigonometricPositionEmbedding(nn.Module):
    """Position embedding use sine and cosine functions.

        See: https://arxiv.org/pdf/1706.03762
    """

    MODE_EXPAND = 'MODE_EXPAND'
    MODE_ADD = 'MODE_ADD'
    MODE_CONCAT = 'MODE_CONCAT'

    def __init__(self,
                 embedding_dim,
                 mode=MODE_ADD):
        super(TrigonometricPositionEmbedding, self).__init__()
        self.embedding_dim = embedding_dim
        self.mode = mode

    def forward(self, x):
        batch_size, seq_len = x.size()[:2]
        if self.mode == self.MODE_EXPAND:
            pos_x = x.type(torch.FloatTensor).view(batch_size, seq_len, 1)
        else:
            pos_x = torch.arange(seq_len).view(1, seq_len, 1).type(torch.FloatTensor)
        half = (torch.arange(self.embedding_dim // 2) * 2).type(torch.FloatTensor)
        powers = 1.0 / torch.pow(10000.0, half / self.embedding_dim).view(1, self.embedding_dim // 2)
        even_embed = torch.sin(pos_x.matmul(powers))
        odd_embed = torch.cos(pos_x.matmul(powers))
        embed = torch.stack((even_embed, odd_embed), dim=-1).view(-1, seq_len, self.embedding_dim)
        if self.mode == self.MODE_EXPAND:
            return embed
        embed = embed.repeat(batch_size, 1, 1)
        if self.mode == self.MODE_ADD:
            return x + embed
        if self.mode == self.MODE_CONCAT:
            return torch.cat((x, embed), dim=-1)
        raise NotImplementedError('Unknown mode: %s' % self.mode)

    def extra_repr(self):
        return 'embedding_dim={}, mode={}'.format(
            self.embedding_dim, self.mode,
        )
