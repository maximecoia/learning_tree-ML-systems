def saluer(nom, politesse="bonjour"):
    return politesse + " " + nom


def min_et_max(valeurs):
    if not valeurs:
        return None
    return min(valeurs), max(valeurs)


def bornees(valeurs, minimum=0, maximum=20):
    return [v for v in valeurs if minimum <= v <= maximum]

print(saluer("alice"))
print(saluer("bob", politesse="bonsoir"))
print(min_et_max([3, 9, 1]))
print(min_et_max([]))
print(bornees([-1, 0, 10, 20, 21]))
print(bornees([-1, 0, 10, 20, 21], 5, 15))
print(bornees([-1, 0, 10, 20, 21], maximum=10))