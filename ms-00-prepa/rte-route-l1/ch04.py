"""Chapter 4, my answer: the blocks of chapters 2 and 3 become a whole GPT.

    cd pratique/raschka && ../../.venv/bin/python3 mes-reponses/ch04.py

LayerNorm, GELU and FeedForward are the three pieces this chapter adds; the
TransformerBlock wires them around the attention of chapter 3 with two
residual connections, and GPTModel stacks twelve of those between the
embeddings and a projection onto the vocabulary. The weights are random: this
model is built, not trained.
"""

import tiktoken
import torch
import torch.nn as nn

# Built in chapter 3, and left there: this file adds what surrounds it.
from ch03 import MultiHeadAttention

GPT_CONFIG_124M = {
    "vocab_size": 50257,  # GPT-2's token count
    "context_length": 1024,  # longest input the position table can index
    "emb_dim": 768,  # numbers describing one token
    "n_heads": 12,  # attention heads, so head_dim = 768 // 12 = 64
    "n_layers": 12,  # TransformerBlocks stacked one on the next
    "drop_rate": 0.1,  # dropout, during training only
    "qkv_bias": False,  # Q/K/V projections carry no bias here
}


class LayerNorm(nn.Module):
    """Normalise each token's own features, then let the network rescale them.

    `dim=-1` is the whole point: the mean and variance are taken across the
    768 features of one token, never across the batch or across tokens, so
    nothing a token learns depends on its neighbours in the batch.
    """

    def __init__(self, emb_dim):
        super().__init__()
        self.eps = 1e-5
        self.scale = nn.Parameter(torch.ones(emb_dim))
        self.shift = nn.Parameter(torch.zeros(emb_dim))

    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)

        # `unbiased=False` divides by n rather than by n - 1.
        var = x.var(dim=-1, keepdim=True, unbiased=False)

        # Dividing by sqrt(var + eps) rather than sqrt(var) is what keeps the
        # result finite when a token's features are all equal. It also makes
        # the output variance slightly below 1, by var / (var + eps).
        norm_x = (x - mean) / torch.sqrt(var + self.eps)

        return self.scale * norm_x + self.shift


class GELU(nn.Module):
    """The FeedForward network's non-linearity, in its tanh approximation.

    Without one, stacking linear layers would collapse into a single linear
    layer. GELU is preferred to ReLU here because it bends instead of folding:
    slightly negative values are damped, not erased, and it stays
    differentiable everywhere.
    """

    def __init__(self):
        super().__init__()

    def forward(self, x):
        return (
            0.5
            * x
            * (
                1
                + torch.tanh(
                    torch.sqrt(torch.tensor(2.0 / torch.pi, device=x.device))
                    * (x + 0.044715 * torch.pow(x, 3))
                )
            )
        )


class FeedForward(nn.Module):
    """Widen to four times the width, bend, come back.

    The return to `emb_dim` is not decoration: the block adds this output to
    its own input, and two tensors only add when their shapes agree.
    """

    def __init__(self, cfg):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(cfg["emb_dim"], 4 * cfg["emb_dim"]),
            GELU(),
            nn.Linear(4 * cfg["emb_dim"], cfg["emb_dim"]),
        )

    def forward(self, x):
        return self.layers(x)


class TransformerBlock(nn.Module):
    """The unit GPT repeats, and almost all of what the chapter builds.

        x = x + Attention(LayerNorm(x))
        x = x + FeedForward(LayerNorm(x))

    Attention lets tokens read each other; FeedForward reworks each token on
    its own. Normalising before each sub-layer rather than after it is the
    Pre-LayerNorm arrangement.
    """

    def __init__(self, cfg):
        super().__init__()
        self.att = MultiHeadAttention(
            d_in=cfg["emb_dim"],
            d_out=cfg["emb_dim"],
            context_length=cfg["context_length"],
            num_heads=cfg["n_heads"],
            dropout=cfg["drop_rate"],
            qkv_bias=cfg["qkv_bias"],
        )
        self.ff = FeedForward(cfg)
        self.norm1 = LayerNorm(cfg["emb_dim"])
        self.norm2 = LayerNorm(cfg["emb_dim"])
        self.drop_shortcut = nn.Dropout(cfg["drop_rate"])

    def forward(self, x):
        # The tokens talk to each other. The causal mask lives inside
        # MultiHeadAttention, so nothing here has to forbid the future.
        shortcut = x
        x = self.norm1(x)
        x = self.att(x)
        x = self.drop_shortcut(x)
        x = x + shortcut

        # Then each token is reworked alone.
        shortcut = x
        x = self.norm2(x)
        x = self.ff(x)
        x = self.drop_shortcut(x)
        x = x + shortcut

        return x


