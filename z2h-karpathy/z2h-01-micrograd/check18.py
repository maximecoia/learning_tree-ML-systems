import random

from nn import MLP

random.seed(1337)
n = MLP(3, [4, 4, 1])

print(len(n.parameters()))
print(n([2.0, 3.0, -1.0]))
