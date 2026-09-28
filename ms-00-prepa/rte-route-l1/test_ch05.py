"""Grade this directory's `ch05.py` against what chapter 5 states in prose.

    python3 -m pytest test_ch05.py -q      # beside ch05.py

The chapter's claims are the kind that a printed number seems to confirm and
never does: that an untrained model's loss lands near log(vocab_size), that
`flatten(0, 1)` is not an arbitrary reshape, that `temperature` and `top_k`
change how a token is picked and never the weights, that a checkpoint brings
back the same model. Each is asserted here against a property computed a
different way from the code under test.

Two tests observe rather than recompute, as in `test_ch03.py` and
`test_ch04.py`: what `calc_loss_loader` really reads is caught by a loader that
counts, and what `generate` really feeds the model is caught by a stub that
records its inputs.

Sixteen mutations were played against the suite before it was kept, in a
throwaway copy of this directory: the predictions flipped against their
targets, the `num_batches` bound ignored, an empty loader answering zero
instead of nan, `evaluate_model` forgetting to hand the model back in train
mode, the same function building a graph, `zero_grad` removed, `global_step`
starting at zero, `tokens_seen` counting batches, `optimizer.step` removed,
sampling collapsed into an argmax, `temperature = 0` no longer falling through
to greedy, the top-k threshold inverted, the context left uncropped, `assign`
accepting any shape, the batch axis dropped, and the loss halved.

All sixteen were caught, and no test survived all of them. Two tests were
rewritten because a mutation passed unnoticed: the loader test asserted how
many batches were pulled rather than how many were averaged -- the loop pulls
one it never uses -- and the gradient test read `p.grad`, which only fills on a
backward pass that evaluation never makes.
"""

import importlib.util
import math
import sys

from pathlib import Path

import pytest
import torch
import torch.nn as nn

HERE = Path(__file__).resolve().parent


def _answer_under_test():
    """This directory's `ch05.py`, unless a runner registered another one."""
    already = sys.modules.get("mes_reponses.ch05")
    if already is not None:
        return already
    answer = HERE / "ch05.py"
    if not answer.is_file():
        raise FileNotFoundError(f"the answer is missing: {answer}")
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location("mes_reponses.ch05", answer)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mes_reponses.ch05"] = module
    spec.loader.exec_module(module)
    return module


MINE = _answer_under_test()

PETIT = {
    "vocab_size": 61,
    "context_length": 16,
    "emb_dim": 12,
    "n_heads": 3,
    "n_layers": 2,
    "drop_rate": 0.0,
    "qkv_bias": False,
}

DEVICE = torch.device("cpu")


@pytest.fixture
def modele():
    torch.manual_seed(123)
    m = MINE.GPTModel(PETIT)
    m.eval()
    return m


@pytest.fixture
def lot():
    """Un batch et sa cible décalée d'un token, comme le chapitre 2 les fait."""
    torch.manual_seed(0)
    ids = torch.randint(0, PETIT["vocab_size"], (2, 9))
    return ids[:, :-1], ids[:, 1:]


class _Compteur:
    """Un loader qui rend toujours le même lot, et dit combien on lui en prend."""

    def __init__(self, lot, taille):
        self.lot = lot
        self.taille = taille
        self.lus = 0

    def __len__(self):
        return self.taille

    def __iter__(self):
        for _ in range(self.taille):
            self.lus += 1
            yield self.lot


def test_an_untrained_loss_lands_on_log_of_the_vocabulary(modele, lot):
    """Le repère que le chapitre ajoute : ignorer, c'est valoir log(V).

    La valeur attendue vient de la taille du vocabulaire, pas du modèle : rien
    n'est ici recalculé à partir de ce qu'on mesure.
    """
    entree, cible = lot
    with torch.no_grad():
        perte = MINE.calc_loss_batch(entree, cible, modele, DEVICE).item()

    attendu = math.log(PETIT["vocab_size"])
    assert (
        abs(perte - attendu) < 0.6
    ), f"loss {perte:.3f} loin de log({PETIT['vocab_size']}) = {attendu:.3f}"

    # Et le repère bouge avec le vocabulaire, ce qui montre qu'il en dépend.
    grand = dict(PETIT, vocab_size=601)
    torch.manual_seed(123)
    autre = MINE.GPTModel(grand)
    autre.eval()
    ids = torch.randint(0, 601, (2, 9))
    with torch.no_grad():
        perte2 = MINE.calc_loss_batch(
            ids[:, :-1], ids[:, 1:], autre, DEVICE
        ).item()
    assert perte2 > perte + 1.0, "un vocabulaire dix fois plus grand devrait "
    "coûter environ log(10) de plus"


