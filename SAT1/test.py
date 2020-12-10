from pysat.solvers import Solver, Minisat22

s = Solver(name='cadical')
s.add_clause([-1, 2])
s.add_clause([-1, -3])
k=s.solve()
print(k)