"""mth-04-statistiques ex02: resampling.

Statement:  ./exo mth-04-statistiques ex02
Grade:      ./exo mth-04-statistiques ex02 -c
Carry:      ./exo mth-04-statistiques ex02 -r    brings estimation.py,
                                                 intervalle.py
Allowed:    estimation intervalle ValueError len sum sorted int range max min
"""

# Import from estimation what you need.

# Dictated by the statement: the generator of mth-03, rewritten here because
# a module stands on its own.
FACTEUR = 1103515245
INCREMENT = 12345
MODULE = 2 ** 31


def indices(graine, combien, taille):
    # Indices drawn in [0, taille[ with replacement, on the high bits.
    # ValueError for a zero size or a negative count.
    ...


def tirer_avec_remise(echantillon, graine):
    # A resample of the SAME SIZE.
    ...


def bootstrap(echantillon, statistique, graine, repetitions):
    # The list of the statistic's values on each resample. Each repetition
    # uses a different seed. ValueError below one repetition.
    ...


def percentile(valeurs, p):
    # By nearest rank, WITHOUT interpolation. ValueError for p outside
    # [0, 100].
    ...


def intervalle_bootstrap(echantillon, statistique, graine, repetitions, niveau=0.95):
    # The two percentiles that enclose `niveau` of the resamples.
    # ValueError for a level outside ]0, 1[.
    ...


def mediane(echantillon):
    # The mean of the two middle values when the count is even.
    ...
