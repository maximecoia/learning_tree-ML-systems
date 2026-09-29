"""maths-01-algebre ex00: vectors.

Statement:  ./exo maths-01-algebre ex00
Grade:      ./exo maths-01-algebre ex00 -c
Allowed:    isinstance iter len list sum zip
"""


class ErreurDeShape(ValueError):
    """Raised whenever two sizes do not fit together."""
    pass


class Vecteur:

    def __init__(self, nombres):
        # Store a copy of the list in self.nombres.
        # On utilise list() pour créer une copie superficielle de la liste reçue.
        self.nombres = list(nombres)

    def __repr__(self):
        # Vecteur([3, -1])
        return f"Vecteur({self.nombres})"

    def __eq__(self, other):
        # Same numbers. NotImplemented for any other type.
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
        # A new Vecteur. ErreurDeShape when the sizes differ.
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a + b for a, b in zip(self.nombres, other.nombres)])

    def __sub__(self, other):
        # A new Vecteur. ErreurDeShape when the sizes differ.
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a - b for a, b in zip(self.nombres, other.nombres)])

    def __mul__(self, scalar):
        # int or float only. NotImplemented for anything else.
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vecteur([x * scalar for x in self.nombres])

    def __rmul__(self, scalar):
        # La multiplication est commutative, on peut réutiliser __mul__
        return self.__mul__(scalar)

    def __matmul__(self, other):
        # The dot product. ErreurDeShape when the sizes differ.
        if len(self) != len(other):
            raise ErreurDeShape
        return sum(a * b for a, b in zip(self.nombres, other.nombres))