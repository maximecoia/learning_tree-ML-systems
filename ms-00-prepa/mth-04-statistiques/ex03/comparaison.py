"""mth-04-statistiques ex03: comparing two series.

Statement:  ./exo mth-04-statistiques ex03
Grade:      ./exo mth-04-statistiques ex03 -c
Carry:      ./exo mth-04-statistiques ex03 -r    brings estimation.py,
                                                 intervalle.py, bootstrap.py
Allowed:    estimation intervalle ValueError len sum sorted int range max min
            any abs
"""

# Import from estimation and intervalle what you need.


def difference(a, b):
    # The mean of b minus the mean of a.
    ...


def erreur_type_difference(a, b):
    # The square root of the sum of the corrected variances, each divided
    # by its size. ValueError for a series of fewer than two measurements.
    ...


def intervalle_difference(a, b, quantile):
    ...


def separees(a, b, quantile):
    # True when that interval does NOT CONTAIN zero.
    ...


def separees_par_recouvrement(a, b):
    # The other rule: the two ranges do not overlap at all. ValueError on an
    # empty series.
    ...


def taux_de_faux_positifs(paires, quantile):
    # The share of pairs declared separated. ValueError on an empty list.
    ...