class GPTModel(nn.Module):
    """Embeddings, twelve blocks, one last norm, one projection.

    Every position gets a score for every token of the vocabulary, not just
    the last one: that is what lets training learn many next-token relations
    in a single forward pass.
    """

    def __init__(self, cfg):
        super().__init__()
        self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
        self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
        self.drop_emb = nn.Dropout(cfg["drop_rate"])

        # Each block holds its own weights; this is not one block read twelve
        # times. The star hands nn.Sequential twelve arguments, not one list.
        self.trf_blocks = nn.Sequential(
            *[TransformerBlock(cfg) for _ in range(cfg["n_layers"])]
        )

        self.final_norm = LayerNorm(cfg["emb_dim"])
        self.out_head = nn.Linear(
            cfg["emb_dim"], cfg["vocab_size"], bias=False
        )

    def forward(self, in_idx):
        batch_size, seq_len = in_idx.shape

        # [B, T] -> [B, T, C]
        tok_embeds = self.tok_emb(in_idx)

        # `device=in_idx.device`: the positions are born where the data lives.
        positions = torch.arange(seq_len, device=in_idx.device)

        # [T] -> [T, C], added to [B, T, C] by broadcasting.
        pos_embeds = self.pos_emb(positions)

        x = tok_embeds + pos_embeds
        x = self.drop_emb(x)
        x = self.trf_blocks(x)
        x = self.final_norm(x)

        # [B, T, C] -> [B, T, vocab_size]. No softmax: the loss of chapter 5
        # reads raw logits.
        logits = self.out_head(x)

        return logits


def generate_text_simple(model, idx, max_new_tokens, context_size):
    """Greedy autoregressive generation, one token per pass.

    Generation cannot be parallel the way training is: the next token does not
    exist yet, so it has to be produced, appended, and fed back in.
    """
    for _ in range(max_new_tokens):
        # The model can only index positions below context_size.
        idx_cond = idx[:, -context_size:]

        with torch.no_grad():
            logits = model(idx_cond)

        # Of the T predictions the model just made, generation wants one.
        logits = logits[:, -1, :]

        # No softmax needed: it preserves order, so the argmax is the same.
        idx_next = torch.argmax(logits, dim=-1, keepdim=True)

        idx = torch.cat((idx, idx_next), dim=1)

    return idx


if __name__ == "__main__":
    torch.manual_seed(123)

    model = GPTModel(GPT_CONFIG_124M)

    # eval() silences dropout; no_grad(), used inside generate, stops the
    # graph from being built. They are two different things.
    model.eval()

    total = sum(p.numel() for p in model.parameters())
    partages = total - sum(p.numel() for p in model.out_head.parameters())
    print(f"parameters                {total:,}")
    print(f"if out_head were tied     {partages:,}")
    print(f"weights in float32        {total * 4 / 1024 ** 2:.0f} MiB")

    tokenizer = tiktoken.get_encoding("gpt2")
    start_context = "Hello, I am"

    encoded = tokenizer.encode(start_context)
    print("\nencoded                  ", encoded)

    # unsqueeze(0) adds the batch axis the model expects.
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)
    print("encoded tensor shape      ", tuple(encoded_tensor.shape))

    out = generate_text_simple(
        model=model,
        idx=encoded_tensor,
        max_new_tokens=6,
        context_size=GPT_CONFIG_124M["context_length"],
    )

    print("generated token IDs       ", out.squeeze(0).tolist())
    print(
        "generated text            ", tokenizer.decode(out.squeeze(0).tolist())
    )