def test_the_loss_is_minus_log_of_the_right_tokens_probability(modele, lot):
    """La dérivation à la main du chapitre, refaite pas à pas.

    softmax, puis la probabilité du bon token, puis log, puis la moyenne, puis
    le signe. C'est un chemin différent de `F.cross_entropy`, et il doit
    tomber sur le même nombre.
    """
    entree, cible = lot
    with torch.no_grad():
        logits = modele(entree)
        probas = torch.softmax(logits, dim=-1)

        # La probabilité attribuée au token correct, position par position.
        bonnes = probas.gather(-1, cible.unsqueeze(-1)).squeeze(-1)
        a_la_main = -torch.log(bonnes).mean().item()

        par_pytorch = MINE.calc_loss_batch(
            entree, cible, modele, DEVICE
        ).item()

    assert abs(a_la_main - par_pytorch) < 1e-5


def test_flatten_keeps_every_prediction_paired_with_its_target(modele, lot):
    """`flatten(0, 1)` aligne B×T prédictions sur B×T réponses, dans l'ordre.

    Vérifié en recalculant la loss position par position : la moyenne des
    pertes individuelles doit valoir la loss globale. Un remplissage qui
    mélangerait les axes casserait cette égalité.
    """
    entree, cible = lot
    b, t = entree.shape
    with torch.no_grad():
        logits = modele(entree)
        une_a_une = [
            torch.nn.functional.cross_entropy(
                logits[i, j].unsqueeze(0), cible[i, j].unsqueeze(0)
            ).item()
            for i in range(b)
            for j in range(t)
        ]
        globale = MINE.calc_loss_batch(entree, cible, modele, DEVICE).item()

    assert len(une_a_une) == b * t
    assert abs(sum(une_a_une) / len(une_a_une) - globale) < 1e-5


def test_the_loader_averages_exactly_the_batches_it_was_asked_for(modele):
    """`num_batches` borne ce qui est MOYENNÉ, ce qui est la vraie promesse.

    Une première version comptait les lots tirés du loader et attendait trois :
    la boucle en tire un quatrième avant de tester son indice et de sortir,
    sans jamais s'en servir. Elle mesurait donc la mécanique de la boucle, pas
    ce que la fonction annonce. Chaque lot porte ici une perte différente, et
    c'est la moyenne qui tranche.
    """
    torch.manual_seed(7)
    lots = [
        (
            torch.randint(0, PETIT["vocab_size"], (2, 8)),
            torch.randint(0, PETIT["vocab_size"], (2, 8)),
        )
        for _ in range(6)
    ]

    with torch.no_grad():
        unitaires = [
            MINE.calc_loss_batch(e, c, modele, DEVICE).item() for e, c in lots
        ]

    class _Suite:
        def __init__(self, lots):
            self.lots = lots

        def __len__(self):
            return len(self.lots)

        def __iter__(self):
            return iter(self.lots)

    with torch.no_grad():
        trois = MINE.calc_loss_loader(_Suite(lots), modele, DEVICE, 3)
        tous = MINE.calc_loss_loader(_Suite(lots), modele, DEVICE)
        trop = MINE.calc_loss_loader(_Suite(lots), modele, DEVICE, 99)

    assert abs(trois - sum(unitaires[:3]) / 3) < 1e-6
    assert abs(tous - sum(unitaires) / 6) < 1e-6
    assert (
        abs(trop - sum(unitaires) / 6) < 1e-6
    ), "une borne plus grande que le loader ne doit pas inventer de lots"
    # Les six pertes diffèrent assez pour que les trois moyennes se distinguent.
    assert len({round(trois, 6), round(tous, 6)}) == 2


def test_an_empty_loader_says_nan_rather_than_dividing_by_zero(modele, lot):
    vide = _Compteur(lot, taille=0)
    assert math.isnan(MINE.calc_loss_loader(vide, modele, DEVICE))
    assert vide.lus == 0


def test_evaluating_leaves_the_model_in_training_mode(modele, lot):
    """`evaluate_model` passe en eval() puis rend le modèle à train()."""
    entree, cible = lot
    loader = _Compteur((entree, cible), taille=2)

    modele.train()
    assert modele.training

    MINE.evaluate_model(modele, loader, loader, DEVICE, eval_iter=2)

    assert modele.training, "le modèle aurait dû repartir en mode train"


