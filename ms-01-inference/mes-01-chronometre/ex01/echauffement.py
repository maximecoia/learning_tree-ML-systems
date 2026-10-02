from time import perf_counter
from chrono import mesurer

def mesurer_plusieurs(f, repetitions=5, echauffement=1, horloge=perf_counter):
    if repetitions < 1:
        raise ValueError("il faut au moins une repetition")
    if echauffement < 0:
        raise ValueError("l'echauffement ne peut pas etre negatif")
    for _ in range(echauffement):
        f()
    durees = []
    for _ in range(repetitions):
        durees.append(mesurer(f, horloge))
    return durees