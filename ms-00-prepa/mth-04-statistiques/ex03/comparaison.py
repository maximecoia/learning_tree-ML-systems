"""mth-04-statistiques ex03: comparing two series.

Statement:  ./exo mth-04-statistiques ex03
Grade:      ./exo mth-04-statistiques ex03 -c
Carry:      ./exo mth-04-statistiques ex03 -r    brings estimation.py,
                                                 intervalle.py, bootstrap.py
Allowed:    estimation intervalle ValueError len sum sorted int range max min
            any abs
"""

# Import from estimation and intervalle what you need.
import estimation
import intervalle


def difference(a, b):
    # The mean of b minus the mean of a.
    return estimation.moyenne(b) - estimation.moyenne(a)


def erreur_type_difference(a, b):
    # The square root of the sum of the corrected variances, each divided
    # by its size. ValueError for a series of fewer than two measurements.
    va = estimation.variance_corrigee(a)
    vb = estimation.variance_corrigee(b)
    return (va / len(a) + vb / len(b)) ** 0.5


def intervalle_difference(a, b, quantile):
    if quantile <= 0:
        raise ValueError()
    d = difference(a, b)
    e = erreur_type_difference(a, b)
    return (d - quantile * e, d + quantile * e)


def separees(a, b, quantile):
    # True when that interval does NOT CONTAIN zero.
    bornes = intervalle_difference(a, b, quantile)
    return not intervalle.contient(bornes, 0)


def separees_par_recouvrement(a, b):
    # The other rule: the two ranges do not overlap at all. ValueError on an
    # empty series.
    if len(a) == 0 or len(b) == 0:
        raise ValueError()
    return max(a) < min(b) or max(b) < min(a)


def taux_de_faux_positifs(paires, quantile):
    # The share of pairs declared separated. ValueError on an empty list.
    if len(paires) == 0:
        raise ValueError()
    count = sum(1 for a, b in paires if separees(a, b, quantile))
    return count / len(paires)