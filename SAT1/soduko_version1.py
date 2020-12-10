from pysat import solvers
import numpy as np
import sys

# s=solvers.Solver()
# s.add_clause([1,-3])
# s.add_clause([2,3,-1])
# s.solve()




def SudokuClauseMaker(problem:np.ndarray):
    def Valid(cells):
        pass

def SudokuMapReader(map_path:str)->np.ndarray:
    result = []
    with open(sudoku_path, 'r') as f:
        for line in f:
            line = line.strip('\n').replace(' ','')
            row = []
            for char in line:
                if char=='.':
                    row.append(0)
                else:
                    row.append(int(char))
            result.append(row)
    f.close()
    result=np.array(result)
    return result



def SatSolver(problem):
    pass

if __name__ == '__main__':
    sudoku_path='env/sudoku_1.txt'
    problem=SudokuMapReader(sudoku_path)
    print(problem)
    sat_clause=SudokuClauseMaker(problem)

