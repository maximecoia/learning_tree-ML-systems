"""mth-01-algebre ex00: vectors.

Statement:  ./exo mth-01-algebre ex00
Grade:      ./exo mth-01-algebre ex00 -c
Allowed:    isinstance iter len list sum zip
"""


class ErreurDeShape(ValueError):
    """Raised whenever two sizes do not fit together."""
    pass


class Vecteur:

    def __init__(self, nombres):
        # list() stores an independent copy: changing the caller's list later
        # does not change the vector.
        self.nombres = list(nombres)

    def __repr__(self):
        # A string of the form Vecteur([3, -1]).
        return f"Vecteur({self.nombres})"

    def __eq__(self, other):
        # Same numbers. NotImplemented for any other type.
        if not isinstance(other, Vecteur):
            return NotImplemented
        return self.nombres == other.nombres

    def __len__(self):
        # The size of the vector.
        return len(self.nombres)

    def __getitem__(self, index):
        # Element access through vecteur[i].
        return self.nombres[index]

    def __iter__(self):
        # Iteration, as in: for x in vecteur.
        return iter(self.nombres)

    def __add__(self, other):
        # A new Vecteur. ErreurDeShape when the sizes differ.
        # Check the type first: a list has a len() but no .nombres, which
        # would raise AttributeError instead of TypeError.
        if not isinstance(other, Vecteur):
            return NotImplemented
        
        if len(self) != len(other):
            raise ErreurDeShape
            
        return Vecteur([a + b for a, b in zip(self.nombres, other.nombres)])

    def __sub__(self, other):
        # A new Vecteur. ErreurDeShape when the sizes differ.
        if not isinstance(other, Vecteur):
            return NotImplemented
            
        if len(self) != len(other):
            raise ErreurDeShape
            
        return Vecteur([a - b for a, b in zip(self.nombres, other.nombres)])

    def __mul__(self, scalar):
        # int or float only. NotImplemented for anything else.
        if not isinstance(scalar, (int, float)):
            return NotImplemented
            
        return Vecteur([x * scalar for x in self.nombres])

    def __rmul__(self, scalar):
        # The scalar on the left, as in 3 * Vecteur(...). Scaling commutes,
        # so this delegates to __mul__.
        return self.__mul__(scalar)

    def __matmul__(self, other):
        # The dot product. ErreurDeShape when the sizes differ.
        if not isinstance(other, Vecteur):
            return NotImplemented
            
        if len(self) != len(other):
            raise ErreurDeShape
            
        # The dot product is the sum of the pairwise products.
        return sum(a * b for a, b in zip(self.nombres, other.nombres))