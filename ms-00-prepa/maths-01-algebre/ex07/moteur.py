"""maths-01-algebre ex07: the 2D transformation engine.

Statement:  ./exo maths-01-algebre ex07
Grade:      ./exo maths-01-algebre ex07 -c
Allowed:    isinstance iter len list range sum zip abs all float ValueError
"""

# --- carried over -----------------------------------------------------------
# Paste ErreurDeShape here, and Vecteur with norme from ex06/projection.py.


class Matrice:
    # --- carried over from ex05/propres.py ----------------------------------
    # Paste the body of Matrice here. The grader checks identite, the matrix
    # product, det and facteur_aire again.

    # --- new in ex07 ---------------------------------------------------------
    @classmethod
    def rotation90(cls):
        # The quarter turn.
        ...

    @classmethod
    def echelle(cls, sx, sy):
        # The scaling by sx along x and sy along y.
        ...

    @classmethod
    def cisaillement_x(cls, k):
        # The horizontal shear.
        ...

    @classmethod
    def enchainer(cls, matrices):
        # The matrix applying the list in order, the first one first.
        # The 2x2 identity for an empty list.
        ...


class Polygone:

    def __init__(self, sommets):
        # Store a copy of the list of Vecteur in self.sommets.
        ...

    def __repr__(self):
        # Polygone([Vecteur([0, 0]), Vecteur([4, 0])])
        ...

    def __eq__(self, other):
        ...

    def __len__(self):
        ...

    def __iter__(self):
        ...

    def transformer(self, matrice):
        # The polygon of the transformed vertices.
        ...

    @property
    def aire(self):
        # The area as a float, by the shoelace formula. 0.0 below three
        # vertices.
        ...
