from engine import Value

a = Value(2.0,  label='a')
b = Value(-3.0, label='b')
c = Value(10.0, label='c')
e = a*b       ; e.label = 'e'
d = e + c     ; d.label = 'd'
f = Value(-2.0, label='f')
L = d * f     ; L.label = 'L'

print(a)
print(L)
print(L._op, L.grad)
print(sorted(n.label for n in L._prev))
print(L._backward())
