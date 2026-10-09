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
        # Epsilon prevents a division by zero when the vector is zero.
        self.eps = eps

        # The subject requires a parameter named exactly "weight".
        # Its shape is (d_model,): one gain per dimension.
        # Every gain starts at 1.
        #
        # device and dtype are optional.
        # They create the parameter directly on the right device.
        self.weight = nn.Parameter(
            torch.ones(d_model, device=device, dtype=dtype)
        )

    def forward(self, x):
        # Remember the input dtype.
        # The subject asks for an output in the same dtype as x.
        input_dtype = x.dtype

        # Upcast to float32 for the arithmetic.
        # This matters when x is bfloat16 or float16.
        x_f = x.to(torch.float32)

        # Mean of the squares over the last dimension.
        #
        # If x has shape (4, 12, 64):
        # x_f * x_f           -> (4, 12, 64)
        # mean(dim=-1)        -> (4, 12) without keepdim
        # mean(keepdim=True)  -> (4, 12, 1)
        #
        # Shape (4, 12, 1) then broadcasts over the 64 dimensions.
        mean_square = (x_f * x_f).mean(dim=-1, keepdim=True)

        # Inverse square root.
        # torch.rsqrt(z) computes 1 / sqrt(z).
        # Same as 1.0 / torch.sqrt(z), in one call.
        inv_rms = torch.rsqrt(mean_square + self.eps)

        # Normalize.
        # inv_rms has shape (..., 1), so it broadcasts over
        # every component of the last axis.
        #
        # weight has shape (d_model,).
        # It broadcasts over the leading dimensions.
        #
        # Example:
        # x_f       : (4, 12, 64)
        # inv_rms   : (4, 12, 1)
        # weight    : (64,)
        # result    : (4, 12, 64)
        weight_f = self.weight.to(torch.float32)
        out = x_f * inv_rms * weight_f

        # Back to the input dtype.
        # A float32 x is unchanged.
        # A bfloat16 x gives a bfloat16 output again.
        return out.to(input_dtype)
