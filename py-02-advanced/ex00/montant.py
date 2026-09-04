class Montant:
    def __init__(self, centimes):
        if not isinstance(centimes, int) or centimes < 0:
            raise ValueError("montant invalide")
        self.centimes = centimes

    def en_euros(self):
        return self.centimes / 100

    def ajouter(self, autre):
        return Montant(self.centimes + autre.centimes)

    def fois(self, n):
        return Montant(self.centimes * n)


print(Montant(1250).centimes)
print(Montant(0).centimes)
print(Montant(1250).en_euros())
print(Montant(1250).ajouter(Montant(300)).centimes)
print(Montant(120).fois(3).centimes)
print(Montant(-1))
print(Montant(12.5))
print(Montant("12"))