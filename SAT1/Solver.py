from SAT1.FileOperation import FileOperation
from pysat.solvers import Solver
import numpy as np
TENT=1
EMPTY=0
TREE=-1

class SAT1Solver():
    def __init__(self,map:dict):
        self.data = map
        self.size = map['size']
        self.row_constraint = map['row_number']
        self.column_constraint = map['column_number']
        self.envrionment = map['environment']
        self.result=[]

    def Run(self):
        self.PreProcessor()
        self.ClauseMaker()
        self.Solver()

    def Combinations(self,L, k):
        n = len(L)
        result = []
        for i in range(n - k + 1):
            if k > 1:
                newL = L[i + 1:]
                Comb, _ = self.Combinations(newL, k - 1)
                for item in Comb:
                    item.insert(0, L[i])
                    result.append(item)
            else:
                result.append([L[i]])
        return result, len(result)

    def GetNeighbours(self, x, y, directions=4)->list:
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
        se=((x)*self.size[0])+y+1
        return se

    def ReturnIndex(self,item):
        for i in range(len(self.small_search_space)):
            if self.small_search_space[i]==item:
                return int(i)

    def SmallSpaceIndex(self, tup, room=None):
        if room == None:
            room = self.small_search_space
        for i in range(len(room)):
            if room[i] == tup:
                return int(i+1)
            else:
                continue

    def PreProcessor(self):
        self.small_search_space=[]
        trees=[]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.envrionment[i,j]==-1:
                    trees.append((i,j))
        for cell in trees:
            neighbours=self.GetNeighbours(cell[0],cell[1])
            for neighbour in neighbours:
                if neighbour!=None \
                        and neighbour not in self.small_search_space \
                        and self.envrionment[neighbour[0],neighbour[1]]!=-1:
                    self.small_search_space.append(neighbour)
        self.small_search_space=sorted(self.small_search_space)

    def NeighbourFilter(self,neigbour,room=None):
        valid_neighbour=[]
        if room==None:
            room=self.small_search_space
        for item in neigbour:
            if item in room and item!=None and item!=-1:
                valid_neighbour.append(item)
            else:
                continue
        return valid_neighbour

    def ClauseMaker(self):
        self.small_search_space_index=[int(i) for i in range(1, len(self.small_search_space)+1)]
        self.clauses = []
        #row constraints
        for row_index in range(len(self.row_constraint)):
            row_con=self.row_constraint[row_index]
            space=[]
            for j in range(len(self.small_search_space)):
                if self.small_search_space[j][0]==row_index:
                    space.append(self.small_search_space_index[j])

            var_indexs=space
            if len(var_indexs)==row_con:
                for v in var_indexs:
                    self.clauses.append([v])
            elif row_con==0:
                for item in var_indexs:
                    self.clauses.append([-item])
            else:
                var_indexs1=[-i for i in var_indexs]
                line_clause1,cluase_number1=self.Combinations(var_indexs1,row_con+1)
                for each in line_clause1:
                    self.clauses.append(each)
                line_clause0,cluase_number0=self.Combinations(var_indexs, len(var_indexs) - row_con + 1)
                for each in line_clause0:
                    self.clauses.append(each)
        # column constrians
        for col_index in range(len(self.column_constraint)):
            col_con=self.column_constraint[col_index]
            space=[]
            for j in range(len(self.small_search_space)):
                if self.small_search_space[j][1]==col_index:
                    space.append(self.small_search_space_index[j])

            var_indexs=space
            if len(var_indexs)==col_con:
                for v in var_indexs:
                    self.clauses.append([v])
            elif col_con==0:
                for item in var_indexs:
                    self.clauses.append([-item])
            else:
                var_indexs1=[-i for i in var_indexs]
                line_clause1,cluase_number1=self.Combinations(var_indexs1,col_con+1)
                for each in line_clause1:
                    self.clauses.append(each)
                line_clause0,cluase_number0=self.Combinations(var_indexs, len(var_indexs) - col_con + 1)
                for each in line_clause0:
                    self.clauses.append(each)

        for i in range(len(self.small_search_space)):
            x=self.small_search_space[i][0]
            y=self.small_search_space[i][1]
            neighbour=self.GetNeighbours(x,y,directions=8)
            neighbour=self.NeighbourFilter(neighbour)
            for n in neighbour:
                nindex=-self.SmallSpaceIndex(n)
                if [-(i+1),nindex] in self.clauses or [nindex,-(i+1)] in self.clauses:
                    continue
                else:
                    self.clauses.append([-(i+1),nindex])

        for item in self.small_search_space:
            tree_space=[]
            neighbours=self.GetNeighbours(item[0],item[1],4)
            count=0
            for each in neighbours:
                if each!=None:
                    if self.envrionment[each[0],each[1]]==-1:
                        count+=1
                    else:
                        continue
                else:
                    continue
            if count>=2:
                k=self.SmallSpaceIndex(item)
                print('dd')
                print(k)
                self.clauses.append([-self.SmallSpaceIndex(item)])

        print(self.clauses)

    def Solver(self,clauses=None):
        transform_clauses=[]
        if clauses==None:
            clauses=np.array(self.clauses)
        for i in range(len(clauses)):
            line=[]
            for item in clauses[i]:
                if type(item)!=int:line.append(item.item())
                else:line.append(item)
            transform_clauses.append(line)
        s=Solver(name='cadical')
        for item in transform_clauses:
            s.add_clause(item)
        self.result_tag=s.solve()
        if self.result_tag==True:
            result_list=s.get_model()
            for index in result_list:
                if index>0:
                    sindex=int(np.abs(index).item()-1)
                    self.result.append(self.small_search_space[sindex])
                else:
                    continue
        else:
            print('gg')

if __name__ == '__main__':
    file_name = 'tents-8x8-e1.txt'
    name = file_name.split('.')[0]
    map = FileOperation.ReadFile(file_name)
    sol=SAT1Solver(map)
    sol.Run()
    print(sol.result_tag)
