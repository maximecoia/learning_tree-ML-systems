"""maths-01-algebre ex06: the norm and the projection.

Statement:  ./exo maths-01-algebre ex06
Grade:      ./exo maths-01-algebre ex06 -c
Allowed:    isinstance iter len list sum zip all float ValueError
"""

# --- carried over from ex00/vecteurs.py -------------------------------------
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

    # --- new in ex06 ---------------------------------------------------------

    @property
    def norme(self):
        # The Euclidean norm is the square root of the sum of squares
        return float(sum(x ** 2 for x in self.nombres) ** 0.5)

    def distance(self, autre):
        # The distance between two points is the norm of their difference
        return (self - autre).norme

    def est_orthogonal(self, autre):
        # Two vectors are orthogonal if their dot product is zero
        return (self @ autre) == 0

    def projeter_sur(self, u):
        # Check if u is the zero vector (cannot project on it)
        if all(x == 0 for x in u):
            raise ValueError
            
        # Projection formula: proj_u(v) = ((v . u) / (u . u)) * u
        coeff = (self @ u) / (u @ u)
        return u * coeff
