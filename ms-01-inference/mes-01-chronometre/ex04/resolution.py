from time import perf_counter
from math import ceil

def resolution(horloge=perf_counter, essais=100):
    if essais < 2:
        raise ValueError("un ecart se prend entre deux lectures")
    lectures = [horloge() for _ in range(essais)]
    ecarts = [b - a for a, b in zip(lectures, lectures[1:])]
    non_nuls = [e for e in ecarts if e != 0]
    if len(non_nuls) == 0:
        raise ValueError("tous les ecarts sont nuls")
    return min(non_nuls)

def lots_necessaires(duree_appel, resolution, facteur=100):
    if duree_appel <= 0:
        raise ValueError("la duree d'appel doit etre positive")
    if resolution <= 0:
        raise ValueError("la resolution doit etre positive")
    if facteur < 1:
        raise ValueError("le facteur doit valoir au moins 1")
    return ceil(facteur * resolution / duree_appel)
