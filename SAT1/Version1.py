from pysat import solvers
import numpy as np

s=solvers.Solver()
s.add_clause([1,-3])
s.add_clause([2,3,-1])
s.solve()
print(s.get_model())



def ClauseMaker():
    pass

def MapReader(map):
    pass

def SatSolver(problem):
    pass

if __name__ == '__main__':
    sudoku_path='SAT1/env/sudoku_1.txt'
    sudoku=np.loadtxt(sudoku_path)
    print(sudoku)
    print('PyCharm')