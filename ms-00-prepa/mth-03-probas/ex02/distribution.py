"""mth-03-probas ex00: the distribution and its variance.

Statement:  ./exo mth-03-probas ex00
Grade:      ./exo mth-03-probas ex00 -c
Allowed:    ValueError len sum any abs
"""


def compter(valeurs):
    # Each value to its number of occurrences. The values need not be
    # numbers. ValueError on an empty sample.
    if len(valeurs) == 0:
        raise ValueError()
    occurrences = {}
    for valeur in valeurs:
        if valeur in occurrences:
            occurrences[valeur] += 1
        else:
            occurrences[valeur] = 1
    return occurrences


def frequences(valeurs):
    # The empirical law: each value to its proportion. They sum to 1.
    occurrences = compter(valeurs)
    n = len(valeurs)
    return {valeur: occurrences[valeur] / n for valeur in occurrences}


# The four functions below raise ValueError on an empty law, on a law whose
# probabilities do not sum to 1 within 1e-9, and on a law that carries a
# negative probability.

def _verifier_loi(loi):
    if len(loi) == 0:
        raise ValueError("empty law")
    if any(p < 0 for p in loi.values()):
        raise ValueError("negative probability")
    total = sum(loi.values())
    if abs(total - 1) > 1e-9:
        raise ValueError("sum != 1")


def esperance(loi):
    # The weighted mean of the values.
    _verifier_loi(loi)
    return sum(valeur * p for valeur, p in loi.items())


def variance(loi):
    # The mean squared deviation from the expectation, in TWO passes.
    _verifier_loi(loi)
    moyenne = sum(valeur * p for valeur, p in loi.items())
    return sum(p * (valeur - moyenne) ** 2 for valeur, p in loi.items())


def variance_naive(loi):
    # The same through E[X^2] - E[X]^2. Not meant for use: it is here to
    # show what it returns.
    _verifier_loi(loi)
    moyenne = sum(valeur * p for valeur, p in loi.items())
    moyenne_des_carres = sum(p * (valeur ** 2) for valeur, p in loi.items())
    return moyenne_des_carres - moyenne ** 2


def ecart_type(loi):
    # The square root of the variance.
    return variance(loi) ** 0.5