import subprocess, re, types


__var_num = 1 #false available per default
def new_var(k = 1):
    global __var_num
    __var_num += k
    return __var_num - (k-1)

def v_false():
    return 1

# return a dims sized multi-dimensional array of variables
def get_vars(*dims):
    if len(dims) == 1:
        return [new_var() for i in range(dims[0])]
    return [get_vars(*dims[1:]) for i in range(dims[0])]

# this makes using *x functions much more convenient
def __simplify_varargs(x):
    if len(x) == 1 and (isinstance(x[0], types.GeneratorType)  #判断x[0]是否为 GeneratorType（动态）类型。
            or isinstance(x[0], list)):
        return list(x[0])
    return list(x)

__clauses = []

def clause(*x):
    x = __simplify_varargs(x)
    global __clauses
    __clauses.append(" ".join(map(str, x))+" 0")  #map(f,l) 将l列表的每个值进行f操作。    。join():将生成的值进行“ ”操作
clause(-1) #false is false :)

#given variables, define v <==> (vars(0) or var(1) or ..)
def disjunction(*vars):
    vars = __simplify_varargs(vars)
    v = new_var()
    # =>
    clause([-v] + vars)
    # <=
    for vi in vars:
        clause(-vi, v)
    return v

# linear sized encoding, using |vars| extra variables
def at_most_one(*vars):
    vars = __simplify_varargs(vars)
    k = len(vars)
    if k <= 1:
        return
    if 3*k - 2 < k*(k-1)/2:
        a = get_vars(k)
        clause(-vars[0], a[0]) # vars_0 => a_0
        for i in range(1,k):
            clause(-vars[i], a[i]) # vars_i => a_i
            clause(-a[i-1], a[i])  # a_(i-1) => a_i
            clause(-a[i-1], -vars[i])  # enforce <= 1
    else: #quadratisches encode ist kuerzer
        for i in range(k):
            for j in range(i+1, k):
                clause(-vars[i], -vars[j])

def exactly_one(*vars):
    vars = __simplify_varargs(vars)
    clause(vars)
    at_most_one(vars)

# exactly k of the variable in var can be true
def sum_constraint(k, *vars):
    vars = __simplify_varargs(vars)
    if len(vars) == 0:
        if k != 0:
            clause(v_false())
        return
    def add (a, b):
        n = max(len(a), len(b))
        while len(a) < n:
            a.append(v_false())
        while len(b) < n:
            b.append(v_false())
        r = [new_var() for i in range(n+1)]
        c = [0] + [new_var() for i in range(n-1)] + [r[-1]]

        #c1 <==> a0 & b0
        # =>
        clause(-c[1], a[0])
        clause(-c[1], b[0])
        # <=
        clause(-a[0], -b[0], c[1])

        # r0 <==> a0 ^ b0
        # =>
        clause(-r[0], a[0], b[0])
        clause(-r[0],-a[0], -b[0])
        # <=
        clause(r[0], -a[0], b[0])
        clause(r[0], a[0], -b[0])

        for i in range(1, n):
            # c_(i+1) <==> (a_i & b_i) | (a_i & c_i) | (b_i & c_i)
            # =>
            clause(-c[i+1], a[i], b[i], c[i])
            clause(-c[i+1], -a[i], b[i], c[i])
            clause(-c[i+1], a[i], -b[i], c[i])
            clause(-c[i+1], a[i], b[i], -c[i])

            # <=
            clause(-a[i], -b[i], c[i+1])
            clause(-a[i], -c[i], c[i+1])
            clause(-b[i], -c[i], c[i+1])

            # r_i <==> a_i ^ b_i ^ c_i
            # =>
            clause(-r[i], a[i], b[i], c[i])
            clause(-r[i], a[i], -b[i], -c[i])
            clause(-r[i], -a[i], b[i], -c[i])
            clause(-r[i], -a[i], -b[i], c[i])
            # <=
            clause(r[i], -a[i], -b[i], -c[i])
            clause(r[i], -a[i], b[i], c[i])
            clause(r[i], a[i], -b[i], c[i])
            clause(r[i], a[i], b[i], -c[i])
        return r
    # add vars using divide & conquer
    def dc(l, r):
        if l == r:
            return [vars[l]]
        return add(dc(l, (l+r)/2), dc((l+r)/2+1,r))

    cake = dc (0, len(vars)-1)
    # == k
    if 2**len(cake) - 1 < k:
        clause(v_false())
    else:
        for i in range(len(cake)):
            if k & (1 << i):
                clause(cake[i])
            else:
                clause(-cake[i])

def get_num_vars():
    global __var_num
    return __var_num

def print_formula_stats():
    global __clauses
    print("%d variables, %d clauses" % (get_num_vars(), len(__clauses)))

def get_encoding():
    global __clauses
    return("\n".join(["p cnf %d %d" % (get_num_vars(), len(__clauses))]
            + __clauses))

__model = []
#true if satisfiable   #solver = "picosat"
def sat_solve(solver = "cadical", args = [], stats = True):
    if stats:
        print("solving formula:",
        print_formula_stats())
    p = subprocess.Popen([solver] + args,
            stdout = subprocess.PIPE, stdin = subprocess.PIPE)
    res = p.communicate(input = get_encoding().encode())[0]
    global __model
    __model = []
    for line in res.split(str.encode('\n')):
        if len(line) > 0 and line[0] == 'v':
            __model += map(int, re.findall("-?\d+", line))
    if len(__model) == 0:
        return False
    del __model[-1]
    assert len(__model) == get_num_vars()
    return True

def model_val(v):
    global __model
    assert 1 <= v <= get_num_vars()
    return __model[v-1] > 0













