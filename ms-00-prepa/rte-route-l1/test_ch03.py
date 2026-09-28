"""Grade this directory's `ch03.py` against what chapter 3 states in prose.

    python3 -m pytest test_ch03.py -q      # beside ch03.py

Upstream's grader is not reused here, and that is a decision, not an
oversight. `pkg/llms_from_scratch/tests/test_ch03.py` holds one function and
zero assertions: its two result lines read `context_vecs.shape ==
torch.Size([8, 6, d_out])`, expressions whose value is discarded, so it passes
on any shape whatsoever. It also imports `PyTorchMultiHeadAttention`, the
bonus class built on `F.scaled_dot_product_attention`, which the chapter's own
code never builds. Binding it would buy a green line and no coverage.

So the tests below are mine. They assert the four claims the chapter makes in
words and no grader checks: the future weighs exactly zero and not almost
zero, each row of weights still sums to one after masking, the mask is a
buffer and not a parameter, and each head scales by the square root of
head_dim rather than of d_out. Two more check what the shapes alone cannot:
that the heads really are independent before the output projection, and that
an indivisible d_out is refused at construction rather than silently rounded.
"""

import importlib.util
import math
import sys
from pathlib import Path

import pytest
import torch

HERE = Path(__file__).resolve().parent

D_IN = 3
D_OUT = 4
NUM_HEADS = 2
HEAD_DIM = D_OUT // NUM_HEADS
CONTEXT_LENGTH = 6


def _answer_under_test():
    """This directory's `ch03.py`, unless a runner registered another one.

    Same door as `test_ch02.py`: a blank-file runner may publish its own
    module under this name first, and honouring what is already in
    `sys.modules` is what lets such a run measure the blank file instead of
    quietly importing the answer.
    """
    already = sys.modules.get("mes_reponses.ch03")
    if already is not None:
        return already
    answer = HERE / "ch03.py"
    if not answer.is_file():
        raise FileNotFoundError(f"the answer is missing: {answer}")
    spec = importlib.util.spec_from_file_location("mes_reponses.ch03", answer)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mes_reponses.ch03"] = module
    spec.loader.exec_module(module)
    return module


MINE = _answer_under_test()


@pytest.fixture
def batch():
    """Two identical sequences, so a difference can only come from the code."""
    return torch.stack((MINE.INPUTS, MINE.INPUTS), dim=0)


@pytest.fixture
def mha():
    torch.manual_seed(123)
    return MINE.MultiHeadAttention(
        d_in=D_IN,
        d_out=D_OUT,
        context_length=CONTEXT_LENGTH,
        dropout=0.0,
        num_heads=NUM_HEADS,
    ).eval()


def _weights(module, x):
    """The attention weights the module really computed, caught in passing.

    An earlier version of this helper recomputed them from the module's
    projections, applying the mask and the divisor itself. Two mutations of
    `ch03.py` then went unnoticed -- dropping the mask entirely, and scaling
    by sqrt(d_out) -- because the test was measuring its own arithmetic and
    not the module's. The weights are now read where the module hands them
    over: `self.dropout` receives exactly `attn_weights`, so a pre-hook on it
    observes the forward pass instead of restating it.
    """
    vus = {}

    def capte(_module, entree):
        vus["w"] = entree[0].detach().clone()

    poignee = module.dropout.register_forward_pre_hook(capte)
    try:
        module(x)
    finally:
        poignee.remove()
    assert "w" in vus, "le module n'a pas appelé self.dropout"
    return vus["w"]


def test_the_future_weighs_exactly_zero(mha, batch):
    """Masking writes -inf, so exp gives 0, not a small number."""
    w = _weights(mha, batch)
    futur = torch.triu(
        torch.ones(batch.shape[1], batch.shape[1], dtype=torch.bool),
        diagonal=1,
    )
    assert torch.all(w[:, :, futur] == 0.0)
    # And the first token, which has only itself to look at, gives itself all
    # of the weight: a mask that leaked would make this less than one.
    assert torch.allclose(w[:, :, 0, 0], torch.ones_like(w[:, :, 0, 0]))


def test_every_row_still_sums_to_one(mha, batch):
    """Softmax is taken after the mask, so the surviving weights renormalise."""
    w = _weights(mha, batch)
    assert torch.allclose(
        w.sum(dim=-1), torch.ones_like(w.sum(dim=-1)), atol=1e-6
    )


