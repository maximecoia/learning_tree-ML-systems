"""mth-04-statistiques ex04: multiple comparisons.

Statement:  ./exo mth-04-statistiques ex04
Grade:      ./exo mth-04-statistiques ex04 -c
Carry:      ./exo mth-04-statistiques ex04 -r    brings estimation.py,
                                                 intervalle.py, bootstrap.py,
                                                 comparaison.py
Allowed:    estimation intervalle bootstrap comparaison ValueError len sum
            sorted int range max min any abs
"""

# Import separees from comparaison.
from comparaison import separees


def risque_au_moins_un(taux, essais):
    # 1 - (1 - taux) ** essais. ValueError for a rate outside [0, 1] or a
    # negative number of trials.
    if taux < 0 or taux > 1:
        raise ValueError()
    if essais < 0:
        raise ValueError()
    return 1 - (1 - taux) ** essais


def seuil_de_bonferroni(niveau, essais):
    # (1 - niveau) / essais. ValueError for a level outside ]0, 1[ or fewer
    # than one trial.
    if niveau <= 0 or niveau >= 1:
        raise ValueError()
    if essais < 1:
        raise ValueError()
    return (1 - niveau) / essais


def comparer_plusieurs(paires, quantile):
    # The verdict of each pair, in the order received. ValueError on an
    # empty list.
    if len(paires) == 0:
        raise ValueError()
    return [separees(a, b, quantile) for a, b in paires]


def au_moins_une(verdicts):
    return any(verdicts)