"""mth-03-probas ex03: turning a conditional around.

Statement:  ./exo mth-03-probas ex03
Grade:      ./exo mth-03-probas ex03 -c
Carry:      ./exo mth-03-probas ex03 -r    brings distribution.py, generateur.py,
                                           lois.py
Allowed:    generateur lois ValueError len sum any abs zip range list all min
            max set int
"""

import generateur
import lois


def conditionnelle(p_conjointe, p_condition):
    # ValueError when conditioning on an impossible event, and when the
    # intersection is larger than the condition.
    lois.verifier_probabilite(p_conjointe)
    lois.verifier_probabilite(p_condition)
    if p_condition == 0:
        raise ValueError()
    if p_conjointe > p_condition:
        raise ValueError()
    return p_conjointe / p_condition


def totales(p_b_si_a, p_a, p_b_si_non_a):
    # The law of total probability.
    lois.verifier_probabilite(p_b_si_a)
    lois.verifier_probabilite(p_a)
    lois.verifier_probabilite(p_b_si_non_a)
    return p_b_si_a * p_a + p_b_si_non_a * (1 - p_a)


def bayes(p_b_si_a, p_a, p_b_si_non_a):
    # P(A | B).
    p_b = totales(p_b_si_a, p_a, p_b_si_non_a)
    return conditionnelle(p_b_si_a * p_a, p_b)


def valeur_predictive(prevalence, sensibilite, specificite):
    # The probability of being ill given that the test is positive.
    lois.verifier_probabilite(prevalence)
    lois.verifier_probabilite(sensibilite)
    lois.verifier_probabilite(specificite)
    return bayes(sensibilite, prevalence, 1 - specificite)


def independants(p_a, p_b, p_conjointe, tolerance=1e-12):
    lois.verifier_probabilite(p_a)
    lois.verifier_probabilite(p_b)
    lois.verifier_probabilite(p_conjointe)
    if tolerance <= 0:
        raise ValueError()
    return abs(p_conjointe - p_a * p_b) <= tolerance


def simuler_depistage(graine, combien, prevalence, sensibilite, specificite):
    # The pair (positifs, malades_parmi_les_positifs). Count the ill people
    # WHO TEST POSITIVE, not all the ill people.
    lois.verifier_probabilite(prevalence)
    lois.verifier_probabilite(sensibilite)
    lois.verifier_probabilite(specificite)
    uniformes = generateur.uniformes(graine, 2 * combien)
    positifs = 0
    malades_parmi_positifs = 0
    for i in range(combien):
        u_ill = uniformes[2 * i]
        u_test = uniformes[2 * i + 1]
        if u_ill < prevalence:
            if u_test < sensibilite:
                positifs += 1
                malades_parmi_positifs += 1
        else:
            if u_test < 1 - specificite:
                positifs += 1
    return (positifs, malades_parmi_positifs)