def test_the_mask_is_a_buffer_and_not_a_parameter(mha):
    """It belongs to the module and follows it, but it never learns."""
    noms = {n for n, _ in mha.named_parameters()}
    assert "mask" not in noms
    assert "mask" in dict(mha.named_buffers())
    assert "mask" in mha.state_dict()


def test_each_head_scales_by_sqrt_head_dim(mha, batch):
    """sqrt(head_dim), not sqrt(d_out): the chapter says so and it matters.

    Head 0 is recomputed here from the module's own weights, by hand, with the
    right divisor. Dividing by sqrt(d_out) instead gives a different
    distribution, which the second assertion demands.
    """
    w = _weights(mha, batch)

    queries = mha.W_query(batch)[:, :, :HEAD_DIM]
    keys = mha.W_key(batch)[:, :, :HEAD_DIM]
    scores = queries @ keys.transpose(1, 2)
    mask = mha.mask.bool()[: batch.shape[1], : batch.shape[1]]
    scores = scores.masked_fill(mask, -torch.inf)

    juste = torch.softmax(scores / math.sqrt(HEAD_DIM), dim=-1)
    faux = torch.softmax(scores / math.sqrt(D_OUT), dim=-1)

    assert torch.allclose(w[:, 0], juste, atol=1e-6)
    assert not torch.allclose(w[:, 0], faux, atol=1e-6)


def test_the_heads_are_independent(mha, batch):
    """Before the output projection, head 1 cannot reach head 0's slice.

    out_proj is the one layer that mixes them, so it is replaced by identity
    here; otherwise every output depends on every head and the claim cannot
    be tested at all.
    """
    mha.out_proj = torch.nn.Identity()
    avant = mha(batch)

    with torch.no_grad():
        # Disturb only the columns of V that head 1 reads.
        mha.W_value.weight[HEAD_DIM:, :] += 1.0
    apres = mha(batch)

    assert torch.allclose(
        avant[..., :HEAD_DIM], apres[..., :HEAD_DIM], atol=1e-6
    )
    assert not torch.allclose(
        avant[..., HEAD_DIM:], apres[..., HEAD_DIM:], atol=1e-6
    )


def test_an_indivisible_d_out_is_refused(batch):
    """7 heads cannot share 4 dimensions, and the code says so at once."""
    with pytest.raises(AssertionError):
        MINE.MultiHeadAttention(
            d_in=D_IN,
            d_out=D_OUT,
            context_length=CONTEXT_LENGTH,
            dropout=0.0,
            num_heads=7,
        )


def test_dropout_is_inert_under_eval_and_active_under_train(batch):
    """The rate only applies while training, and the chapter insists on it."""
    torch.manual_seed(123)
    module = MINE.MultiHeadAttention(
        d_in=D_IN,
        d_out=D_OUT,
        context_length=CONTEXT_LENGTH,
        dropout=0.5,
        num_heads=NUM_HEADS,
    )

    module.eval()
    assert torch.equal(module(batch), module(batch))

    module.train()
    torch.manual_seed(1)
    a = module(batch)
    torch.manual_seed(2)
    b = module(batch)
    assert not torch.allclose(a, b, atol=1e-6)


def test_the_shapes_the_chapter_asks_you_to_recite(batch):
    """The four shapes of section 39, asserted rather than printed."""
    assert MINE.simple_attention(MINE.INPUTS).shape == torch.Size([6, 3])

    torch.manual_seed(123)
    sa = MINE.SelfAttention(d_in=D_IN, d_out=2)
    assert sa(MINE.INPUTS).shape == torch.Size([6, 2])

    ca = MINE.CausalAttention(
        d_in=D_IN, d_out=2, context_length=CONTEXT_LENGTH, dropout=0.0
    )
    assert ca(batch).shape == torch.Size([2, 6, 2])

    m = MINE.MultiHeadAttention(
        d_in=D_IN,
        d_out=D_OUT,
        context_length=CONTEXT_LENGTH,
        dropout=0.0,
        num_heads=NUM_HEADS,
    )
    assert m(batch).shape == torch.Size([2, 6, D_OUT])
