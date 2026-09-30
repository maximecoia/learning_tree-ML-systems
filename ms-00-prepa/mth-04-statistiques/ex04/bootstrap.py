"""mth-04-statistiques ex02: resampling.

Statement:  ./exo mth-04-statistiques ex02
Grade:      ./exo mth-04-statistiques ex02 -c
Carry:      ./exo mth-04-statistiques ex02 -r    brings estimation.py,
                                                 intervalle.py
Allowed:    estimation intervalle ValueError len sum sorted int range max min
"""

# Dictated by the statement: the generator of mth-03, rewritten here because
# a module stands on its own.
FACTEUR = 1103515245
INCREMENT = 12345
MODULE = 2 ** 31


def indices(graine, combien, taille):
    # Indices drawn in [0, taille[ with replacement, on the high bits.
    # ValueError for a zero size or a negative count.
    if taille <= 0:
        raise ValueError()
    if combien < 0:
        raise ValueError()
    resultats = []
    etat = graine
    for _ in range(combien):
        etat = (FACTEUR * etat + INCREMENT) % MODULE
        resultats.append(int(etat / MODULE * taille))
    return resultats


def tirer_avec_remise(echantillon, graine):
    # A resample of the SAME SIZE.
    n = len(echantillon)
    idx = indices(graine, n, n)
    return [echantillon[i] for i in idx]


def bootstrap(echantillon, statistique, graine, repetitions):
    # The list of the statistic's values on each resample. Each repetition
    # uses a different seed. ValueError below one repetition.
    if repetitions < 1:
        raise ValueError()
    resultats = []
    for i in range(repetitions):
        reechantillon = tirer_avec_remise(echantillon, graine + i)
        resultats.append(statistique(reechantillon))
    return resultats


def percentile(valeurs, p):
    # By nearest rank, WITHOUT interpolation. ValueError for p outside
    # [0, 100].
    if p < 0 or p > 100:
        raise ValueError()
    if len(valeurs) == 0:
        raise ValueError()
    tries = sorted(valeurs)
    n = len(tries)
    x = p * n / 100
    rang = int(x)
    # A float can land a hair above a whole rank: (1 - 0.95) / 2 * 100 is
    # 2.500000000000002, so 2.5 % of 200 values reads 5.000000000000004, and
    # a strict ceiling would step to rank 6. Only a real fraction moves up.
    if x - rang > 1e-9:
        rang += 1
    if rang < 1:
        rang = 1
    return tries[rang - 1]


def intervalle_bootstrap(echantillon, statistique, graine, repetitions, niveau=0.95):
    # The two percentiles that enclose `niveau` of the resamples.
    # ValueError for a level outside ]0, 1[.
    if niveau <= 0 or niveau >= 1:
        raise ValueError()
    valeurs = bootstrap(echantillon, statistique, graine, repetitions)
    alpha = (1 - niveau) / 2 * 100
    return (percentile(valeurs, alpha), percentile(valeurs, 100 - alpha))


def mediane(echantillon):
    # The mean of the two middle values when the count is even.
    if len(echantillon) == 0:
        raise ValueError()
    tries = sorted(echantillon)
    n = len(tries)
    if n % 2 == 1:
        return tries[n // 2]
    return (tries[n // 2 - 1] + tries[n // 2]) / 2