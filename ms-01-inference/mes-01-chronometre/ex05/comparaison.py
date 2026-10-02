from time import perf_counter

from chrono import mesurer
from bruit import resumer

def comparer(a, b, repetitions=5, echauffement=1, horloge=perf_counter):
    if repetitions < 1:
        raise ValueError("il faut au moins une repetition")
    if echauffement < 0:
        raise ValueError("l'echauffement ne peut pas etre negatif")
    for _ in range(echauffement):
        a()
        b()
    mesures_a = []
    mesures_b = []
    for _ in range(repetitions):
        mesures_a.append(mesurer(a, horloge))
        mesures_b.append(mesurer(b, horloge))
    resume_a = resumer(mesures_a)
    if resume_a['min'] <= 0:
        raise ValueError("un minimum nul ou negatif ne permet pas de rapport")
    resume_b = resumer(mesures_b)
    separees = max(mesures_a) < min(mesures_b) or max(mesures_b) < min(mesures_a)
    return {
        'a': resume_a,
        'b': resume_b,
        'rapport': resume_b['min'] / resume_a['min'],
        'incertain': not separees,
    }