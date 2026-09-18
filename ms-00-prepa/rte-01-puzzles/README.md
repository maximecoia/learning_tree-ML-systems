# rte-01-puzzles — Tensor Puzzles

Twenty-one NumPy primitives, reimplemented from first principles in PyTorch.

The exercise set is [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles)
by Sasha Rush, MIT licensed, © 2022. The statements, the drawings and the
hypothesis-based checker are his. The twenty-one function bodies in the notebook
are mine.

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

- `Tensor Puzzlers.ipynb` — the finished notebook, all twenty-one solved, with
  the checker's output kept in the cells. The diagrams are inline SVG, so the
  notebook renders on its own.

Nothing else. The upstream clone, its `lib.py`, its images, the virtualenv and
the hypothesis cache stay out of this repository: re-running the notebook fetches
`lib.py` from upstream, and republishing Sasha Rush's files here would serve no
one.

One post-processing pass is applied to the notebook before it lands here. chalk
writes every diagram label as `<text style="...;font-size:0.75px;...">`, and that
declaration block is dropped by GitHub's notebook renderer while the `style` on
the surrounding `<g>` survives. The label then falls back to 16px inside a group
scaled by about 79, which puts a word roughly 1460px tall over a 300px-tall
diagram. Carrying the same declarations as SVG presentation attributes survives
the renderer and measures identically in a browser, so that is what the published
notebook holds.

## How the answers were checked

The notebook carries the checker's verdict cell by cell. The same twenty-one
solutions were then extracted to a plain module and run again against the
upstream specs and their hypothesis harness, outside a notebook, where a stale
cell cannot make a puzzle look solved: twenty-one passed, none failed.

The harness itself was checked against a deliberate break. Making `cumsum`
return twice its value turned two puzzles red, `cumsum` and the `compress` that
depends on it, and the run exited non-zero. A suite that stays green under that
is not measuring anything.

## Running it

```bash
pip install -qqq torchtyping hypothesis pytest git+https://github.com/chalk-diagrams/chalk
wget -q https://github.com/srush/Tensor-Puzzles/raw/main/lib.py
```

Then open the notebook and run it top to bottom. The first cell does both steps
if you would rather stay inside Jupyter.
