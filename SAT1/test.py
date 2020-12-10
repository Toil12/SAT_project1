from pysat.solvers import Solver, Minisat22

s = Solver(name='cadical')
s.add_clause([-1, 2])
s.add_clause([-1, -3])
k=s.solve()
a=[1]
print((1,2)==(2,1))