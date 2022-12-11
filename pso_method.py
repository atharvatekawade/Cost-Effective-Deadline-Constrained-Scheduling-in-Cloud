import random
from copy import deepcopy
import math
import config, utils

def pso(D, f = 0):
    w = 0.5
    c1 = 2
    c2 =2
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
    V = []
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

    mapping = {}
    ctr = 0
    for t in range(max_tasks):
        for pr in range(len(config.center)):
            for cl in range(len(config.center[pr])):
                mapping[ctr] = [pr, cl, t]
                ctr += 1

    assert(ctr == len(mapping))
    for pt in range(p):
        particle = []
        v = []

        if(random.uniform(0, 1) < f):
            particle = utils.my_algo(D, mapping)
        else:
            for j in range(len(config.graph)):
                particle.append(random.randint(0, len(mapping)-1))

        for j in range(len(config.graph)):
            v.append(random.randint(50, 100)/100)
        
        s, c = utils.simulate_pso(particle, mapping)
        
        X.append([deepcopy(particle), s, c])
        V.append(v)
        pb.append([deepcopy(particle), s, c])

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
        for i in range(p):
            x = deepcopy(X[i][0])
            v = deepcopy(V[i])
            min_val = 1
            for j in range(len(X[i][0])):
                temp = X[i][0][j]
                try:
                    X[i][0][j] = math.floor(X[i][0][j] + V[i][j])
                except:
                    s, c = utils.simulate_pso(g[0], mapping)
                    return  s, c

                V[i][j] = w*V[i][j] + c1*r1*(pb[i][0][j] - temp) + c2*r2*(g[0][j] - temp)

                if(X[i][0][j] < 0):
                    min_val = min(min_val, abs(x[j]/v[j]))
                
                elif(X[i][0][j] >= len(mapping)):
                    min_val = min(min_val, abs((len(mapping)-1-x[j])/v[j]))
            
            for j in range(len(X[i][0])):
                try:
                    X[i][0][j] = math.floor(x[j] + min_val*v[j])
                except:
                    s, c = utils.simulate_pso(g[0], mapping)
                    return  s, c
                
                if(X[i][0][j] < 0):
                    X[i][0][j] = 0
                
                elif(X[i][0][j] >= len(mapping)):
                    X[i][0][j] = len(mapping)-1

            s, c = utils.simulate_pso(X[i][0], mapping)  

            if(pb[i][1] <= D and s <= D and c <= pb[i][2]):
                pb[i] = [deepcopy(X[i][0]), s, c]

            elif(pb[i][1] > D and s <= D):
                pb[i] = [deepcopy(X[i][0]), s, c]
            
            elif(pb[i][1] > D and s > D and s < pb[i][1]):
                pb[i] = [deepcopy(X[i][0]), s, c]
            
            elif(pb[i][1] > D and s == pb[i][1] and c < pb[i][2]):
                pb[i] = [deepcopy(X[i][0]), s, c]
            
            if(g[1] <= D and s <= D and c < g[2]):
                g = [deepcopy(X[i][0]), s, c]
            
            elif(g[1] > D and s <= D):
                g = [deepcopy(X[i][0]), s, c]
            
            elif(g[1] > D and s > D and s < g[1]):
                g = [deepcopy(X[i][0]), s, c]
            
            elif(g[1] > D and s == g[1] and c < g[1]):
                g = [deepcopy(X[i][0]), s, c]
    
    s, c = utils.simulate_pso(g[0], mapping)
    return  s, c