import math


class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data                       # the number itself
        # dL/dself, filled by the backward pass
        self.grad = 0
        # does nothing until an op sets it
        self._backward = lambda: None
        self._prev = set(_children)            # where this value came from
        self._op = _op                         # for the drawing only
        self.label = label                     # for the drawing only

    def __repr__(self):
        # without this: a memory address
        return f"Value(data={self.data})"

    def __add__(self, other):
        # accept 2 as well as Value(2)
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        # a closure: it remembers self, other, out
        def _backward():
            self.grad += out.grad          # local derivative 1
            other.grad += out.grad         # local derivative 1
        out._backward = _backward             # armed now, fired by backward()

        return out

    def __mul__(self, other):
        # accept 2 as well as Value(2)
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        # a closure: it remembers self, other, out
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward             # armed now, fired by backward()

        return out

    def __pow__(self, other):
        # a constant exponent only
        assert isinstance(other, (int, float)), "only int/float powers"
        # one parent, not two
        out = Value(self.data ** other, (self,), f'**{other}')

        # a closure: it remembers self, other, out
        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad
        out._backward = _backward             # armed now, fired by backward()

        return out

    def exp(self):
        # exp is its own derivative
        out = Value(math.exp(self.data), (self,), 'exp')

        # a closure: it remembers self, other, out
        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward             # armed now, fired by backward()

        return out

    def tanh(self):
        x = self.data
        # t is captured by the closure below
        t = (math.exp(2*x) - 1)/(math.exp(2*x) + 1)
        out = Value(t, (self,), 'tanh')

        # a closure: it remembers self, other, out
        def _backward():
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward             # armed now, fired by backward()

        return out

    def __neg__(self):                # -self
        return self * -1

    def __radd__(self, other):        # other + self
        return self + other

    def __sub__(self, other):         # self - other
        return self + (-other)

    def __rsub__(self, other):        # other - self
        return other + (-self)

    def __rmul__(self, other):        # other * self
        return self * other

    def __truediv__(self, other):     # self / other
        return self * other**-1

    def __rtruediv__(self, other):    # other / self
        return other * self**-1

    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule
        self.grad = 1
        for v in reversed(topo):
            v._backward()
