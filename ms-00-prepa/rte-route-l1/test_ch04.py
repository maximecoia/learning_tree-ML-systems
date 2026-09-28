"""Grade this directory's `ch04.py` against what chapter 4 states in prose.

    python3 -m pytest test_ch04.py -q      # beside ch04.py

The chapter's own notebook checks almost nothing: it prints shapes and a
parameter count and leaves the reader to compare them by eye. The claims that
matter are made in words, and words do not fail.

So the tests below assert those claims. That LayerNorm normalises each token
alone and lands its variance just below one, which is the chapter's own
observation about `eps`. That GELU is the tanh approximation and not a ReLU
with a nicer name. That the block is wired so a silent sub-layer leaves the
input untouched, which is what a residual connection means, and that each
sub-layer is handed a normalised input rather than a raw one, which is what
Pre-LayerNorm means. That a token arriving later cannot change a logit already
computed, which is the whole reason training can be parallel. That generation
appends the argmax of the last position and never feeds the model more than
its context. And that the output head is genuinely a second matrix here, since
the chapter is explicit that it did not tie the weights.

Fourteen mutations were played against the suite before it was kept, in a
throwaway copy of this directory: a LayerNorm normalising the batch axis, the
`eps` dropped from the root, a GELU replaced by a ReLU, a FeedForward widening
by two, a residual removed, the norm moved after its sub-layer, the causal
mask removed from `ch03.py`, the first position read instead of the last, an
`argmin`, the context left uncropped, the output head tied to the embedding,
the positions frozen to zero, the model returning only its last position, and
the model seeding itself. All fourteen were caught, and no test survived all
of them -- the position test and the seed test were written because the
twelfth and fourteenth mutations passed unnoticed without them.
"""

import importlib.util
import sys
from pathlib import Path

import pytest
import torch
import torch.nn as nn

HERE = Path(__file__).resolve().parent


def _answer_under_test():
    """This directory's `ch04.py`, unless a runner registered another one.

    `ch04.py` imports `MultiHeadAttention` from `ch03`, so this directory has
    to be importable before the module body runs.
    """
    already = sys.modules.get("mes_reponses.ch04")
    if already is not None:
        return already
    answer = HERE / "ch04.py"
    if not answer.is_file():
        raise FileNotFoundError(f"the answer is missing: {answer}")
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location("mes_reponses.ch04", answer)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mes_reponses.ch04"] = module
    spec.loader.exec_module(module)
    return module


MINE = _answer_under_test()

# Small enough to build in a blink, large enough that every axis is distinct:
# 12 features over 3 heads is 4 per head, and none of 2, 3, 4, 5, 12 repeat.
PETIT = {
    "vocab_size": 23,
    "context_length": 8,
    "emb_dim": 12,
    "n_heads": 3,
    "n_layers": 2,
    "drop_rate": 0.0,
    "qkv_bias": False,
}


@pytest.fixture
def x():
    """A batch of two sequences of five tokens, in the small config."""
    torch.manual_seed(0)
    return torch.randint(0, PETIT["vocab_size"], (2, 5))


@pytest.fixture
def h():
    """Hidden states, the shape every inner module passes around."""
    torch.manual_seed(1)
    return torch.randn(2, 5, PETIT["emb_dim"]) * 3.0 + 7.0


@pytest.fixture
def gpt():
    torch.manual_seed(123)
    modele = MINE.GPTModel(PETIT)
    modele.eval()
    return modele


class _Muet(nn.Module):
    """A sub-layer that contributes nothing, so only the wiring remains."""

    def forward(self, x):
        return torch.zeros_like(x)


def test_layernorm_normalises_each_token_alone(h):
    """`dim=-1` means the features of one token, not the batch, not the row.

    Checked twice: the statistics come out right per token, and perturbing one
    token leaves every other token's output bit-for-bit identical. The second
    half is what would still pass if `dim` were wrong and the first half were
    read carelessly.
    """
    norme = MINE.LayerNorm(PETIT["emb_dim"])
    sortie = norme(h)

    assert sortie.shape == h.shape
    assert torch.allclose(
        sortie.mean(dim=-1), torch.zeros(2, 5), atol=1e-5
    ), "la moyenne par token devrait être nulle"

    abime = h.clone()
    abime[0, 0] += 100.0
    autre = norme(abime)
    assert torch.equal(
        autre[0, 1:], sortie[0, 1:]
    ), "toucher un token en a changé un autre"
    assert torch.equal(
        autre[1], sortie[1]
    ), "toucher une séquence en a changé une autre"
    assert not torch.equal(abime[0, 0], h[0, 0])


