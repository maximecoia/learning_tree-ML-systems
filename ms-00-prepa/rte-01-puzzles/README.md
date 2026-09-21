# rte-01-puzzles — Tensor Puzzles

Twenty-one NumPy primitives, reimplemented from first principles in PyTorch.

**Puzzles by [Sasha Rush](http://rush-nlp.com) (with Marcos Treviso), from
[srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles), MIT licensed,
© 2022. Solutions by Maxime Coia.**

This is my worked copy of that exercise book, which its author publishes for
readers to copy and solve. A filled-in copy can otherwise read as if it were the
original, so the split is worth stating outright:

- **His:** the twenty-one statements, the diagrams, and the hypothesis-based
  checker that grades every answer (`lib.py`, fetched from his repository by the
  notebook's setup cell).
- **Mine:** the twenty-one function bodies written under those statements.

## The rules that make it hard

Each puzzle asks for one function of the standard library, written in a single
line of under eighty columns. The only tools allowed are `@`, arithmetic,
comparison, `.shape`, indexing, and the puzzles already solved. No `view`, no
`sum`, no `take`, no `squeeze`, no `tensor`. You start with two primitives given
for free, `arange` and `where`, and build everything else on top.

What is left once loops and helpers are gone is broadcasting. Comparing an
`arange` shaped `[:, None]` against one shaped `[None, :]` builds the selection
matrix a loop would otherwise walk, and `@` collapses it back down. `eye` is
`i == j`, `triu` is the same comparison loosened to `i <= j`, and `cumsum` is a
single product against that triangle.

This is why the module sits on the route rather than beside it. Causal attention
is `arange[:, None] >= arange[None, :]`. The twenty-one puzzles are that one
gesture, declined twenty-one times.

## What is in this folder

- `Tensor Puzzlers.ipynb` — the finished notebook, all twenty-one solved. Each
  puzzle appears once and carries the answer: the starter cell underneath every
  statement, whose body raises `NotImplementedError`, is not kept, since nothing
  is left for a reader to fill in. The diagrams are inline SVG, so the notebook
  renders on its own, and each one shows the spec's `target` row above my `yours`
  row on three generated examples. The `run_test(...)` call at the head of each
  cell stays commented out, the way it arrived: on success it displays a random
  puppy video, and the verdict is established outside the notebook anyway.

Nothing else. The upstream clone, its `lib.py`, its images, the virtualenv and
the hypothesis cache stay out of this repository: re-running the notebook fetches
`lib.py` from upstream, and republishing Sasha Rush's files here would serve no
one.

One post-processing pass is applied to the notebook before it lands here, and it
is worth naming because the bug it fixes is invisible locally. chalk writes some
labels with a `style` attribute that spans several lines. The newline is a real
one in the file and CSS treats it as whitespace, so Jupyter renders them fine.
GitHub's notebook viewer re-serializes that attribute and writes the newline as a
literal backslash-n, which CSS reads as an escape sequence: the declaration behind
it parses as a property whose name starts with `n` and is dropped. `font-size`
goes with it, the label falls back to the 13px it inherits from the page, and that
sits inside a group scaled by about 79.

Only the multi-line labels break, which is why the damage looks random. Measured
on GitHub's viewer when the fix was written, against the notebook as it then
stood: 52 of its 159 labels carried a newline, and those 52 were exactly the ones
that covered their diagram, the worst at 713px in a 285px frame. Carrying the
same declarations as SVG presentation attributes keeps the newline out of the CSS
parser, and none overflowed afterwards. Dropping the starter cells took the
notebook down to 24 diagrams and 101 labels; every one of them is written as
presentation attributes, and re-running the pass finds nothing left to rewrite.

A second rewrite goes with it, for the frame rather than the labels. chalk sizes
each diagram in pixels and gives it no `viewBox`, so a viewer with less room than
that has nothing to remap the drawing onto: `max-width: 100%` shrinks the box and
the drawing is cut off instead of scaled down. GitHub's content column measured
753px and five diagrams were wider, `arange` at 1999px showing as a black corner,
the top left of a frame four fifths of which was off the column. Every diagram
now carries `viewBox="0 0 <width> <height>"` alongside
`max-width:100%; height:auto`, so it scales to whatever room it is given and
still draws at its pixel size when there is room enough.

## How the answers were checked

Not by the notebook. A cell keeps whatever output it printed last, so an answer
edited after its final run still looks solved, and three of these were in exactly
that state: `bincount`, `repeat` and `bucketize` were displaying a diagram drawn
while their body still raised `NotImplementedError`, which shows up as a missing
`yours` row. They have been redrawn. Even fresh, a diagram shows agreement with
the spec on three generated examples. That is evidence, not a verdict.

The verdict comes from outside. The twenty-one answers live in a plain module,
and a runner pairs each one with the upstream spec and the upstream hypothesis
harness, both read straight from the notebook, in a fresh process where no stale
cell can vouch for anything: twenty-one passed, none failed.

The runner was itself checked against a deliberate break. Making `cumsum` return
twice its value turns two puzzles red, `cumsum` and the `compress` built on it,
and the run exits non-zero. A suite that stays green under that is not measuring
anything.

## Running it

```bash
pip install -qqq torchtyping hypothesis pytest git+https://github.com/chalk-diagrams/chalk
wget -q https://github.com/srush/Tensor-Puzzles/raw/main/lib.py
```

Then open the notebook and run it top to bottom. The first cell does both steps
if you would rather stay inside Jupyter.
