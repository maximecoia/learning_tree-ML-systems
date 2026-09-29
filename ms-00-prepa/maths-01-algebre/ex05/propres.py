"""maths-01-algebre ex05: eigenvectors.

Statement:  ./exo maths-01-algebre ex05
Grade:      ./exo maths-01-algebre ex05 -c
Allowed:    isinstance iter len list range sum zip abs all float enumerate
            next sorted ValueError
"""

# --- carried over from ex04/systemes.py -------------------------------------
# Paste ErreurDeShape and Vecteur here.


class Matrice:
    # --- carried over from ex04/systemes.py ---------------------------------
    # Paste the body of Matrice here, det and its properties included.

    # --- new in ex05 ---------------------------------------------------------
    @property
    def trace(self):
        # The sum of the diagonal of a square matrix. ErreurDeShape when the
        # matrix is not square.
        ...

    def valeur_propre(self, v):
        # The eigenvalue of v when v is an eigenvector, None otherwise.
        # ValueError when v is the zero vector.
        ...

    def valeurs_propres(self):
        # The sorted real eigenvalues of a 2x2 matrix, as floats. An empty
        # list when there is none.
        ...
