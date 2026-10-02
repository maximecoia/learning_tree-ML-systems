def mediane(valeurs):
    triees = sorted(valeurs)
    n = len(triees)
    if n == 0:
        raise ValueError("une liste vide n'a pas de mediane")
    mileu = n // 2
    if n % 2 == 1:
        return triees[mileu]
    return (triees[mileu - 1] + triees[mileu]) / 2

def resumer(durees):
    if len(durees) == 0:
        raise ValueError("une liste vide ne peut pas etre resumee")
    return {
        'n': len(durees),
        'min': min(durees),
        'mediane': mediane(durees),
        'moyenne': sum(durees) / len(durees),
        'ecart': max(durees) - min(durees),
    }