def test_the_variance_lands_just_below_one(h):
    """`eps` buys stability and costs a little variance: var / (var + eps).

    The expected value is computed from the input, not from the output, so
    this is not the module restating itself.
    """
    norme = MINE.LayerNorm(PETIT["emb_dim"])
    sortie = norme(h)

    var_entree = h.var(dim=-1, keepdim=True, unbiased=False)
    attendu = var_entree / (var_entree + norme.eps)
    obtenu = sortie.var(dim=-1, keepdim=True, unbiased=False)

    assert torch.allclose(obtenu, attendu, atol=1e-6)
    assert (obtenu < 1.0).all(), "la variance devrait rester sous 1"
    assert (obtenu > 0.999).all(), "elle ne devrait s'en éloigner qu'à peine"


def test_gelu_is_the_tanh_approximation_and_not_a_relu():
    """Compared against PyTorch's own GELU, computed a different way."""
    gelu = MINE.GELU()
    u = torch.linspace(-4.0, 4.0, 401)

    attendu = nn.functional.gelu(u, approximate="tanh")
    assert torch.allclose(gelu(u), attendu, atol=1e-6)

    negatifs = u[u < -0.1]
    assert (gelu(negatifs) != 0).all(), "GELU n'efface pas tout le négatif"
    assert (gelu(negatifs) < 0).all(), "elle le rend petit, pas positif"


def test_feedforward_widens_by_four_and_comes_back(h):
    """The dimensions are read off the layers, not off the formula."""
    ff = MINE.FeedForward(PETIT)
    lineaires = [m for m in ff.modules() if isinstance(m, nn.Linear)]

    assert len(lineaires) == 2
    assert lineaires[0].in_features == PETIT["emb_dim"]
    assert lineaires[0].out_features == 4 * PETIT["emb_dim"]
    assert lineaires[1].in_features == 4 * PETIT["emb_dim"]
    assert lineaires[1].out_features == PETIT["emb_dim"]
    assert ff(h).shape == h.shape

    # And the widening is really traversed, not bypassed.
    vus = {}
    lineaires[0].register_forward_hook(
        lambda m, e, s: vus.__setitem__("large", s.shape[-1])
    )
    ff(h)
    assert vus.get("large") == 4 * PETIT["emb_dim"]


def test_the_block_is_the_identity_when_its_sublayers_are_silent(h):
    """What a residual connection means, stated as an equation.

    Both sub-layers are replaced by modules that return zeros. Whatever the
    block does around them, `x + 0 + 0` must come back unchanged. A block
    written without its `+ shortcut` returns zeros instead.
    """
    bloc = MINE.TransformerBlock(PETIT)
    bloc.eval()
    bloc.att = _Muet()
    bloc.ff = _Muet()

    assert torch.equal(bloc(h), h)


def test_each_sublayer_receives_a_normalised_input(h):
    """Pre-LayerNorm: the norm comes before the sub-layer, not after it.

    What the sub-layers receive is caught by a pre-hook rather than
    recomputed, so this observes the forward pass instead of restating it.
    """
    bloc = MINE.TransformerBlock(PETIT)
    bloc.eval()
    vus = {}

    def capte(nom):
        return lambda module, entree: vus.__setitem__(nom, entree[0].detach())

    bloc.att.register_forward_pre_hook(capte("att"))
    bloc.ff.register_forward_pre_hook(capte("ff"))
    bloc(h)

    assert set(vus) == {"att", "ff"}, "un sous-bloc n'a pas été appelé"
    for nom, recu in vus.items():
        moyenne = recu.mean(dim=-1)
        assert torch.allclose(
            moyenne, torch.zeros_like(moyenne), atol=1e-5
        ), f"{nom} a reçu une entrée non normalisée"
    assert not torch.allclose(
        h.mean(dim=-1), torch.zeros(2, 5), atol=1e-5
    ), "l'entrée brute est déjà centrée : le test ne prouverait rien"


def test_a_later_token_cannot_change_an_earlier_logit(gpt):
    """The reason training can be parallel, tested on the whole model.

    Two sequences share a prefix and differ on their last token. Every logit
    at a position before that token must be identical. Remove the causal mask
    and this fails everywhere at once.
    """
    idx = torch.tensor([[3, 7, 11, 2, 19]])
    autre = idx.clone()
    autre[0, -1] = (autre[0, -1] + 5) % PETIT["vocab_size"]
    assert not torch.equal(idx, autre)

    with torch.no_grad():
        a = gpt(idx)
        b = gpt(autre)

    assert a.shape == (1, 5, PETIT["vocab_size"])
    assert torch.equal(
        a[:, :-1, :], b[:, :-1, :]
    ), "changer le dernier token a bougé un logit antérieur"
    assert not torch.equal(
        a[:, -1, :], b[:, -1, :]
    ), "le dernier logit, lui, devrait bouger"


def test_the_model_predicts_at_every_position(gpt, x):
    """`[B, T]` in, `[B, T, vocab_size]` out: one prediction per position."""
    with torch.no_grad():
        logits = gpt(x)
    assert logits.shape == (
        x.shape[0],
        x.shape[1],
        PETIT["vocab_size"],
    )


