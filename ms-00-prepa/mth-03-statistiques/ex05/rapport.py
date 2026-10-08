"""mth-03-statistiques ex05: a report that refuses.

Statement:  ./exo mth-03-statistiques ex05
Grade:      ./exo mth-03-statistiques ex05 -c
Carry:      ./exo mth-03-statistiques ex05 -r    brings estimation.py,
                                                 intervalle.py, bootstrap.py,
                                                 comparaison.py, multiples.py
Allowed:    estimation intervalle bootstrap comparaison multiples ValueError
            len sum sorted int range max min any abs
"""

# Import from comparaison and estimation what you need.
import estimation
import comparaison

# Dictated by the statement.
VERDICTS = ("a est plus petit", "b est plus petit", "indécis")


def mesures_pour_detecter(ecart, dispersion, quantile):
    # 2 * q**2 * sigma**2 / ecart**2, ROUNDED UP. ValueError for a zero or
    # negative gap, a negative dispersion or a zero quantile.
    if ecart <= 0:
        raise ValueError()
    if dispersion < 0:
        raise ValueError()
    if quantile == 0:
        raise ValueError()
    n = 2 * quantile ** 2 * dispersion ** 2 / ecart ** 2
    entier = int(n)
    # A float can land a hair above a whole count: for a gap of 0.01, a
    # dispersion of 0.81 and a quantile of 1, n reads 13122.000000000002,
    # and a strict ceiling would ask for 13123 measurements.
    # Only a real fraction moves up. The tolerance is relative, because the
    # rounding noise grows with the count itself.
    if n - entier > n * 1e-12:
        return entier + 1
    return entier


def comparer(a, b, quantile):
    # A dict with moyenne_a, moyenne_b, difference, intervalle, erreur_type,
    # separees, verdict, recouvrement and mesures_necessaires.
    # verdict is "indécis" when separees is False, and otherwise names the
    # SMALLER series, the question one asks of latencies.
    # mesures_necessaires is None when the difference is zero, and otherwise
    # uses the LARGER of the two dispersions.
    if quantile == 0:
        raise ValueError()

    moyenne_a = estimation.moyenne(a)
    moyenne_b = estimation.moyenne(b)
    diff = comparaison.difference(a, b)
    bornes = comparaison.intervalle_difference(a, b, quantile)
    err = comparaison.erreur_type_difference(a, b)
    sep = comparaison.separees(a, b, quantile)
    rec = comparaison.separees_par_recouvrement(a, b)

    if not sep:
        verdict = VERDICTS[2]
    elif moyenne_a < moyenne_b:
        verdict = VERDICTS[0]
    else:
        verdict = VERDICTS[1]

    if diff == 0:
        mesures = None
    else:
        dispersion = max(estimation.ecart_type(a), estimation.ecart_type(b))
        mesures = mesures_pour_detecter(abs(diff), dispersion, quantile)

    return {
        "moyenne_a": moyenne_a,
        "moyenne_b": moyenne_b,
        "difference": diff,
        "intervalle": bornes,
        "erreur_type": err,
        "separees": sep,
        "verdict": verdict,
        "recouvrement": rec,
        "mesures_necessaires": mesures,
    }