def test_evaluating_builds_no_graph(modele, lot):
    """`no_grad` n'est pas décoratif : aucun graphe ne doit être construit.

    Une première version regardait `p.grad` après l'évaluation et le trouvait
    vide — mais `.grad` ne se remplit qu'au `backward()`, jamais appelé ici.
    Elle ne voyait donc pas la différence entre `no_grad` et `enable_grad`.
    Ce qui distingue vraiment les deux se lit sur la sortie du modèle : sous
    `no_grad` elle ne réclame pas de gradient. On l'observe par un hook, au
    moment où le modèle rend sa sortie.
    """
    entree, cible = lot
    loader = _Compteur((entree, cible), taille=2)

    vus = []
    poignee = modele.register_forward_hook(
        lambda m, e, sortie: vus.append(sortie.requires_grad)
    )
    try:
        MINE.evaluate_model(modele, loader, loader, DEVICE, eval_iter=2)
    finally:
        poignee.remove()

    assert vus, "le modèle n'a pas été appelé"
    assert not any(vus), "une sortie réclamait un gradient"

    # Et hors du bloc, la même mesure doit voir l'inverse : sinon elle ne
    # prouverait rien de plus qu'un modèle sans paramètre entraînable.
    temoin = []
    poignee = modele.register_forward_hook(
        lambda m, e, sortie: temoin.append(sortie.requires_grad)
    )
    try:
        MINE.calc_loss_batch(entree, cible, modele, DEVICE)
    finally:
        poignee.remove()

    assert temoin == [True]


def test_training_clears_the_gradients_between_steps(modele, lot):
    """Sans `zero_grad`, les gradients s'additionneraient d'un batch à l'autre.

    L'optimizer est doublé par un témoin qui note l'ordre des appels : c'est
    l'ordre qui est vérifié, pas le fait qu'une ligne existe.
    """
    entree, cible = lot

    class _Temoin(torch.optim.AdamW):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.ordre = []

        def zero_grad(self, *a, **k):
            self.ordre.append("zero")
            return super().zero_grad(*a, **k)

        def step(self, *a, **k):
            self.ordre.append("step")
            return super().step(*a, **k)

    optimizer = _Temoin(modele.parameters(), lr=1e-4)
    loader = _Compteur((entree, cible), taille=3)

    MINE.train_model_simple(
        model=modele,
        train_loader=loader,
        val_loader=_Compteur((entree, cible), taille=1),
        optimizer=optimizer,
        device=DEVICE,
        num_epochs=1,
        eval_freq=99,
        eval_iter=1,
        start_context="a",
        tokenizer=_Tokenizer(),
    )

    assert optimizer.ordre == ["zero", "step"] * 3, optimizer.ordre


class _Tokenizer:
    """Le minimum que `generate_and_print_sample` demande d'un tokenizer."""

    def encode(self, texte, allowed_special=None):
        return [1, 2, 3]

    def decode(self, ids):
        return " ".join(str(i) for i in ids)


def test_the_very_first_step_is_evaluated(modele, lot):
    """`global_step = -1` existe pour qu'un point soit pris au tout début."""
    entree, cible = lot
    optimizer = torch.optim.AdamW(modele.parameters(), lr=1e-4)

    pertes, _, vus = MINE.train_model_simple(
        model=modele,
        train_loader=_Compteur((entree, cible), taille=4),
        val_loader=_Compteur((entree, cible), taille=1),
        optimizer=optimizer,
        device=DEVICE,
        num_epochs=1,
        eval_freq=100,
        eval_iter=1,
        start_context="a",
        tokenizer=_Tokenizer(),
    )

    assert len(pertes) == 1, "un seul point, celui du premier pas"
    assert vus == [
        entree.numel()
    ], "il doit être pris après un seul batch, pas avant ni plus tard"


def test_tokens_seen_counts_the_elements_of_the_input(modele, lot):
    entree, cible = lot
    optimizer = torch.optim.AdamW(modele.parameters(), lr=1e-4)

    _, _, vus = MINE.train_model_simple(
        model=modele,
        train_loader=_Compteur((entree, cible), taille=6),
        val_loader=_Compteur((entree, cible), taille=1),
        optimizer=optimizer,
        device=DEVICE,
        num_epochs=1,
        eval_freq=2,
        eval_iter=1,
        start_context="a",
        tokenizer=_Tokenizer(),
    )

    pas = entree.numel()
    assert vus == [pas, 3 * pas, 5 * pas], vus


