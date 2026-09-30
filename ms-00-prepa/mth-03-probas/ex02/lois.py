"""mth-03-probas ex02: the laws and their expectations.

Statement:  ./exo mth-03-probas ex02
Grade:      ./exo mth-03-probas ex02 -c
Carry:      ./exo mth-03-probas ex02 -r    brings distribution.py, generateur.py
Allowed:    generateur ValueError len sum any abs zip range list all min max
            set int
"""

# Import from distribution and generateur what you need.


def verifier_probabilite(p):
    # ValueError when p is not in [0, 1]. Public, because the next steps
    # need it.
    ...


def combinaisons(n, k):
    # Without factorials. k > n gives 0, a negative argument raises
    # ValueError.
    ...


def loi_bernoulli(p):
    # A law in the sense of ex00.
    ...


def loi_binomiale(n, p):
    # A law in the sense of ex00.
    ...


def esperance_binomiale(n, p):
    # The closed form.
    ...


def esperance_geometrique(p):
    # The closed form. ValueError for p == 0: success never comes, the
    # expectation is infinite, and no number represents it.
    ...


def tirer_bernoulli(graine, combien, p):
    # 0s and 1s. Compare to p on the HIGH bits, by dividing the whole state
    # by MODULE.
    ...


def tirer_geometrique(graine, combien, p):
    # The number of trials of each run. The first success counts: a run
    # that succeeds at once is worth 1, not 0.
    ...
