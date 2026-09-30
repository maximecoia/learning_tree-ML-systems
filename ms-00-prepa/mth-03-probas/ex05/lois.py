"""mth-03-probas ex02: the laws and their expectations.

Statement:  ./exo mth-03-probas ex02
Grade:      ./exo mth-03-probas ex02 -c
Carry:      ./exo mth-03-probas ex02 -r    brings distribution.py, generateur.py
Allowed:    generateur ValueError len sum any abs zip range list all min max
            set int
"""

# Import from distribution and generateur what you need.
import generateur

def verifier_probabilite(p):
    # ValueError when p is not in [0, 1]. Public, because the next steps
    # need it.
    if p < 0 or p > 1:
        raise ValueError()


def combinaisons(n, k):
    # Without factorials. k > n gives 0, a negative argument raises
    # ValueError.
    if n < 0 or k < 0:
        raise ValueError()
    if k > n:
        return 0
    if k > n - k:
        k = n - k
    resultat = 1
    for i in range(1, k + 1):
        resultat = resultat * (n - k + i) // i
    return resultat


def loi_bernoulli(p):
    # A law in the sense of ex00.
    verifier_probabilite(p)
    if p == 0:
        return {0: 1.0}
    if p == 1:
        return {1: 1.0}
    return {0: 1 - p, 1: p}


def loi_binomiale(n, p):
    # A law in the sense of ex00.
    verifier_probabilite(p)
    loi = {}
    for k in range(n + 1):
        proba = combinaisons(n, k) * (p ** k) * ((1 - p) ** (n - k))
        if proba != 0:
            loi[k] = proba
    return loi


def esperance_binomiale(n, p):
    # The closed form.
    verifier_probabilite(p)
    return n * p



def esperance_geometrique(p):
    # The closed form. ValueError for p == 0: success never comes, the
    # expectation is infinite, and no number represents it.
    verifier_probabilite(p)
    if p == 0:
        raise ValueError()
    return 1 / p


def tirer_bernoulli(graine, combien, p):
    # 0s and 1s. Compare to p on the HIGH bits, by dividing the whole state
    # by MODULE.
    verifier_probabilite(p)
    uniformes = generateur.uniformes(graine, combien)
    return [1 if u < p else 0 for u in uniformes]


def tirer_geometrique(graine, combien, p):
    # The number of trials of each run. The first success counts: a run
    # that succeeds at once is worth 1, not 0.
    verifier_probabilite(p)
    if p == 0:
        raise ValueError()
    etat = graine
    resultats = []
    for _ in range(combien):
        essais = 0
        while True:
            etat = generateur.suivant(etat)
            u = etat / generateur.MODULE
            essais += 1
            if u < p:
                break
        resultats.append(essais)
    return resultats
