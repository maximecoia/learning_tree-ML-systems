from time import perf_counter

def mesurer(f, horloge=perf_counter):
    debut = horloge()
    f()
    fin = horloge()
    return fin - debut

def duree_lisible(secondes):
    if secondes < 0:
        raise ValueError("une duree ne peut pas etre negative")
    if secondes >= 1:
        valeur, unite = secondes, "s"
    elif secondes >= 1e-3:
        valeur, unite = secondes * 1e3, "ms"
    elif secondes >= 1e-6:
        valeur, unite = secondes * 1e6, "µs"
    else:
        valeur, unite = secondes * 1e9, "ns"
    return f"{valeur:.3f} {unite}"