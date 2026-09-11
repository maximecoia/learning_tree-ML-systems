"""Acceptance test for the engine. Three checks, one command."""
import random

from engine import Value
from nn import MLP


def verdict(name, ok, detail):
    print('%-36s %-5s  %s' % (name, 'OK' if ok else 'ECART', detail))
    return ok


all_ok = True

# 1. the reference neuron: the same bits PyTorch gives, in float64
x1, x2 = Value(2.0), Value(0.0)
w1, w2 = Value(-3.0), Value(1.0)
b = Value(6.8813735870195432)
o = (x1 * w1 + x2 * w2 + b).tanh()
o.backward()
attendu = {'o': 0.7071067811865476, 'x1': -1.4999999999999996,
           'w1': 0.9999999999999998, 'x2': 0.4999999999999999, 'w2': 0.0}
obtenu = {'o': o.data, 'x1': x1.grad, 'w1': w1.grad, 'x2': x2.grad, 'w2': w2.grad}
faux = [k for k, v in attendu.items() if obtenu[k] != v]
all_ok &= verdict('1. reference neuron, bit for bit', not faux,
                  'all five exact' if not faux else
                  'differs on %s: %r' % (faux, [obtenu[k] for k in faux]))

# 2. a + a accumulates instead of overwriting: the += fix of section 15
a = Value(3.0)
d = a + a
d.backward()
all_ok &= verdict('2. a + a gives a.grad == 2', a.grad == 2.0,
                  'expected 2.0                   got %s' % a.grad)

# 3. the network actually learns the four examples
random.seed(1337)
model = MLP(3, [4, 4, 1])
xs = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]
ys = [1.0, -1.0, -1.0, 1.0]
for _ in range(100):
    pred = [model(x) for x in xs]
    loss = sum((yh - y) ** 2 for yh, y in zip(pred, ys))
    model.zero_grad()
    loss.backward()
    for p in model.parameters():
        p.data += -0.05 * p.grad
signes = all((yh.data > 0) == (y > 0) for yh, y in zip(pred, ys))
all_ok &= verdict('3. loss < 0.01 and 4 signs right', loss.data < 0.01 and signes,
                  'expected < 0.01                got %.6f' % loss.data)

print('ALL OK' if all_ok else 'SOMETHING IS OFF')
