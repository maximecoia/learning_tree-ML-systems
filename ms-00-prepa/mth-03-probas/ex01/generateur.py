"""mth-03-probas ex01: the generator and its flaws.

Statement:  ./exo mth-03-probas ex01
Grade:      ./exo mth-03-probas ex01 -c
Carry:      ./exo mth-03-probas ex01 -r    brings distribution.py from ex00
Allowed:    ValueError len sum any abs zip range list all
"""

# Dictated by the statement.
FACTEUR = 1103515245
INCREMENT = 12345
MODULE = 2 ** 31
RANG_MAXIMAL = 30


def suivant(etat):
    # The next state. ValueError for a state outside [0, MODULE[.
    if etat < 0 or etat >= MODULE:
        raise ValueError()
    return (FACTEUR * etat + INCREMENT) % MODULE


def suite(graine, combien):
    # The `combien` states that FOLLOW the seed: the seed is not one of
    # them. ValueError for a negative count.
    if combien < 0:
        raise ValueError()
    etats = []
    etat = graine
    for _ in range(combien):
        etat = suivant(etat)
        etats.append(etat)
    return etats


def uniformes(graine, combien):
    # The same states, brought into [0, 1[.
    return [etat / MODULE for etat in suite(graine, combien)]


def bits(etats, rang):
    # The bit of this rank in each state, rank 0 being the lowest.
    # ValueError for a rank outside [0, RANG_MAXIMAL].
    if rang < 0 or rang > RANG_MAXIMAL:
        raise ValueError()
    return [(etat >> rang) & 1 for etat in etats]


def series(valeurs):
    # The lengths of the runs of identical values that follow each other.
    # ValueError on an empty sequence.
    if len(valeurs) == 0:
        raise ValueError()
    longueurs = []
    longueur = 1
    for i in range(1, len(valeurs)):
        if valeurs[i] == valeurs[i - 1]:
            longueur += 1
        else:
            longueurs.append(longueur)
            longueur = 1
    longueurs.append(longueur)
    return longueurs