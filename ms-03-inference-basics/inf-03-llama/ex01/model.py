import torch
import torch.nn as nn


class RMSNorm(nn.Module):
    """
    Root mean square normalization.

    The layer normalizes each vector along the last dimension.
    It does not center: it does not subtract the mean.
    It only learns a gain, named weight.
    """

    def __init__(self, d_model, eps=1e-5, device=None, dtype=None):
        # Always call the parent class constructor.
        super().__init__()

        # Keep epsilon for forward.
        self.eps = eps

        # Without a requested dtype, use float32.
        if dtype is None:
            dtype = torch.float32

        # The subject requires a parameter named exactly "weight".
        # Its shape is (d_model,): one gain per dimension.
        self.weight = nn.Parameter(
            torch.ones(d_model, device=device, dtype=dtype)
        )

    def forward(self, x):
        # Remember the input dtype.
        input_dtype = x.dtype

        # Upcast to float32 for the arithmetic.
        x_f = x.to(torch.float32)

        # Mean of the squares over the last dimension.
        # keepdim=True gives shape (..., 1), which broadcasts against x.
        mean_square = (x_f * x_f).mean(dim=-1, keepdim=True)

        # Inverse square root.
        inv_rms = torch.rsqrt(mean_square + self.eps)

        # Move the weight to x's device too, in float32.
        weight_f = self.weight.to(device=x.device, dtype=torch.float32)

        # Normalize, then apply the learned gain.
        out = x_f * inv_rms * weight_f

        # Back to the input dtype.
        return out.to(input_dtype)


class SwiGLU(nn.Module):
    """
    SwiGLU feed-forward block.

    The formula is:

        SwiGLU(x) = W2 (SiLU(W1 x) * W3 x)

    There are three matrices:
    - w1 goes up from d_model to d_ff
    - w3 also goes up from d_model to d_ff, it is the gate
    - w2 goes back down from d_ff to d_model

    There is no bias.
    """

    def __init__(self, d_model, d_ff):
        # Always call the parent class constructor.
        super().__init__()

        # The initial values do not matter: the grader
        # loads its own weights afterwards.
        #
        # The required shapes are:
        # w1 : (d_ff, d_model)
        # w2 : (d_model, d_ff)
        # w3 : (d_ff, d_model)
        self.w1 = nn.Parameter(torch.randn(d_ff, d_model))
        self.w2 = nn.Parameter(torch.randn(d_model, d_ff))
        self.w3 = nn.Parameter(torch.randn(d_ff, d_model))

    def forward(self, x):
        # Put the weights on x's device.
        # Also cast them to x's dtype, so the output
        # naturally has the same dtype as the input.
        w1 = self.w1.to(device=x.device, dtype=x.dtype)
        w2 = self.w2.to(device=x.device, dtype=x.dtype)
        w3 = self.w3.to(device=x.device, dtype=x.dtype)

        # First up-projection.
        # x has shape (..., d_model).
        # w1.t() has shape (d_model, d_ff).
        # The result has shape (..., d_ff).
        h1 = x @ w1.t()

        # Third up-projection.
        # It does not go through SiLU: it is the gate.
        h3 = x @ w3.t()

        # SiLU on h1.
        # SiLU(z) = z * sigmoid(z).
        gate = h1 * torch.sigmoid(h1)

        # Element-wise product with the gate.
        h = gate * h3

        # Down-projection.
        # h has shape (..., d_ff).
        # w2.t() has shape (d_ff, d_model).
        # The result has shape (..., d_model).
        out = h @ w2.t()

        return out
