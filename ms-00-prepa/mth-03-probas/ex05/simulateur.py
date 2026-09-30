"""mth-03-probas ex05: a simulator that checks itself.

Statement:  ./exo mth-03-probas ex05
Grade:      ./exo mth-03-probas ex05 -c
Carry:      ./exo mth-03-probas ex05 -r    brings distribution.py, generateur.py,
                                           lois.py, bayes.py, convergence.py
Allowed:    generateur lois convergence ValueError len sum any abs zip range
            list all min max set int
"""

# Import from convergence, generateur and lois what you need.

# Dictated by the statement.
LOIS = ("bernoulli", "binomiale", "geometrique")


def tirer_binomiale(graine, combien, essais, p):
    # Each draw is the sum of `essais` Bernoulli trials. Do not build the
    # law to draw from it: stack the trials, which IS the definition of a
    # binomial. ValueError for a negative number of trials.
    ...


def verifier_loi(tirages, esperance_theorique, ecart_type_theorique, ecarts=5):
    # A dict with combien, esperance_simulee, esperance_theorique, ecart,
    # borne and accorde. borne is `ecarts` times the standard error, and
    # accorde is True when ecart is strictly below borne. ValueError for no
    # draw, a negative standard deviation or a zero margin.
    ...


def confronter(graine, combien, p=0.2, essais=10):
    # One report per law, under the keys bernoulli, binomiale and
    # geometrique. ValueError for a zero probability.
    ...
