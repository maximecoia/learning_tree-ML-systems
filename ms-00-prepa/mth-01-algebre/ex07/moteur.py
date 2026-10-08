"""mth-01-algebre ex07: the 2D transformation engine.

Statement:  ./exo mth-01-algebre ex07
Grade:      ./exo mth-01-algebre ex07 -c
Allowed:    isinstance iter len list range sum zip abs all float ValueError
"""

# --- carried over -----------------------------------------------------------
# Paste ErreurDeShape here, and Vecteur with norme from ex06/projection.py.


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

    @property
    def norme(self):
        # The Euclidean norm is the square root of the sum of squares
        return float(sum(x ** 2 for x in self.nombres) ** 0.5)

    def distance(self, autre):
        # The distance between two points is the norm of their difference
        return (self - autre).norme

    def est_orthogonal(self, autre):
        # Two vectors are orthogonal if their dot product is zero, up to the
        # rounding of floats: the residual of a projection is orthogonal by
        # construction, yet its dot product can read 4.44e-16. The tolerance
        # scales with both lengths, so the test reads the angle and not the
        # size, and the zero vector, of length 0, stays orthogonal to all.
        # The dot product comes first: it is what refuses a size mismatch.
        produit = self @ autre
        seuil = 1e-9 * self.norme * autre.norme
        return -seuil <= produit <= seuil

    def projeter_sur(self, u):
        # Check if u is the zero vector (cannot project on it)
        if all(x == 0 for x in u):
            raise ValueError
            
        # Projection formula: proj_u(v) = ((v . u) / (u . u)) * u
        coeff = (self @ u) / (u @ u)
        return u * coeff


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
        if isinstance(other, Vecteur):
            if self.shape[1] != len(other):
                raise ErreurDeShape
            return Vecteur([Vecteur(ligne) @ other for ligne in self.lignes])
            
        if isinstance(other, Matrice):
            if self.shape[1] != other.shape[0]:
                raise ErreurDeShape
                
            colonnes_other = other.colonnes()
            nouvelles_lignes = []
            for ligne in self.lignes:
                v_ligne = Vecteur(ligne)
                nouvelle_ligne = [v_ligne @ col for col in colonnes_other]
                nouvelles_lignes.append(nouvelle_ligne)
                
            return Matrice(nouvelles_lignes)
            
        return NotImplemented

    @classmethod
    def identite(cls, n):
        return cls([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    def puis(self, suivante):
        return suivante @ self

    @property
    def det(self):
        if self.shape != (2, 2):
            raise ErreurDeShape
        
        a = self.lignes[0][0]
        b = self.lignes[0][1]
        c = self.lignes[1][0]
        d = self.lignes[1][1]
        
        return a * d - b * c

    @property
    def facteur_aire(self):
        return abs(self.det)

    @property
    def renverse_orientation(self):
        return self.det < 0

    @property
    def est_singuliere(self):
        return self.det == 0

    def inverse(self):
        det_val = self.det
        
        if det_val == 0:
            raise ValueError
            
        a = self.lignes[0][0]
        b = self.lignes[0][1]
        c = self.lignes[1][0]
        d = self.lignes[1][1]
        
        return Matrice([
            [d / det_val, -b / det_val],
            [-c / det_val, a / det_val]
        ])

    def resoudre(self, b):
        return self.inverse() @ b

    @property
    def rang(self):
        if all(x == 0 for ligne in self.lignes for x in ligne):
            return 0
            
        if self.det == 0:
            return 1
            
        return 2

    @property
    def dim_noyau(self):
        return 2 - self.rang

    @property
    def trace(self):
        if self.shape[0] != self.shape[1]:
            raise ErreurDeShape
            
        return sum(self.lignes[i][i] for i in range(self.shape[0]))

    def valeur_propre(self, v):
        if all(x == 0 for x in v):
            raise ValueError
            
        av = self @ v
        
        lam = None
        for i in range(len(v)):
            if v[i] != 0:
                lam = av[i] / v[i]
                break
                
        for i in range(len(v)):
            if av[i] != lam * v[i]:
                return None
                
        return float(lam)

    def valeurs_propres(self):
        if self.shape != (2, 2):
            raise ErreurDeShape
            
        t = self.trace
        d = self.det
        
        delta = t ** 2 - 4 * d
        
        if delta < 0:
            return []
            
        if delta == 0:
            val = float(t / 2)
            return [val, val]
            
        racine = delta ** 0.5
        l1 = float((t + racine) / 2)
        l2 = float((t - racine) / 2)
        
        # CORRECTION HERE: Manual sort instead of sorted()
        if l1 <= l2:
            return [l1, l2]
        return [l2, l1]

    # --- NEW in ex07 ---------------------------------------------------------

    @classmethod
    def rotation90(cls):
        # The quarter turn matrix
        return cls([[0, -1], [1, 0]])

    @classmethod
    def echelle(cls, sx, sy):
        # The scaling matrix by sx along x and sy along y
        return cls([[sx, 0], [0, sy]])

    @classmethod
    def cisaillement_x(cls, k):
        # The horizontal shear matrix
        return cls([[1, k], [0, 1]])

    @classmethod
    def enchainer(cls, matrices):
        # Apply the matrices in order, the first one first.
        # If the list is empty, return the 2x2 identity.
        if not matrices:
            return cls.identite(2)
            
        res = matrices[0]
        for m in matrices[1:]:
            res = m @ res
        return res


class Polygone:

    def __init__(self, sommets):
        # Store a copy of the list of Vecteur in self.sommets
        self.sommets = list(sommets)

    def __repr__(self):
        return f"Polygone({self.sommets})"

    def __eq__(self, other):
        if not isinstance(other, Polygone):
            return NotImplemented
        return self.sommets == other.sommets

    def __len__(self):
        return len(self.sommets)

    def __iter__(self):
        return iter(self.sommets)

    def transformer(self, matrice):
        # Return the polygon of the transformed vertices
        return Polygone([matrice @ v for v in self.sommets])

    @property
    def aire(self):
        # The area as a float, by the shoelace formula. 0.0 below three vertices.
        if len(self.sommets) < 3:
            return 0.0
            
        # Append the first point at the end to close the polygon
        points = self.sommets + [self.sommets[0]]
        
        # Shoelace formula: sum(x_i * y_{i+1} - x_{i+1} * y_i) / 2
        total = sum(p1[0] * p2[1] - p2[0] * p1[1] for p1, p2 in zip(points, points[1:]))
        
        return float(abs(total) / 2)