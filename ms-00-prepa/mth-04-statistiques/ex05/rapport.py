"""mth-04-statistiques ex05: a report that refuses.

Statement:  ./exo mth-04-statistiques ex05
Grade:      ./exo mth-04-statistiques ex05 -c
Carry:      ./exo mth-04-statistiques ex05 -r    brings estimation.py,
                                                 intervalle.py, bootstrap.py,
                                                 comparaison.py, multiples.py
Allowed:    estimation intervalle bootstrap comparaison multiples ValueError
            len sum sorted int range max min any abs
"""

# Import from comparaison and estimation what you need.

# Dictated by the statement.
VERDICTS = ("a est plus petit", "b est plus petit", "indécis")


def mesures_pour_detecter(ecart, dispersion, quantile):
    # 2 * q**2 * sigma**2 / ecart**2, ROUNDED UP. ValueError for a zero or
    # negative gap, a negative dispersion or a zero quantile.
    ...


def comparer(a, b, quantile):
    # A dict with moyenne_a, moyenne_b, difference, intervalle, erreur_type,
    # separees, verdict, recouvrement and mesures_necessaires.
    # verdict is "indécis" when separees is False, and otherwise names the
    # SMALLER series, the question one asks of latencies.
    # mesures_necessaires is None when the difference is zero, and otherwise
    # uses the LARGER of the two dispersions.
    ...
