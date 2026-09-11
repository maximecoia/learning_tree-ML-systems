# Unit 1 — micrograd, reverse-mode automatic differentiation

The engine from Karpathy's
[*The spelled-out intro to neural networks and backpropagation*](https://www.youtube.com/watch?v=VMj-3S1tku0),
written by hand. Nothing here is new: every line is built section by section in
the written unit that accompanies it, and a harness checks that the two copies
never drift apart.

## What is here

| file | lines | what it is |
|---|---|---|
| `engine.py` | 106 | `Value`, the five local derivatives, `backward()` |
| `nn.py` | 55 | `Neuron`, `Layer`, `MLP`, `parameters()` |
| `verifier.py` | 52 | three checks, one command |
| `check06.py`, `check07.py`, `check18.py` | | the one-off checks for sections 06, 07 and 18 |

**No dependencies.** `engine.py` imports only `math`, `nn.py` only `random`.
PyTorch is useful for the section 17 comparison alone, and its absence is
handled cleanly.

## Run

```bash
python3 verifier.py
```

```
1. reference neuron, bit for bit     OK     all five exact
2. a + a gives a.grad == 2           OK     expected 2.0                   got 2
3. loss < 0.01 and 4 signs right     OK     expected < 0.01                got 0.005104
ALL OK
```

Instant. None of these checks trains for long.

## What each check proves

**1, the reference neuron, bit for bit.** The five numbers of section 17, held
to exact equality, against what *this engine* produces rather than against
PyTorch. Section 17 shows that two independent implementations agree to one
**ulp**, never to the bit. But an engine compared to itself has no reason to
move, and exact equality then catches a wrong local derivative that a tolerance
would wave through. When it fails, it names which of the five diverge.

**2, `a + a` gives `a.grad == 2`.** The section 15 bug in three lines. It passes
only if *both* accumulations in `__add__` use `+=`. Breaking one of the two is
not enough to make it fall: the first assignment is overwritten, then completed
by the second.

**3, the network learns.** The four examples of sections 18 to 21, a hundred
steps, demanding a loss under 0.01 *and* all four signs right. It falls if
`zero_grad()` zeroes nothing: the loss sticks at 4.0, which is exactly the
section 21 bug.

All three were broken on purpose to confirm they can fail.

## Using the engine

```python
from engine import Value

a = Value(2.0)
b = Value(-3.0)
c = a * b + a
c.backward()
print(a.grad, b.grad)      # -2.0  2.0
```

```python
from nn import MLP

model = MLP(3, [4, 4, 1])          # 3 inputs, two layers of 4, one output
print(len(model.parameters()))     # 41
```

## What this engine does not have

No tensors: a `Value` carries one scalar. No memory management: the whole graph
stays alive. No handling of non-differentiable points. One Python closure per
operation, which is readable and slow. Five gaps, all deliberate.

That is the point: **the same five local derivatives and the same topological
sort run inside PyTorch**, at a different scale and in a different form.
