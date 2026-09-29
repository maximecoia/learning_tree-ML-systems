"""maths-01-algebre ex01: matrices.

Statement:  ./exo maths-01-algebre ex01
Grade:      ./exo maths-01-algebre ex01 -c
Allowed:    isinstance iter len list range sum zip
"""

# --- carried over from ex00/vecteurs.py -------------------------------------
# Paste ErreurDeShape and Vecteur here. The grader checks them again.


class ErreurDeShape(ValueError):
    """Raised whenever two sizes do not fit together."""
    pass


class Vecteur:

    def __init__(self, nombres):
        self.nombres = list(nombres)

    def __repr__(self):
        return f"Vecteur({self.nombres})"

    def __eq__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        return self.nombres == other.nombres

    def __len__(self):
        return len(self.nombres)

    def __getitem__(self, index):
        return self.nombres[index]

    def __iter__(self):
        return iter(self.nombres)

    def __add__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a + b for a, b in zip(self.nombres, other.nombres)])

    def __sub__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a - b for a, b in zip(self.nombres, other.nombres)])

    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vecteur([x * scalar for x in self.nombres])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __matmul__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return sum(a * b for a, b in zip(self.nombres, other.nombres))


class Matrice:

    def __init__(self, lignes):
        self.lignes = [list(ligne) for ligne in lignes]
        
        if not self.lignes:
            raise ErreurDeShape
        if not self.lignes[0]:
            raise ErreurDeShape
            
        nb_colonnes = len(self.lignes[0])
        for ligne in self.lignes:
            if len(ligne) != nb_colonnes:
                raise ErreurDeShape

    def __repr__(self):
        return f"Matrice({self.lignes})"

    def __eq__(self, other):
        if not isinstance(other, Matrice):
            return NotImplemented
        return self.lignes == other.lignes

    def __getitem__(self, index):
        return Vecteur(self.lignes[index])

    @property
    def shape(self):
        return (len(self.lignes), len(self.lignes[0]))

    def colonnes(self):
        return [Vecteur(col) for col in zip(*self.lignes)]

    @classmethod
    def depuis_colonnes(cls, colonnes):
        if not colonnes:
            raise ErreurDeShape
            
        taille = len(colonnes[0])
        for v in colonnes:
            if len(v) != taille:
                raise ErreurDeShape
                
        return cls(zip(*colonnes))

    def __matmul__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
            
        if self.shape[1] != len(other):
            raise ErreurDeShape
            
        return Vecteur([Vecteur(ligne) @ other for ligne in self.lignes])