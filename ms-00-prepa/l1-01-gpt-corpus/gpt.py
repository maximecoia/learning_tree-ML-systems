"""A causal character-level GPT, with attention written by hand.

    from gpt import GPT, BLOCK_SIZE

The model only. Training is train.py, evaluation evaluate.py, sampling
generate.py, and verifier.py holds the seven checks it passes. No
nn.Transformer and no nn.MultiheadAttention: every head is the three
projections, the scaled scores, the causal mask and the softmax below.

The path of one batch, shape by shape. B sequences, T tokens, width C,
vocabulary V, 4 heads of width C / 4:

    idx                      (B, T)        integers in [0, V)
    token + position         (B, T, C)     two lookups, added
    3 blocks, pre-norm:
      attention, + x         (B, T, C)     scores (B, T, T), masked above the diagonal
      feed-forward, + x      (B, T, C)     through (B, T, 4C)
    final LayerNorm          (B, T, C)
    lm_head                  (B, T, V)     the logits

Written against torch 2.14.0 / Python 3.12.
"""
import torch
import torch.nn as nn
from torch.nn import functional as F

# --- hyperparameters --------------------------------------------------------
# Module-level constants: GPT(vocab_size) takes no other argument.
BLOCK_SIZE = 32          # T, the context length and the rows of the position table
N_EMB = 64               # C, the width of the residual stream
N_HEAD = 4               # head width 64 // 4 = 16
N_LAYER = 3
DROPOUT = 0.0            # must stay 0 for check 3, which runs the model twice in train mode
SEED = 1337


# --- one attention head -----------------------------------------------------
class Head(nn.Module):
    """Self-attention, one head. x (B, T, C) -> (B, T, head_size)."""

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(N_EMB, head_size, bias=False)
        self.query = nn.Linear(N_EMB, head_size, bias=False)
        self.value = nn.Linear(N_EMB, head_size, bias=False)
        # 1 where position i may read position j (j <= i), 0 above the diagonal.
        self.register_buffer('tril', torch.tril(torch.ones(BLOCK_SIZE, BLOCK_SIZE)))
        self.dropout = nn.Dropout(DROPOUT)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)                                       # (B, T, hs)
        q = self.query(x)                                     # (B, T, hs)
        v = self.value(x)                                     # (B, T, hs)
        wei = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5   # (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1)                          # each row sums to 1
        wei = self.dropout(wei)
        return wei @ v                                        # (B, T, hs)


# --- several heads, then the projection back into the residual stream -------
class MultiHeadAttention(nn.Module):
    """n heads in parallel, concatenated, projected. (B, T, C) -> (B, T, C)."""

    def __init__(self, n_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(n_heads)])
        self.proj = nn.Linear(n_heads * head_size, N_EMB)
        self.dropout = nn.Dropout(DROPOUT)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)  # (B, T, C)
        return self.dropout(self.proj(out))


# --- the position-wise feed-forward -----------------------------------------
class FeedForward(nn.Module):
    """(B, T, C) -> (B, T, C), the same small network at every position."""

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.GELU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(DROPOUT),
        )

    def forward(self, x):
        return self.net(x)


# --- communication, then computation ----------------------------------------
class Block(nn.Module):
    """One transformer block, pre-norm. (B, T, C) -> (B, T, C)."""

    def __init__(self, n_embd, n_heads):
        super().__init__()
        assert n_embd % n_heads == 0, "n_embd must be divisible by n_heads"
        self.sa = MultiHeadAttention(n_heads, n_embd // n_heads)
        self.ffwd = FeedForward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        # Each sublayer reads a normalized copy and adds its result to the raw x.
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


# --- the model --------------------------------------------------------------
class GPT(nn.Module):
    """Token ids in, next-token logits out. (B, T) -> (B, T, vocab_size)."""

    def __init__(self, vocab_size):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, N_EMB)
        self.position_embedding = nn.Embedding(BLOCK_SIZE, N_EMB)
        self.blocks = nn.Sequential(*[Block(N_EMB, N_HEAD) for _ in range(N_LAYER)])
        self.ln_f = nn.LayerNorm(N_EMB)
        self.lm_head = nn.Linear(N_EMB, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok = self.token_embedding(idx)                                    # (B, T, C)
        pos = self.position_embedding(torch.arange(T, device=idx.device))  # (T, C)
        x = tok + pos
        x = self.blocks(x)
        logits = self.lm_head(self.ln_f(x))                                # (B, T, V)
        if targets is None:
            return logits, None
        loss = F.cross_entropy(logits.reshape(B * T, -1), targets.reshape(B * T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -BLOCK_SIZE:]                    # crop the input, never the output
            logits, _ = self(idx_cond)
            probs = F.softmax(logits[:, -1, :], dim=1)         # (B, V): the last position only
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
