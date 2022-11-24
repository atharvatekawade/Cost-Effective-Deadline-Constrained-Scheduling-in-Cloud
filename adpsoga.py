import random
import math
from copy import deepcopy
import config, utils

def find_key(val, d):
    for key in d:
        if(d[key] == val):
            return key

def crossover_pso(a, b):
    i = random.randint(0, len(a[0])-2)
    j = random.randint(i+1, len(a[0])-1)

    for m in range(len(a)):
        for k in range(i, j):
            a[m][k] = b[m][k]
    
    return a

def mutate_pso(x, max_tasks):
    i = random.randint(0, len(x[0])-1)
    x[0][i] = random.randint(0, len(config.center)-1)
    x[1][i] = random.randint(0, len(config.center[x[0][i]])-1)
    x[2][i] = random.randint(0, max_tasks-1)

    return x

def simulate_gpso(particle, mapping, l = []):
    if(l == []):
        l = [i for i in range(len(config.graph))]
    
    p = []
    for i in range(len(particle[0])):
        r = find_key([particle[0][i], particle[1][i], particle[2][i]], mapping)
        p.append(r)

    s, c = utils.simulate_pso(p, mapping, l)

    return s, c

def div(x, g):
    s = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
            if(x[i][j] != g[i][j]):
                s += 1
    
    return s/(3*len(x[0]))

def gpso(D, f = 0):
    wmax = 1.4
    wmin = 0.2

    c1_start = 0.9
    c1_end = 0.2

    c2_start =0.4
    c2_end = 0.9
    p = 100
    itr = 1000

    max_tasks = 0
    min_lvl = min(config.topological_levels)
    max_lvl = max(config.topological_levels)

    for i in range(min_lvl, max_lvl+1):
        num_tasks = 0
        for j in range(len(config.graph)):
            if(config.topological_levels[j] == i):
                num_tasks += 1
        
        max_tasks = max(max_tasks, num_tasks)
    
    X = []
    pb = []
    g = []

    best_cost = float('inf')
    best_particle = -1

    min_span = float('inf')
    min_particle = -1

    c1 = 2
    c2 = 2
    w = 0.5
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    r3 = random.uniform(0, 1)

    mapping = {}
    ctr = 0
    for t in range(max_tasks):
        for pr in range(len(config.center)):
            for cl in range(len(config.center[pr])):
                mapping[ctr] = [pr, cl, t]
                ctr += 1
    
    assert(ctr == len(mapping))

    for pt in range(p):
        particle = [[], [], []]
        for j in range(len(config.graph)):
            particle[0].append(random.randint(0, len(config.center)-1))
            particle[1].append(random.randint(0, len(config.center[particle[0][j]])-1))
            particle[2].append(random.randint(0, max_tasks-1))
        
        ord = []
        ord = utils.precedence(ord)
        s, c = simulate_gpso(particle, mapping, ord)
        
        X.append([deepcopy(particle), s, c, ord])
        pb.append([deepcopy(particle), s, c, ord])

        if(s <= D):
            if(c < best_cost):
                best_cost = c
                best_particle = pt
        
        elif(s < min_span):
            min_span = s
            min_particle = pt
    
    if(best_particle == -1):
        best_particle = min_particle
    
    g = deepcopy(X[best_particle])


    for gen in range(itr):
        # if(gen%100 == 0):
        #     print("Generation:", gen)
        c1 = c1_start - (c1_start - c1_end)*gen/itr
        c2 = c2_start - (c2_start - c2_end)*gen/itr

        for i in range(p):
            diff = div(X[i][0], g[0])
            w = wmax - (wmax - wmin)*math.exp(diff/(diff-1.01))

            if(r1 < w):
                X[i][0] = mutate_pso(X[i][0], max_tasks)
            
            if(r2 < c1):
                X[i][0] = crossover_pso(X[i][0], pb[i][0])
            
            if(r3 < c2):
                X[i][0] = crossover_pso(X[i][0], g[0])
            
            X[i][0] = utils.repair(X[i][0], max_tasks)
            s, c = simulate_gpso(X[i][0], mapping, X[i][3])  

            if(pb[i][1] <= D and s <= D and c <= pb[i][2]):
                pb[i] = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]

            elif(pb[i][1] > D and s <= D):
                pb[i] = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            elif(pb[i][1] > D and s > D and s < pb[i][1]):
                pb[i] = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            elif(pb[i][1] > D and s == pb[i][1] and c < pb[i][2]):
                pb[i] = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            if(g[1] <= D and s <= D and c < g[2]):
                g = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            elif(g[1] > D and s <= D):
                g = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            elif(g[1] > D and s > D and s < g[1]):
                g = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
            
            elif(g[1] > D and s == g[1] and c < g[1]):
                g = [deepcopy(X[i][0]), s, c, deepcopy(X[i][3])]
    
    s, c = simulate_gpso(g[0], mapping, g[3])
    return  s, c