import random
import math
from copy import deepcopy
import config, utils

def bin_tournament(X, D):
    a = random.randint(0, len(X)-1)
    b = random.randint(0, len(X)-1)

    if(X[a][1] <= D and X[b][1] <= D):
        if(X[a][2] <= X[b][2]):
            return a
        
        else:
            return b
    
    elif(X[a][1] == X[b][1]):
        if(X[a][2] <= X[b][2]):
            return a
        
        else:
            return b
    
    elif(X[a][1] < X[b][1]):
        return a
    
    else:
        return b
    
def my_pso(D, f = 0):
    w = 0.5
    c1 = 2
    c2 =2
    p = 100
    itr = 1000
    min_lvl = min(config.topological_levels)
    max_lvl = max(config.topological_levels)
    ml = -1
    max_tasks = 0

    for i in range(min_lvl, max_lvl+1):
        num_tasks = 0
        for j in range(len(config.graph)):
            if(config.topological_levels[j] == i):
                num_tasks += 1

        if(max_tasks < num_tasks):
            ml = i
            max_tasks = num_tasks
    
    task_levels = []
    for i in range(len(config.graph)):
        if(config.topological_levels[i] == ml):
            task_levels.append(i)
    
    for i in range(ml-1, min_lvl-1, -1):
        for j in range(len(config.graph)):
            if(config.topological_levels[j] == i):
                flag = 0
                for t in task_levels:
                    if(config.graph[j][t] > 0):
                        flag = 1
                        break
                
                if(flag == 0):
                    task_levels.append(j)
    
    for i in task_levels:
        for j in task_levels:
            if(config.graph[i][j] > 0):
                print("Wrong tasks concurrent")
                quit()

    max_tasks = len(task_levels)
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
    wmax = 1.4
    wmin = 0.4
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
            particle = utils.my_algo(0.9*D, mapping)
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
        randm = random.randint(0, p-1)
        w = wmax - gen*(wmax-wmin)/itr
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
            
            if(i == randm):
                j  = random.randint(0, len(X[i][0])-1)
                X[i][0][j] = random.randint(0, len(mapping)-1)

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
    
        a = bin_tournament(X, D)
        b = bin_tournament(X, D)
        k = random.randint(0, len(X[0][0])-1)

        particle = []
        for j in range(len(X[0][0])):
            if(j <= k):
                particle.append(X[a][0][k])
            else:
                particle.append(X[b][0][k])
        
        s, c = utils.simulate_pso(particle, mapping)

        wp1 = -1
        ww1 = 0

        wp2 = -1
        ww2 = 0

        for i in range(len(pb)):
            if(pb[i][1] <= D):
                if(ww1 < pb[i][2]):
                    wp1 = i
                    ww1 = pb[i][2]

            elif(ww2 < pb[i][1]):
                wp2 = i 
                ww2 = pb[i][1]
        
        if(wp1 == -1):
            wp1 = wp2
        
        X[wp1] = [particle, s, c]
        pb[wp1] = [particle, s, c]
        
    s, c = utils.simulate_pso(g[0], mapping)
    return  s, c