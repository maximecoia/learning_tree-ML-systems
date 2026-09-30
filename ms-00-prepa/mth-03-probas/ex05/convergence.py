"""mth-03-probas ex04: the root and its cost.

Statement:  ./exo mth-03-probas ex04
Grade:      ./exo mth-03-probas ex04 -c
Carry:      ./exo mth-03-probas ex04 -r    brings distribution.py, generateur.py,
                                           lois.py, bayes.py
Allowed:    distribution ValueError len sum any abs zip range list all min
            max set int
"""

import distribution


def moyenne(valeurs):
    # ValueError on an empty sample.
    if len(valeurs) == 0:
        raise ValueError()
    return sum(valeurs) / len(valeurs)


def ecart_type_echantillon(valeurs):
    # Through the empirical law of ex00. ValueError on an empty sample.
    if len(valeurs) == 0:
        raise ValueError()
    loi = distribution.frequences(valeurs)
    return distribution.ecart_type(loi)


def erreur_type(ecart_type, combien):
    # sigma / sqrt(n). ValueError for zero measurements and for a negative
    # standard deviation.
    if combien <= 0:
        raise ValueError()
    if ecart_type < 0:
        raise ValueError()
    return ecart_type / combien ** 0.5


def mesures_pour(ecart_type, precision):
    # The number of measurements needed to reach this standard error,
    # ROUNDED UP. A zero or negative precision raises ValueError.
    if precision <= 0:
        raise ValueError()
    if ecart_type < 0:
        raise ValueError()
    n = (ecart_type / precision) ** 2
    entier = int(n)
    # A float can land a hair above a whole count: (0.07 / 0.01) ** 2 is
    # 49.000000000000014, and a strict ceiling would pay for 50 measurements.
    # Only a real fraction moves up. The tolerance is relative, because the
    # rounding noise grows with the count itself.
    if n - entier > n * 1e-12:
        return entier + 1
    return entier


def paquets(valeurs, taille):
    # Splits into packets of this size and throws away the incomplete rest.
    # A zero or negative size raises ValueError.
    if taille <= 0:
        raise ValueError()
    return [valeurs[i:i + taille] for i in range(0, len(valeurs) - len(valeurs) % taille, taille)]