def test_the_position_is_part_of_what_the_model_reads(gpt):
    """Feed the same token six times: the six logits must still differ.

    Without position embeddings every position would receive the very same
    vector, and causal attention over identical vectors returns that vector
    again, so the six rows would come out equal. This is what catches a
    `torch.zeros` written where `torch.arange` belongs -- a mutation that no
    shape and no causality test notices.
    """
    pareils = torch.full((1, 6), 5, dtype=torch.long)
    with torch.no_grad():
        logits = gpt(pareils)[0]

    for k in range(1, 6):
        assert not torch.allclose(
            logits[0], logits[k], atol=1e-6
        ), f"la position {k} rend la même chose que la position 0"


def test_generation_appends_the_argmax_of_the_last_position():
    """Driven by a stub whose logits are known, so the answer is known too.

    The stub answers with a different winner at each position; only the last
    one may be picked.
    """

    class _Truque(nn.Module):
        def __init__(self):
            super().__init__()
            self.vus = []

        def forward(self, idx):
            self.vus.append(idx.shape[1])
            b, t = idx.shape
            logits = torch.zeros(b, t, PETIT["vocab_size"])
            for k in range(t):
                logits[:, k, k % PETIT["vocab_size"]] = 10.0
            # La dernière position désigne un token que rien d'autre ne vise.
            logits[:, -1, :] = 0.0
            logits[:, -1, 17] = 10.0
            return logits

    modele = _Truque()
    depart = torch.tensor([[1, 2, 3]])
    out = MINE.generate_text_simple(
        modele, depart, max_new_tokens=2, context_size=8
    )

    assert out.shape == (1, 5), "deux tokens auraient dû être ajoutés"
    assert torch.equal(out[:, :3], depart), "le départ doit être conservé"
    assert out[0, 3].item() == 17
    assert out[0, 4].item() == 17
    assert modele.vus == [3, 4], "le contexte doit grandir d'un token par tour"


def test_generation_never_feeds_more_than_the_context():
    """`idx[:, -context_size:]` keeps the newest tokens, and only those."""

    class _Compteur(nn.Module):
        def __init__(self):
            super().__init__()
            self.vus = []

        def forward(self, idx):
            self.vus.append(idx.clone())
            b, t = idx.shape
            logits = torch.zeros(b, t, PETIT["vocab_size"])
            logits[:, -1, 4] = 1.0
            return logits

    modele = _Compteur()
    depart = torch.tensor([[1, 2, 3, 4, 5, 6]])
    MINE.generate_text_simple(modele, depart, max_new_tokens=3, context_size=4)

    assert [t.shape[1] for t in modele.vus] == [4, 4, 4]
    assert torch.equal(modele.vus[0][0], torch.tensor([3, 4, 5, 6]))
    assert torch.equal(modele.vus[1][0], torch.tensor([4, 5, 6, 4]))
    assert torch.equal(modele.vus[2][0], torch.tensor([5, 6, 4, 4]))


def test_the_output_head_is_not_tied_to_the_embedding(gpt):
    """The chapter says so explicitly, and the count depends on it."""
    assert gpt.out_head.weight is not gpt.tok_emb.weight
    assert not torch.equal(gpt.out_head.weight, gpt.tok_emb.weight)

    total = sum(p.numel() for p in gpt.parameters())
    tete = sum(p.numel() for p in gpt.out_head.parameters())
    assert tete == PETIT["vocab_size"] * PETIT["emb_dim"]
    assert total - tete < total


def test_the_counts_the_chapter_quotes():
    """163 M built, 124 M if the head were shared. Built once, on the real
    configuration, because the numbers are the claim."""
    torch.manual_seed(123)
    grand = MINE.GPTModel(MINE.GPT_CONFIG_124M)

    total = sum(p.numel() for p in grand.parameters())
    tete = sum(p.numel() for p in grand.out_head.parameters())

    assert total == 163_009_536
    assert total - tete == 124_412_160
    assert tete == 50257 * 768


def test_the_same_seed_gives_the_same_initial_weights():
    """What `torch.manual_seed(123)` buys, and what it does not."""
    torch.manual_seed(123)
    a = MINE.GPTModel(PETIT)
    torch.manual_seed(123)
    b = MINE.GPTModel(PETIT)
    torch.manual_seed(7)
    c = MINE.GPTModel(PETIT)

    for (na, pa), (nb, pb) in zip(a.named_parameters(), b.named_parameters()):
        assert na == nb
        assert torch.equal(pa, pb), f"{na} diffère malgré la même graine"

    differents = [
        na
        for (na, pa), (_, pc) in zip(
            a.named_parameters(), c.named_parameters()
        )
        if not torch.equal(pa, pc)
    ]
    assert differents, "deux graines différentes ont donné les mêmes poids"
