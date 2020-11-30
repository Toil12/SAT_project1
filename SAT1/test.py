from pysat import solvers
s=solvers.Solver()
s.add_clause([1,-3])
s.add_clause([2,3,-1])
s.solve()
print(s.get_model())