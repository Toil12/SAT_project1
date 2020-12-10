from SAT1.FileOperation import FileOperation
from pysat import solvers
import numpy as np
TENT=1
EMPTY=2
TREE=3

class Solver():
    def __init__(self,map:dict):
        self.data = map
        self.size = map['size']
        self.row_constraint = map['row_number']
        self.column_constraint = map['column_number']
        self.envrionment = map['environment']
        self.PreProcessor()

    def PreProcessor(self):
        self.var=np.zeros((self.size[0],self.size[1]*3))
        self.small_search_space=[]
        trees=[]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.envrionment[i,j]==-1:
                    self.var[i,3*(j+1)-1]=1
                    trees.append((i,j))
        for cell in trees:
            neighbours=self.GetNeighbours(cell[0],cell[1])
            for neighbour in neighbours:
                if neighbour!=None and neighbour not in self.small_search_space:
                    self.small_search_space.append(neighbour)
        self.small_search_space=sorted(self.small_search_space)

    def ClauseMaker(self):
        clauses=[]
        self.row_constraint
        self.column_constraint
        self.small_search_space
        [][]







    def GetNeighbours(self, x, y, directions=4):
        neighbours = []
        if directions == 4:
            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y))
            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x,y+1))
            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y))
            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x,y-1))
            return neighbours
        else:
            if x - 1 < 0 or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y-1))

            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y))

            if x - 1 < 0 or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y+1))

            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x,y+1))

            if x + 1 >= self.size[0] or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y+1))

            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y))

            if x + 1 >= self.size[0] or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y-1))

            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x,y-1))
        return neighbours

    def PositioanToVar(self,positon:tuple):
        x=positon[0]
        y=positon[1]
        se=(x*self.size[0])+y
        return se*3

    def ReturnIndex(self,item):
        for i in range(len(self.small_search_space)):
            if self.small_search_space[i]==item:
                return int(i)

if __name__ == '__main__':
    file_name = 'tents-8x8-t1.txt'
    name = file_name.split('.')[0]
    map = FileOperation.ReadFile(file_name)
    sol=Solver(map)
    sol.PreProcessor()
    print(sol.envrionment)
    print(sol.small_search_space)
    print(len(sol.small_search_space))
    print(sol.PositioanToVar((2,2)))