def test_training_actually_lowers_the_loss(modele, lot):
    """Sur un seul batch répété, le modèle doit finir par l'apprendre."""
    entree, cible = lot
    optimizer = torch.optim.AdamW(modele.parameters(), lr=0.01)

    avant = MINE.calc_loss_batch(entree, cible, modele, DEVICE).item()
    MINE.train_model_simple(
        model=modele,
        train_loader=_Compteur((entree, cible), taille=30),
        val_loader=_Compteur((entree, cible), taille=1),
        optimizer=optimizer,
        device=DEVICE,
        num_epochs=1,
        eval_freq=99,
        eval_iter=1,
        start_context="a",
        tokenizer=_Tokenizer(),
    )
    apres = MINE.calc_loss_batch(entree, cible, modele, DEVICE).item()

    assert apres < avant - 1.0, f"{avant:.3f} -> {apres:.3f}"


class _Truque(nn.Module):
    """Un modèle dont les logits sont connus, et qui note ce qu'on lui donne."""

    def __init__(self, ordre):
        super().__init__()
        self.ordre = ordre
        self.vus = []

    def forward(self, idx):
        self.vus.append(idx.clone())
        b, t = idx.shape
        logits = torch.zeros(b, t, PETIT["vocab_size"])
        for rang, token in enumerate(self.ordre):
            logits[:, -1, token] = 10.0 - rang
        return logits


def test_temperature_zero_is_greedy_and_repeatable():
    """Sans tirage, deux appels donnent exactement la même suite."""
    modele = _Truque([7, 3, 5])
    depart = torch.tensor([[1, 2]])

    a = MINE.generate(modele, depart, 4, 16, temperature=0.0)
    b = MINE.generate(modele, depart, 4, 16, temperature=0.0)

    assert torch.equal(a, b)
    assert a[0, 2:].tolist() == [7, 7, 7, 7], "l'argmax, toujours le même"


def test_sampling_can_pick_something_other_than_the_argmax():
    """Avec une température, le tirage n'est plus déterministe."""
    modele = _Truque([7, 3, 5])
    depart = torch.tensor([[1, 2]])

    torch.manual_seed(0)
    a = MINE.generate(modele, depart, 20, 16, temperature=2.0)
    torch.manual_seed(1)
    b = MINE.generate(modele, depart, 20, 16, temperature=2.0)

    assert not torch.equal(a, b), "deux graines devraient diverger"
    assert set(a[0, 2:].tolist()) != {
        7
    }, "le tirage ne doit pas être un argmax"


def test_top_k_never_draws_outside_the_k_best():
    """Les autres tokens passent à -inf, donc à une probabilité nulle."""
    meilleurs = [7, 3, 5]
    modele = _Truque(meilleurs)
    depart = torch.tensor([[1, 2]])

    torch.manual_seed(0)
    sortie = MINE.generate(modele, depart, 40, 16, temperature=3.0, top_k=3)
    tires = set(sortie[0, 2:].tolist())

    assert tires <= set(meilleurs), f"{tires - set(meilleurs)} hors du top-3"
    assert len(tires) > 1, "avec une température de 3, le tirage doit varier"


def test_generation_never_feeds_more_than_the_context():
    """`idx[:, -context_size:]` garde les derniers tokens, et eux seuls."""
    modele = _Truque([4])
    depart = torch.tensor([[1, 2, 3, 4, 5, 6]])

    MINE.generate(modele, depart, 3, context_size=4)

    assert [v.shape[1] for v in modele.vus] == [4, 4, 4]
    assert modele.vus[0][0].tolist() == [3, 4, 5, 6]
    assert modele.vus[1][0].tolist() == [4, 5, 6, 4]


def test_assign_refuses_a_shape_that_does_not_match():
    """La protection qui transforme une architecture fausse en erreur."""
    gauche = torch.nn.Parameter(torch.zeros(3, 4))

    juste = MINE.assign(gauche, torch.ones(3, 4).numpy())
    assert juste.shape == (3, 4)
    assert torch.equal(juste.data, torch.ones(3, 4))

    with pytest.raises(ValueError, match="Shape mismatch"):
        MINE.assign(gauche, torch.ones(4, 3).numpy())


def test_text_survives_the_round_trip_through_token_ids():
    import tiktoken

    tokenizer = tiktoken.get_encoding("gpt2")
    texte = "Every effort moves you"

    ids = MINE.text_to_token_ids(texte, tokenizer)
    assert ids.ndim == 2 and ids.shape[0] == 1, "l'axe du batch doit être là"

    assert MINE.token_ids_to_text(ids, tokenizer) == texte
