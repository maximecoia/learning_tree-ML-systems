"""counts.py: operation counts and ratios (FLOPs, intensity, roofline).

Reuses magnitudes.py: compute_floor relies on transfer_time,
since it is the same formula, "time = quantity / rate".
"""

from magnitudes import transfer_time


def matmul_flops(m, k, n):
    """Floating-point operations of the product (m×k) · (k×n): 2·m·k·n."""
    if m < 0 or k < 0 or n < 0:
        raise ValueError("negative dimension")
    return 2 * m * k * n


def linear_flops(batch, d_in, d_out):
    """A linear layer applied to a batch: it is a matmul (batch × weights)."""
    return matmul_flops(batch, d_in, d_out)


def forward_flops(tokens, params):
    """Forward pass of a model: ~2 FLOPs per parameter per token."""
    if tokens < 0 or params < 0:
        raise ValueError("negative count")
    return 2 * tokens * params


def train_flops(tokens, params):
    """Full training step: ~6 FLOPs per parameter per token."""
    if tokens < 0 or params < 0:
        raise ValueError("negative count")
    return 6 * tokens * params


def dominant(seq_len, d_model):
    """Dominant term: attention (L²·d) or linear (L·d²), 'equal' on a tie."""
    if seq_len <= 0 or d_model <= 0:
        raise ValueError("zero sequence length or width")
    attention = seq_len * seq_len * d_model
    linear = seq_len * d_model * d_model
    if attention > linear:
        return "attention"
    if attention < linear:
        return "linear"
    return "equal"


def intensity(flops, nbytes):
    """Arithmetic intensity: operations per byte moved."""
    if flops < 0 or nbytes < 0:
        raise ValueError("negative value")
    if nbytes == 0:
        raise ValueError("no bytes moved")
    return flops / nbytes


def vector_add_intensity(bits=32):
    """Intensity of c = a + b: 1 operation for 3 elements read or written."""
    if bits <= 0:
        raise ValueError("zero or negative precision")
    return intensity(1, 3 * bits / 8)


def matmul_intensity(n, bits=32):
    """Intensity of a product (n×n)·(n×n): 2n³ ops, 3 matrices moved."""
    if n <= 0:
        raise ValueError("zero or negative dimension")
    if bits <= 0:
        raise ValueError("zero or negative precision")
    return intensity(matmul_flops(n, n, n), 3 * n * n * bits / 8)


def ridge_point(flops_per_s, bytes_per_s):
    """Ridge point of a machine: peak compute / peak memory bandwidth."""
    if flops_per_s < 0 or bytes_per_s < 0:
        raise ValueError("negative rate")
    if bytes_per_s == 0:
        raise ValueError("zero memory bandwidth")
    return flops_per_s / bytes_per_s


def compute_floor(flops, flops_per_s):
    """Minimum time (s) for these operations at peak rate."""
    return transfer_time(flops, flops_per_s)
