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

    def __repr__(self):
        return f"Montant({self.centimes})"

    def texte(self):
        euros = self.centimes // 100
        centimes = self.centimes % 100
        return f"{euros},{centimes:02d} €"

    def __eq__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return self.centimes == autre.centimes

    def __lt__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return self.centimes < autre.centimes

    def tries(montants):
        return sorted(montants)

    def le_plus_grand(montants):
        if not montants:
            return None
        return max(montants)