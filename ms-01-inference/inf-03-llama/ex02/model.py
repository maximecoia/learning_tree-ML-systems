import torch
import torch.nn as nn


class RMSNorm(nn.Module):
    def __init__(self, d_model, eps=1e-5, device=None, dtype=None):
        super().__init__()
        self.eps = eps
        if dtype is None:
            dtype = torch.float32
        self.weight = nn.Parameter(
            torch.ones(d_model, device=device, dtype=dtype)
        )

    def forward(self, x):
        input_dtype = x.dtype
        x_f = x.to(torch.float32)
        mean_square = (x_f * x_f).mean(dim=-1, keepdim=True)
        inv_rms = torch.rsqrt(mean_square + self.eps)
        weight_f = self.weight.to(device=x.device, dtype=torch.float32)
        out = x_f * inv_rms * weight_f
        return out.to(input_dtype)


class SwiGLU(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w1 = nn.Parameter(torch.randn(d_ff, d_model))
        self.w2 = nn.Parameter(torch.randn(d_model, d_ff))
        self.w3 = nn.Parameter(torch.randn(d_ff, d_model))

    def forward(self, x):
        w1 = self.w1.to(device=x.device, dtype=x.dtype)
        w2 = self.w2.to(device=x.device, dtype=x.dtype)
        w3 = self.w3.to(device=x.device, dtype=x.dtype)

        h1 = x @ w1.t()
        h3 = x @ w3.t()
        gate = h1 * torch.sigmoid(h1)
        h = gate * h3
        out = h @ w2.t()
        return out


class RotaryPositionalEmbedding(nn.Module):
    """
    Encode token positions by rotating the adjacent pairs of the
    query and key vectors by an angle that depends on the position.

    CS336 / Meta Llama convention: rotation over adjacent pairs
    (x0 with x1, x2 with x3, and so on).
    """

    def __init__(self, theta, d_k, max_seq_len, device=None):
        super().__init__()
        self.theta = theta
        self.d_k = d_k
        self.max_seq_len = max_seq_len
        # No learned parameter. cos and sin are recomputed in forward
        # rather than cached in a buffer.

    def forward(self, x, token_positions):
        # x : (..., seq_len, d_k)
        # token_positions : (..., seq_len)

        # 1. Upcast the positions to float32 for precision.
        # In bf16, large positions (e.g. 8189, 8190) become identical.
        pos = token_positions.to(torch.float32)

        # 2. Base frequency of each pair.
        # pair_indices : [0, 2, 4, ..., d_k - 2]
        pair_indices = torch.arange(0, self.d_k, 2, dtype=torch.float32, device=x.device)
        # freqs : [1.0, 1.0 / theta^(2/d_k), ...]
        freqs = 1.0 / (self.theta ** (pair_indices / self.d_k))

        # 3. Angles.
        # pos.unsqueeze(-1) turns (..., seq_len) into (..., seq_len, 1),
        # which broadcasts against freqs of shape (d_k // 2,).
        # Result: angles of shape (..., seq_len, d_k // 2).
        angles = pos.unsqueeze(-1) * freqs

        cos_angles = torch.cos(angles)
        sin_angles = torch.sin(angles)

        # 4. Split the adjacent pairs.
        # x_even takes indices 0, 2, 4...
        # x_odd takes indices 1, 3, 5...
        x_even = x[..., 0::2] # (..., seq_len, d_k // 2)
        x_odd  = x[..., 1::2] # (..., seq_len, d_k // 2)

        # 5. Upcast to float32 for the rotation (numerical safety).
        x_even = x_even.to(torch.float32)
        x_odd = x_odd.to(torch.float32)

        # 6. Apply the 2D rotation.
        out_even = x_even * cos_angles - x_odd * sin_angles
        out_odd  = x_even * sin_angles + x_odd * cos_angles

        # 7. Re-interleave the pairs.
        # torch.stack adds a last dimension: (..., seq_len, d_k // 2, 2)
        # flatten(-2) merges the last two dimensions: (..., seq_len, d_k)
        out = torch.stack([out_even, out_odd], dim=-1).flatten(-2)

        # 8. Back to the input dtype.
        return out.to(x.dtype)
