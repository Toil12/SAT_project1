import numpy as np
from PyQt5.QtWidgets import QApplication
from pysat import solvers
from SAT1.GUI import GUI
from SAT1.FileOperation import FileOperation as fileop


from pysat import solvers
import numpy as np
import sys

# s=solvers.Solver()
# s.add_clause([1,-3])
# s.add_clause([2,3,-1])
# s.solve()



class Solver:
    def __init__(self):
        self.problem

    def Solve(self,map:dict):
        pass

if __name__ == '__main__':
    file_name='tents-10x10-e1.txt'
    map = fileop.ReadFile(file_name)
    app = QApplication(sys.argv)
    gui=GUI(map)
    gui.InitUI()
    gui.Load()
    sys.exit(app.exec_())
    # gui.initUI()
    # problem=TentsMapReader(sudoku_path)
    # print(problem)
    # sat_clause=TentsClauseMaker(problem)
    # result=SatSolver(sat_clause)
    # show=Draw(result)


