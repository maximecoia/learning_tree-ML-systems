"""mth-03-probas ex04: the square root and its cost.

Statement:  ./exo mth-03-probas ex04
Grade:      ./exo mth-03-probas ex04 -c
Carry:      ./exo mth-03-probas ex04 -r    brings distribution.py, generateur.py,
                                           lois.py, bayes.py
Allowed:    distribution ValueError len sum any abs zip range list all min max
            set int
"""

# Import from distribution what you need.


def moyenne(valeurs):
    # ValueError on an empty sample.
    ...


def ecart_type_echantillon(valeurs):
    # Through the empirical law of ex00. ValueError on an empty sample.
    ...


def erreur_type(ecart_type, combien):
    # sigma / sqrt(n). ValueError for zero measurements, and for a negative
    # standard deviation.
    ...


def mesures_pour(ecart_type, precision):
    # The number of measurements needed to reach this standard error,
    # ROUNDED UP. ValueError for a zero or negative precision.
    ...


def paquets(valeurs, taille):
    # Batches of this size, the incomplete remainder dropped. ValueError for
    # a zero or negative size.
    ...
