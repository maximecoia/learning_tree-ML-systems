"""mth-03-probas ex03: turning a conditional around.

Statement:  ./exo mth-03-probas ex03
Grade:      ./exo mth-03-probas ex03 -c
Carry:      ./exo mth-03-probas ex03 -r    brings distribution.py, generateur.py,
                                           lois.py
Allowed:    generateur lois ValueError len sum any abs zip range list all min
            max set int
"""

# Import from generateur and lois what you need.


def conditionnelle(p_conjointe, p_condition):
    # ValueError when conditioning on an impossible event, and when the
    # intersection is larger than the condition.
    ...


def totales(p_b_si_a, p_a, p_b_si_non_a):
    # The law of total probability.
    ...


def bayes(p_b_si_a, p_a, p_b_si_non_a):
    # P(A | B).
    ...


def valeur_predictive(prevalence, sensibilite, specificite):
    # The probability of being ill given that the test is positive.
    ...


def independants(p_a, p_b, p_conjointe, tolerance=1e-12):
    ...


def simuler_depistage(graine, combien, prevalence, sensibilite, specificite):
    # The pair (positifs, malades_parmi_les_positifs). Count the ill people
    # WHO TEST POSITIVE, not all the ill people.
    ...
