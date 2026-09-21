"""Chapter 3, my answer: attention, from one dot product to several heads.

    cd pratique/raschka && ../../.venv/bin/python3 mes-reponses/ch03.py

Three modules, each one the previous plus what the chapter adds next:
SelfAttention learns Q, K and V; CausalAttention forbids looking ahead and
drops some of the weights; MultiHeadAttention runs several attentions at once
by cutting one projection rather than by building several.

Nothing here is read from disk. The chapter's six toy embeddings are the whole
input, so this file runs anywhere and prints the shapes it claims.
"""

import torch
import torch.nn as nn

# Six tokens of three dimensions: "Your journey starts with one step".
# Shape (num_tokens, d_in) = (6, 3).
INPUTS = torch.tensor(
    [
        [0.43, 0.15, 0.89],  # Your
        [0.55, 0.87, 0.66],  # journey
        [0.57, 0.85, 0.64],  # starts
        [0.22, 0.58, 0.33],  # with
        [0.77, 0.25, 0.10],  # one
        [0.05, 0.80, 0.55],  # step
    ]
)


def simple_attention(x):
    """Attention with no learned weight, to show the mechanism alone.

    Every token is compared with every token by a dot product, the scores
    become weights that sum to one, and each context vector is the weighted
    sum of the inputs. (6, 3) in, (6, 3) out.
    """
    attn_scores = x @ x.T
    attn_weights = torch.softmax(attn_scores, dim=-1)
    return attn_weights @ x


class SelfAttention(nn.Module):
    """Scaled dot-product attention with learned Q, K and V.

    The three projections answer two different questions: Q against K decides
    where to look, V decides what is read from there. Dividing by the square
    root of d_k keeps the dot products from growing with the dimension and
    saturating the softmax.
    """

    def __init__(self, d_in, d_out, qkv_bias=False):
        super().__init__()
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)

    def forward(self, x):
        queries = self.W_query(x)
        keys = self.W_key(x)
        values = self.W_value(x)

        # (T, d_out) @ (d_out, T) -> (T, T)
        attn_scores = queries @ keys.T
        d_k = keys.shape[-1]
        attn_weights = torch.softmax(attn_scores / d_k**0.5, dim=-1)

        # (T, T) @ (T, d_out) -> (T, d_out)
        context_vec = attn_weights @ values
        return context_vec


class CausalAttention(nn.Module):
    """One usable head: batched, forbidden to look ahead, with dropout.

    The mask is a buffer and not a parameter: it belongs to the module and
    follows it onto a GPU, but it never learns. Writing -inf rather than zero
    is what makes the future weigh exactly nothing, since softmax exponentiates
    and exp(-inf) is 0.
    """

    def __init__(self, d_in, d_out, context_length, dropout, qkv_bias=False):
        super().__init__()
        self.d_out = d_out
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.dropout = nn.Dropout(dropout)
        mask = torch.triu(
            torch.ones(context_length, context_length), diagonal=1
        )
        self.register_buffer("mask", mask)

    def forward(self, x):
        b, num_tokens, d_in = x.shape

        queries = self.W_query(x)
        keys = self.W_key(x)
        values = self.W_value(x)

        # (b, T, d_out) @ (b, d_out, T) -> (b, T, T)
        attn_scores = queries @ keys.transpose(1, 2)

        # The buffer is cut to the batch's own length: it was built for
        # context_length, which may be larger than the tokens actually given.
        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]
        attn_scores.masked_fill_(mask_bool, -torch.inf)

        d_k = keys.shape[-1]
        attn_weights = torch.softmax(attn_scores / d_k**0.5, dim=-1)
        attn_weights = self.dropout(attn_weights)

        # (b, T, T) @ (b, T, d_out) -> (b, T, d_out)
        context_vec = attn_weights @ values
        return context_vec


class MultiHeadAttention(nn.Module):
    """Several heads at once, by cutting one projection instead of stacking.

    d_out is split into num_heads slices of head_dim, and the head axis is
    moved in front of the token axis so every head's attention is computed in
    the same matrix product. Each head therefore scales by sqrt(head_dim), not
    by sqrt(d_out).
    """

    def __init__(
        self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False
    ):
        super().__init__()
        assert d_out % num_heads == 0, "d_out must be divisible by num_heads"

        self.d_out = d_out
        self.num_heads = num_heads
        self.head_dim = d_out // num_heads

        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.out_proj = nn.Linear(d_out, d_out)
        self.dropout = nn.Dropout(dropout)
        mask = torch.triu(
            torch.ones(context_length, context_length), diagonal=1
        )
        self.register_buffer("mask", mask)

    def forward(self, x):
        b, num_tokens, d_in = x.shape

        queries = self.W_query(x)
        keys = self.W_key(x)
        values = self.W_value(x)

        # (b, T, d_out) -> (b, T, heads, head_dim). view only re-reads the
        # numbers already there; d_out is cut, nothing is computed.
        queries = queries.view(b, num_tokens, self.num_heads, self.head_dim)
        keys = keys.view(b, num_tokens, self.num_heads, self.head_dim)
        values = values.view(b, num_tokens, self.num_heads, self.head_dim)

        # (b, T, heads, head_dim) -> (b, heads, T, head_dim), so that every
        # head's attention falls out of a single matrix product.
        queries = queries.transpose(1, 2)
        keys = keys.transpose(1, 2)
        values = values.transpose(1, 2)

        # (b, heads, T, head_dim) @ (b, heads, head_dim, T) -> (b, heads, T, T)
        attn_scores = queries @ keys.transpose(2, 3)

        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]
        attn_scores.masked_fill_(mask_bool, -torch.inf)

        attn_weights = torch.softmax(
            attn_scores / keys.shape[-1] ** 0.5, dim=-1
        )
        attn_weights = self.dropout(attn_weights)

        # (b, heads, T, T) @ (b, heads, T, head_dim) -> (b, heads, T, head_dim)
        context_vec = attn_weights @ values

        # Back to (b, T, d_out). transpose only changes how the tensor is
        # read, so contiguous is what makes view legal here.
        context_vec = context_vec.transpose(1, 2)
        context_vec = context_vec.contiguous().view(b, num_tokens, self.d_out)

        context_vec = self.out_proj(context_vec)
        return context_vec


if __name__ == "__main__":
    torch.manual_seed(123)

    print("simple attention      ", simple_attention(INPUTS).shape)

    sa = SelfAttention(d_in=3, d_out=2)
    print("trainable self-attention", sa(INPUTS).shape)

    # (6, 3) stacked twice -> (2, 6, 3): a batch of two identical sequences.
    batch = torch.stack((INPUTS, INPUTS), dim=0)
    print("batch                 ", batch.shape)

    ca = CausalAttention(d_in=3, d_out=2, context_length=6, dropout=0.0)
    print("causal attention      ", ca(batch).shape)

    mha = MultiHeadAttention(
        d_in=3, d_out=4, context_length=6, dropout=0.0, num_heads=2
    )
    print("multi-head attention  ", mha(batch).shape)
