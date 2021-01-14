import numpy as np
from SAT1.FileOperation import FileOperation
EMPTY = 0
TENT = 1
TREE =-1
MAX_ITERATION=10000

class BadGenerationException(Exception):
    """ Get raised if we fail to generate a valid grid within MAX_TRIES tentatives. """
    pass

class GridMaker():
    def __init__(self, i,j):
        self.data={}
        self.size =[int(i),int(j)]
        self.nb_tents = int(3.16 * np.min(self.size) - 10.83)
        self.grid = np.zeros((self.size[0], self.size[1]), dtype=int)
        self.PlaceTents(self.nb_tents)
        self.row_constraints, self.col_constraints = self.RowColumnNumber()
        self.PlaceTrees()
        self.RemoveTents()
        self.DataToDict()

    def DataToDict(self):
        self.data['environment'] = np.array(self.grid)
        self.data['size'] = np.array(self.size)
        self.data['row_number'] = np.array(self.row_constraints)
        self.data['column_number'] = np.array(self.col_constraints)

    def PlaceTents(self, nb_tents):
        for _ in range(nb_tents):
            placed = False
            tries=0
            while placed is False:
                if tries > MAX_ITERATION:
                    break
                x = np.random.randint(0, self.size[0])
                y = np.random.randint(0, self.size[1])
                neighbours = self.GetNeighbours(self.grid, x, y, directions=8)
                if self.grid[x][y] != TENT and TENT not in neighbours:
                    self.grid[x][y] = TENT
                    placed = True
                tries+=1

    def PlaceTrees(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid[x][y] == TENT:
                    neighbours = self.GetNeighbours(self.grid, x, y)
                    placed = False
                    tries=0
                    # print('i start')
                    while placed is False:
                        if tries > MAX_ITERATION:
                            break
                        i = np.random.randint(0, 3)
                        # print(i)
                        if neighbours[i] == 0:
                            if i == 0:
                                self.grid[x-1][y] = TREE
                            if i == 1:
                                self.grid[x][y+1] = TREE
                            if i == 2:
                                self.grid[x+1][y] = TREE
                            if i == 3:
                                self.grid[x][y-1] = TREE
                            placed = True
                        tries+=1

    def RemoveTents(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid[x][y] == TENT:
                    self.grid[x][y] = EMPTY
        self.finish=True

    def RowColumnNumber(self):
        row_constraints = []
        col_constraints = []
        for i in range(self.size[0]):
            sum=0
            for item in self.grid[i,:]:
                if item==TENT:
                    sum+=1
            row_constraints.append(sum)

        for i in range(self.size[1]):
            sum=0
            for item in self.grid[:,i]:
                if item==TENT:
                    sum+=1
            col_constraints.append(sum)

        return row_constraints, col_constraints


    def GetNeighbours(self,env, x, y, directions=4):
        neighbours = []
        if directions == 4:
            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x - 1][y])
            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append(env[x][y + 1])
            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append(env[x + 1][y])
            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x][y - 1])
        else:
            if x - 1 < 0 or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x - 1][y - 1])

            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x - 1][y])

            if x - 1 < 0 or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append(env[x - 1][y + 1])

            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append(env[x][y + 1])

            if x + 1 >= self.size[0] or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append(env[x + 1][y + 1])

            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append(env[x + 1][y])

            if x + 1 >= self.size[0] or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x + 1][y - 1])

            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append(env[x][y - 1])
        return neighbours

if __name__ == '__main__':
    a=GridMaker(8,8)
    print(a.grid)
    for key in a.data.keys():
        print(key)
        print(a.data[key])
    # print(a.data.keys())
