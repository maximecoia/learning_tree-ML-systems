"""mth-03-probas ex00: the distribution and its variance.

Statement:  ./exo mth-03-probas ex00
Grade:      ./exo mth-03-probas ex00 -c
Allowed:    ValueError len sum any abs
"""


def compter(valeurs):
    # Each value to its number of occurrences. The values need not be
    # numbers. ValueError on an empty sample.
    ...


def frequences(valeurs):
    # The empirical law: each value to its proportion. They sum to 1.
    ...


# The four functions below raise ValueError on an empty law, on a law whose
# probabilities do not sum to 1 within 1e-9, and on a law that carries a
# negative probability.

def esperance(loi):
    # The weighted mean of the values.
    ...


def variance(loi):
    # The mean squared deviation from the expectation, in TWO passes.
    ...


def variance_naive(loi):
    # The same through E[X^2] - E[X]^2. Not meant for use: it is here to
    # show what it returns.
    ...


def ecart_type(loi):
    # The square root of the variance.
    ...
