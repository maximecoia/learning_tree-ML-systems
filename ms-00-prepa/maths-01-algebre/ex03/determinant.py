"""maths-01-algebre ex03: the determinant.

Statement:  ./exo maths-01-algebre ex03
Grade:      ./exo maths-01-algebre ex03 -c
Allowed:    isinstance iter len list range sum zip abs
"""

# --- carried over from ex02/produit.py --------------------------------------
# Paste ErreurDeShape and Vecteur here.


class Matrice:
    # --- carried over from ex02/produit.py ----------------------------------
    # Paste the body of Matrice here.

    # --- new in ex03 ---------------------------------------------------------
    @property
    def det(self):
        # The determinant of a 2x2 matrix. ErreurDeShape for any other shape.
        ...

    @property
    def facteur_aire(self):
        # The factor by which the matrix scales areas.
        ...

    @property
    def renverse_orientation(self):
        # True when the matrix flips orientation, like a mirror.
        ...

    @property
    def est_singuliere(self):
        # True when the matrix squashes a dimension.
        ...
