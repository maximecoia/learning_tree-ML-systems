"""mth-04-statistiques ex00: the estimator and its bias.

Statement:  ./exo mth-04-statistiques ex00
Grade:      ./exo mth-04-statistiques ex00 -c
Allowed:    ValueError len sum

The functions of this module ANALYSE samples, they do not produce them: the
caller draws.
"""


def moyenne(echantillon):
    # ValueError on an empty sample.
    if len(echantillon) == 0:
        raise ValueError()
    return sum(echantillon) / len(echantillon)


def variance_biaisee(echantillon):
    # The sum of squared deviations from the mean, divided by n. It answers
    # even on a single measurement.
    if len(echantillon) == 0:
        raise ValueError()
    m = moyenne(echantillon)
    return sum((x - m) ** 2 for x in echantillon) / len(echantillon)


def variance_corrigee(echantillon):
    # The same sum divided by n - 1. ValueError below two measurements.
    if len(echantillon) < 2:
        raise ValueError()
    m = moyenne(echantillon)
    return sum((x - m) ** 2 for x in echantillon) / (len(echantillon) - 1)


def ecart_type(echantillon):
    # The square root of the CORRECTED variance.
    return variance_corrigee(echantillon) ** 0.5


def facteur_de_biais(taille):
    # (n - 1) / n. ValueError for a size below 1.
    if taille < 1:
        raise ValueError()
    return (taille - 1) / taille