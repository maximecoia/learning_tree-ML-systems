from graph import trace, example

L = example()
nodes, edges = trace(L)
print(len(nodes), len(edges))
print(sorted(n.label for n in nodes))
print(sorted(f"{p.label}->{q.label}" for p, q in edges))
