<div align="center">

# The maths

**Linear algebra, probability and statistics, written in plain Python and held
against something that can contradict them.**

`mth-01-algebre` → `mth-02-probas` → `mth-03-statistiques`

20 of 20 exercises complete

</div>

---

## About

This is the maths line of the [roadmap](README.md), run in the background of
the prep while the route to the trained GPT goes on. Nothing here imports a
library: no `numpy`, no `random`, no `statistics`. Each step is graded by its
own checker, and each formula is set against a second, independent path to the
same number, a figure seen by eye, a simulation, or a count over thousands of
cases whose answer is known.

| Module | Question |
|---|---|
| [`mth-01-algebre`](ms-00-prepa/mth-01-algebre) | Can a matrix be read as the transformation it is, and its determinant as the area it scales? |
| [`mth-02-probas`](ms-00-prepa/mth-02-probas) | Does a simulation land where the closed form says, inside a bound that tightens with the draws? |
| [`mth-03-statistiques`](ms-00-prepa/mth-03-statistiques) | Do two series really differ, and how often is that answer wrong? |

Each step folder carries the whole module up to that step, so any folder runs
on its own. Three results, one per module, from the repository root, each in its own subshell:

```bash
(cd ms-00-prepa/mth-01-algebre/ex02 && python3 -c "from produit import Matrice, Vecteur; E, R = Matrice([[2, 0], [0, 1]]), Matrice([[0, -1], [1, 0]]); print(E.puis(R) @ Vecteur([1, 0]), R.puis(E) @ Vecteur([1, 0]))")
(cd ms-00-prepa/mth-02-probas/ex05 && python3 -c "from distribution import variance, variance_naive; L = {1.23456789e9: 0.5, 1.23456790e9: 0.5}; print(variance(L), variance_naive(L))")
(cd ms-00-prepa/mth-03-statistiques/ex05 && python3 -c "from rapport import mesures_pour_detecter; print(mesures_pour_detecter(0.10, (1 / 12) ** 0.5, 1.96))")
```

They print `Vecteur([0, 2]) Vecteur([0, 1])`, then `25.0 -256.0`, then `65`.
The sections below say what each of those means.

## Progress

### mth-01-algebre, complete, 8 of 8

Vectors as classes with their operators, matrices read by their columns, the
product as a composition, the determinant as a signed area, the inverse and
the rank, eigenvalues from the trace and the determinant, norm and projection,
and a 2D engine that chains transformations over a polygon and checks that its
area follows the determinant.

### mth-02-probas, complete, 6 of 6

A law and its variance, a congruential generator and the counters hidden in its
low bits, Bernoulli, binomial and geometric laws against their closed forms,
Bayes on a screening test, the square-root cost of precision, and a simulator
that confronts each law with its formula under a bound that tightens.

### mth-03-statistiques, complete, 6 of 6

The bias of the variance divided by n, the coverage of a confidence interval
counted rather than assumed, the bootstrap where no formula exists, the
comparison of two series and its false-positive rate, multiple comparisons and
Bonferroni, and a report that can answer "undecided".

## What they measured

Every figure below is reproducible from the code published here.

- **Order shows on a single point.** Stretching the x axis by 2 then turning a
  quarter turn sends `[1, 0]` to `[0, 2]`; turning first sends it to `[0, 1]`.
- **The one-pass variance goes negative.** On two latencies in nanoseconds,
  1.23456789e9 and 1.23456790e9, whose variance is 25, `E[X²] - E[X]²` returns
  -256.0. The two-pass version returns 25.0.
- **The low bit of a congruential generator is a counter.** Its runs have a
  single length: it alternates 0, 1, 0, 1 on every draw, because both
  constants are odd.
- **A false claim passes on small data.** On a geometric law of expectation
  exactly 5, the claim 5.2 is accepted on 1,000 draws, its gap of 0.017 sitting
  under a bound of 0.707, and rejected on 100,000, where the gap is 0.208 and
  the bound 0.071.
- **"95 %" is a count.** A 95 % interval built on five measurements with the
  normal quantile contains the true mean in 86.6 % of 20,000 samples. Student's
  quantile, with the same standard deviation, brings it to 93.4 %.
- **The textbook sample size is a coin toss.** The formula asks for 65
  measurements per series to detect a gap of 0.10, and 65 detect it about one
  time in two. Four times as many detect it almost every time.

## Decisions worth naming

### Operators refuse what they do not know

Every operator of `Vecteur` and `Matrice` returns `NotImplemented` for a type it
does not handle, and Python turns that refusal into the `TypeError` a caller
expects. Sizes that do not fit raise `ErreurDeShape`, a subclass of
`ValueError`, and the type is checked before the size: a list has a length but
no numbers, and testing the size first would raise the wrong error.

### The variance takes two passes

`E[X²] - E[X]²` is the same number on paper and a different one in floating
point: it subtracts two large, nearly equal values and loses every digit they
share. The two-pass form subtracts before it squares, so nothing large is ever
taken from anything large. The one-pass version is kept, named
`variance_naive`, only to show what it returns.

### The bound comes from the theory, not from the data

When a simulation is set against its closed form, the bound is five standard
errors computed from the law's theoretical standard deviation, never from the
dispersion of the sample being judged. A bound drawn from the data would widen
with them, and a broken generator would vouch for itself.

### A ceiling written by hand needs a tolerance

Three functions round up by hand, a percentile rank and two measurement
budgets. They used to move to the next integer as soon as `int()` dropped
anything, so a float landing a hair above a whole number stepped one too far:
`(0.07 / 0.01) ** 2` is `49.000000000000014`, and a budget paid for 50
measurements instead of 49. No grader poses such a case. The three now move up
only for a real fraction, checked against the exact ceiling computed in
fractions on 128,700 cases: 321 wrong answers before, none after.

### Zero is compared with a tolerance that scales

`est_orthogonal` used to compare a dot product to zero exactly, and the
residual of a projection, orthogonal by construction, came back `False`: its
dot product with the line reads `4.44e-16`. It now accepts a dot product up to
`1e-9` times the product of the two lengths, so it reads the angle and not the
size. Over 14,520 projection residuals it used to fail 5,200 and now fails none;
over 28,561 pairs of integer vectors, where the old comparison was already
exact, the answers did not change.
