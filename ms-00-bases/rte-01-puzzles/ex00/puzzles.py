"""Solutions to Sasha Rush's Tensor Puzzles (https://github.com/srush/Tensor-Puzzles).

The exercise set asks for 21 NumPy/PyTorch primitives reimplemented from first
principles. The house rules are what make it hard: one line per puzzle, and the
only tools allowed are `@`, arithmetic, comparison, `.shape`, indexing, and the
puzzles already solved. No `view`, `sum`, `take`, `squeeze` or `tensor`.

Every solution below therefore leans on broadcasting: a comparison between two
`arange` vectors shaped `[:, None]` and `[None, :]` builds the selection matrix
that a loop would otherwise walk, and `@` collapses it back down.

The statements and the test harness are Sasha Rush's, under MIT. The function
bodies are mine.
"""

import torch
from torchtyping import TensorType as TT


# The two primitives the puzzles hand out for free.

def arange(i: int) -> TT["i"]:
    "Replaces a for-loop."
    return torch.tensor(range(i))


def where(q, a, b):
    "Replaces an if-statement."
    return (q * a) + (~q) * b


# Puzzle 1 - ones. Multiplying by zero flattens any arange to a zero vector.
def ones(i: int) -> TT["i"]:
    return arange(i) * 0 + 1


# Puzzle 2 - sum. A dot product against a vector of ones adds every entry.
def sum(a: TT["i"]) -> TT[1]:
    return ones(a.shape[0]) @ a[:, None]


# Puzzle 3 - outer. Broadcasting a column against a row is the outer product.
def outer(a: TT["i"], b: TT["j"]) -> TT["i", "j"]:
    return a[:, None] * b[None, :]


# Puzzle 4 - diag. Indexing with the same arange twice walks the diagonal.
def diag(a: TT["i", "i"]) -> TT["i"]:
    return a[arange(a.shape[0]), arange(a.shape[0])]


# Puzzle 5 - eye. The diagonal is where the row index equals the column index.
def eye(j: int) -> TT["j", "j"]:
    return (arange(j)[:, None] == arange(j)[None, :]) * 1


# Puzzle 6 - triu. Same comparison, loosened to `<=`, fills the upper triangle.
def triu(j: int) -> TT["j", "j"]:
    return (arange(j)[:, None] <= arange(j)[None, :]) * 1


# Puzzle 7 - cumsum. Each output entry sums a prefix, which is one triu column.
def cumsum(a: TT["i"]) -> TT["i"]:
    return a @ triu(a.shape[0])


# Puzzle 8 - diff. Subtract the shifted vector, and treat index 0 as its own base.
def diff(a: TT["i"], i: int) -> TT["i"]:
    return a - where(arange(i) == 0, 0, a[arange(i) - 1])


# Puzzle 9 - vstack. Row 0 selects `a`, row 1 selects `b`.
def vstack(a: TT["i"], b: TT["i"]) -> TT[2, "i"]:
    return where(arange(2)[:, None] == 0, a, b)


# Puzzle 10 - roll. Shifting the index by one, modulo the length, wraps around.
def roll(a: TT["i"], i: int) -> TT["i"]:
    return a[(arange(i) + 1) % i]


# Puzzle 11 - flip. Reading the index backwards reverses the vector.
def flip(a: TT["i"], i: int) -> TT["i"]:
    return a[i - arange(i) - 1]


# Puzzle 12 - compress. `cumsum(g) - 1` is the destination slot of each kept
# entry; comparing it to an arange builds the permutation matrix, and masking by
# `g` drops the entries that were not selected.
def compress(g: TT["i", bool], v: TT["i"], i: int) -> TT["i"]:
    return v @ ((((cumsum(g * 1) - 1)[:, None] == arange(i)[None, :]) * 1) * g[:, None])


# Puzzle 13 - pad_to. `% i` keeps the read in bounds when j > i; the `where`
# then zeroes whatever sat past the end of the source.
def pad_to(a: TT["i"], i: int, j: int) -> TT["j"]:
    return where(arange(j) < i, a[arange(j) % i], 0)


# Puzzle 14 - sequence_mask. Compare a column of lengths to a row of positions.
def sequence_mask(values: TT["i", "j"], length: TT["i", int]) -> TT["i", "j"]:
    return where(arange(values.shape[1])[None, :] < length[:, None], values, 0)


# Puzzle 15 - bincount. One-hot each value, then sum the rows of that matrix.
def bincount(a: TT["i"], j: int) -> TT["j"]:
    return ones(a.shape[0]) @ ((a[:, None] == arange(j)[None, :]) * 1)


# Puzzle 16 - scatter_add. Same one-hot matrix, weighted by the values instead.
def scatter_add(values: TT["i"], link: TT["i"], j: int) -> TT["j"]:
    return values @ ((link[:, None] == arange(j)[None, :]) * 1)


# Puzzle 17 - flatten. Integer division gives the row, the remainder the column.
def flatten(a: TT["i", "j"], i: int, j: int) -> TT["i * j"]:
    return a[arange(i * j) // j, arange(i * j) % j]


# Puzzle 18 - linspace. `(n == 1)` guards the division when a single point is
# asked for, which is the one case where the step is undefined.
def linspace(i: TT[1], j: TT[1], n: int) -> TT["n", float]:
    return i + (j - i) * arange(n) / (n - 1 + (n == 1))


# Puzzle 19 - heaviside. Zero falls back to `b`, anything else tests its sign.
def heaviside(a: TT["i"], b: TT["i"]) -> TT["i"]:
    return where(a == 0, b, (a > 0) * 1)


# Puzzle 20 - repeat. A column of ones stretches the vector into d rows.
def repeat(a: TT["i"], d: TT[1]) -> TT["d", "i"]:
    return ones(d[0])[:, None] * a[None, :]


# Puzzle 21 - bucketize. Count how many boundaries each value clears.
def bucketize(v: TT["i"], boundaries: TT["j"]) -> TT["i"]:
    return ((v[:, None] >= boundaries[None, :]) * 1) @ ones(boundaries.shape[0])
