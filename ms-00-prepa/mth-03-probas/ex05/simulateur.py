"""mth-03-probas ex05: a simulator that checks itself.

Statement:  ./exo mth-03-probas ex05
Grade:      ./exo mth-03-probas ex05 -c
Carry:      ./exo mth-03-probas ex05 -r    brings distribution.py, generateur.py,
                                           lois.py, bayes.py, convergence.py
Allowed:    generateur lois convergence ValueError len sum any abs zip range
            list all min max set int
"""

import generateur
import lois
import convergence

# Dictated by the statement.
LOIS = ("bernoulli", "binomiale", "geometrique")


def tirer_binomiale(graine, combien, essais, p):
    # Each draw is the sum of `essais` Bernoulli trials. Do not build the
    # law to draw from it: stack the trials, which IS the definition of a
    # binomial. ValueError for a negative number of trials.
    if essais < 0:
        raise ValueError()
    tirages_bernoulli = lois.tirer_bernoulli(graine, combien * essais, p)
    resultats = []
    for i in range(combien):
        resultats.append(sum(tirages_bernoulli[i * essais:(i + 1) * essais]))
    return resultats


def verifier_loi(tirages, esperance_theorique, ecart_type_theorique, ecarts=5):
    # A dict with combien, esperance_simulee, esperance_theorique, ecart,
    # borne and accorde. borne is `ecarts` times the standard error, and
    # accorde is True when ecart is strictly below borne. ValueError for no
    # draw, a negative standard deviation or a zero margin.
    if len(tirages) == 0:
        raise ValueError()
    if ecart_type_theorique < 0:
        raise ValueError()
    if ecarts <= 0:
        raise ValueError()
    combien = len(tirages)
    esperance_simulee = convergence.moyenne(tirages)
    ecart = abs(esperance_simulee - esperance_theorique)
    erreur = convergence.erreur_type(ecart_type_theorique, combien)
    borne = ecarts * erreur
    accorde = ecart < borne
    return {
        "combien": combien,
        "esperance_simulee": esperance_simulee,
        "esperance_theorique": esperance_theorique,
        "ecart": ecart,
        "borne": borne,
        "accorde": accorde,
    }


def confronter(graine, combien, p=0.2, essais=10):
    # One report per law, under the keys bernoulli, binomiale and
    # geometrique. ValueError for a zero probability.
    if p == 0:
        raise ValueError()
    lois.verifier_probabilite(p)

    # Theoretical values
    esp_b = p
    var_b = p * (1 - p)
    std_b = var_b ** 0.5

    esp_bin = essais * p
    var_bin = essais * p * (1 - p)
    std_bin = var_bin ** 0.5

    esp_geo = 1 / p
    var_geo = (1 - p) / (p ** 2)
    std_geo = var_geo ** 0.5

    # Simulations
    tirages_b = lois.tirer_bernoulli(graine, combien, p)
    tirages_bin = tirer_binomiale(graine, combien, essais, p)
    tirages_geo = lois.tirer_geometrique(graine, combien, p)

    return {
        "bernoulli": verifier_loi(tirages_b, esp_b, std_b),
        "binomiale": verifier_loi(tirages_bin, esp_bin, std_bin),
        "geometrique": verifier_loi(tirages_geo, esp_geo, std_geo),
    }