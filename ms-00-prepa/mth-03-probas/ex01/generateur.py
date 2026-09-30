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
    ...


def suite(graine, combien):
    # The `combien` states that FOLLOW the seed: the seed is not one of
    # them. ValueError for a negative count.
    ...


def uniformes(graine, combien):
    # The same states, brought into [0, 1[.
    ...


def bits(etats, rang):
    # The bit of this rank in each state, rank 0 being the lowest.
    # ValueError for a rank outside [0, RANG_MAXIMAL].
    ...


def series(valeurs):
    # The lengths of the runs of identical values that follow each other.
    # ValueError on an empty sequence.
    ...
