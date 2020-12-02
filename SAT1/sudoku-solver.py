from flo_sat_encoder import *
solver = "/home/jingcheng/下载/cadical-sc2020-45029f8/build/cadical"
grid = [list(input()) for i in range(9)]

x= get_vars(9, 9, 9)  # one variable per (row, column, value)


# each cell has exactly one value

for i in range(9):
    for j in range(9):
        exactly_one(x[i][j][v] for v in range(9))
        if grid[i][j] !='.': #value predetermined?
            clause(x[i][j][int(grid[i][j])-1])

# value in each row/column/3x3 block need to occur

for v in range(9):
    for i in range(9):
        clause(x[i][j][v] for j in range(9))  #row
        clause(x[j][i][v] for j in range(9))  #column
    # 3x3 block
    for i in range(3):
        for j in range(3):
            clause(x[3*i+a][3*j+b][v]
                    for a in range(3) for b in range(3))

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
