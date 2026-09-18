def retenues(notes, minimum):
    return [note for note in notes if note >= minimum]


def moyenne(notes):
    if not notes:
        return None
    return round(sum(notes) / len(notes), 2)


def au_carre(notes):
    return [note ** 2 for note in notes]


def decroissantes(notes):
    return sorted(notes, reverse=True)


print(retenues([14, 9, 17], 10))
print(retenues([], 10))
print(moyenne([14, 17]))
print(moyenne([10, 11, 11]))
print(moyenne([]))
print(au_carre([1, 2, 3]))
print(decroissantes([3, 9, 1]))