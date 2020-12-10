from SAT1.demo2 import *
solver = "/home/jingcheng/下载/cadical-sc2020-45029f8/build/cadical"
grid = [list(input()) for i in range(9)]

x= get_vars(8, 8, 3)  # one variable per (row, column, value)

# .:表示空 v=0
# T:表示树 v=1
# z:表示帐篷 v=2
# each cell has exactly 1 value

for i in range(8):
    for j in range(8):
        exactly_one(x[i][j][v] for v in range(3))
        if grid[i][j] =='T': 
            clause(x[i][j][1])

# 单元格旁（上，下，左，右）是否有一棵树
for i in range(8):
    for j in range(8):
        found = False
        for i1 in range(8):
            for j1 in range(8):
                if grid[i1][j1] == "T":
                    result = abs(i1 - i)+abs(j1 - j)
                    if result <= 1: #单元格附近（上，下，左，右）有一棵树，
                        found = True #啥也不干
        if found == False:
           clause(-x[i][j][2])

#对每行每列的帐篷数进行遍历:改进成每次的结尾的数

for i in range(8):
    k = grid[i][9]
    
    #sum_constraint(k, (x[i][j][2] for j in range(8)))  #row
for j in range(8):
    k = grid[8][j]
    #sum_constraint(k, (x[i][j][2] for j in range(8)))  #column
    
    #clause(x[i][j][2] for j in range(8)) #row
    #clause(x[j][i][2] for j in range(8)) #column

#2x2中最多出现一个帐篷

for i in range(7):
    for j in range(7):
        at_most_one(x[i+a][j+b][2] for a in range(2) for b in range(2))
        #clause(x[i+a][j+b][2] for a in range(1) for b in range(1))     这是至少有一个帐篷
        #result = sum([int(grid[i][j]),int(grid[i][j+1]),int(grid[i+1][j]),int(grid[i+1][j+1])])  #取sum
        #if result <= 1:  #只包含一个帐篷
            #clause(x[i][j][2])


print (get_encoding())
exit(0)

#sat solving magic
if sat_solve(solver): 
    #reconstruct solution
    for i in range(9):
        for j in range(9):
            grid[i][j] = str(next(v for v in range(9)
                if model_val(x[i][j][v]))+1)
    #print
    print ("-"* 25 + "\n" + "\n".join("| " + "".join(
        grid[i][j] + (" | "if j % 3 == 2 else "")
        for j in range(9))+("\n" + "-"*25 if i % 3 == 2 else "")
        for i in range(9)))
else:
    print ("no solution")
