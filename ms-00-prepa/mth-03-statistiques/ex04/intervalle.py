"""mth-03-statistiques ex01: the confidence interval.

Statement:  ./exo mth-03-statistiques ex01
Grade:      ./exo mth-03-statistiques ex01 -c
Carry:      ./exo mth-03-statistiques ex01 -r    brings estimation.py from ex00
Allowed:    estimation ValueError len sum
"""

# Import from estimation what you need.
import estimation

# Dictated by the statement, as is.
QUANTILES_NORMAUX = {
    0.90: 1.6448536269514722,
    0.95: 1.959963984540054,
    0.99: 2.5758293035489004,
}
QUANTILES_STUDENT_95 = {
    2: 12.706204736174698,
    3: 4.302652729749464,
    5: 2.7764451051977987,
    10: 2.262157162798205,
    30: 2.045229642132703,
}


def erreur_type(echantillon):
    # The standard deviation divided by sqrt(n).
    return estimation.ecart_type(echantillon) / (len(echantillon) ** 0.5)


def intervalle(echantillon, quantile):
    # The pair of bounds: the mean plus or minus quantile times the standard
    # error. ValueError for a zero or negative quantile.
    if quantile <= 0:
        raise ValueError()
    m = estimation.moyenne(echantillon)
    e = erreur_type(echantillon)
    return (m - quantile * e, m + quantile * e)


def contient(bornes, valeur):
    # Bounds included. ValueError for a reversed pair.
    inf, sup = bornes
    if inf > sup:
        raise ValueError()
    return inf <= valeur <= sup


def largeur(bornes):
    # ValueError for a reversed pair.
    inf, sup = bornes
    if inf > sup:
        raise ValueError()
    return sup - inf


def couverture(intervalles, vraie):
    # The PROPORTION of intervals that contain the value. ValueError on an
    # empty list.
    if len(intervalles) == 0:
        raise ValueError()
    return sum(1 for b in intervalles if contient(b, vraie)) / len(intervalles)