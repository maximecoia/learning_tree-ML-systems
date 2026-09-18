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