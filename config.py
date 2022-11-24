import random
import numpy as np

def init(n):
    global providers
    global center
    global graph
    global prices
    global fixed_price
    global size
    global smin
    global smax
    global inter
    global ext
    global boot_time
    global topological_levels

    providers = 6
    center = []
    graph = []
    prices = []
    fixed_price = []
    size = []
    smin = 10
    smax = 10**3
    inter = 20
    ext = 100
    boot_time = 97
    topological_levels = []

    unit_price = 0.001
    center = []
    prices = []
    size = []

    for i in range(int(providers/3)):
        fixed_price.append([])
            
    for i in range(providers):
        vms = random.randint(1, 32)
        center.append([])
        prices.append([])
        j = 0
        while(j < vms):
            cap = random.randint(1, 32)
            if(cap not in center[i]):
                center[i].append(cap)
                c = unit_price*center[i][j]
                c = np.random.normal(loc=c, scale=c/10) 
                if(i%3 == 0):
                    c = c*60*(1-random.randint(1,3)/10000)
                    prices[i].append(round(c,2))
                            
                else:
                    prices[i].append(round(c,2))
                    if(i%3 == 2):
                        tp = int((i-2)/3)
                        fixed_price[tp].append(c*random.randint(11, 14)/10)
                j += 1


    graph = []
    nodes = int((n-4)/4)

    for i in range(n):
        graph.append([])
        for _ in range(n):
            graph[i].append(0)

    curr_lvl = [i+1 for i in range(0, nodes)]

    for i in curr_lvl:
        graph[0][i] = random.randint(smin, smax)
    
    for _ in range(3):
        next_lvl = [curr_lvl[i]+nodes for i in range(len(curr_lvl))]

        for i in range(len(curr_lvl)):
            graph[curr_lvl[i]][next_lvl[i]] = random.randint(smin, smax)
        
        curr_lvl = next_lvl[:]
    
    for i in curr_lvl:
        graph[i][n-3] = random.randint(smin, smax)
    
    graph[n-3][n-2] = random.randint(smin, smax)
    graph[n-2][n-1] = random.randint(smin, smax)


    vertices = []
    for i in range(1, len(graph)):
        flag = 0
        for j in range(len(graph)):
            if(graph[j][i] > 0):
                flag = 1
                break
        
        if(flag == 0):
            vertices.append(i)
    
    for i in vertices:
        graph[0][i] = 1


    for i in range(len(graph)):
        for j in range(len(graph)):
            if(graph[i][j] > 0 and i >= j):
                print("Wrong graph levels", i, j)
                quit()

    topological_levels = [0 for _ in range(len(graph))]

    for i in range(1, len(graph)):
        max_lvl = 0
        for j in range(len(graph)):
            if(graph[j][i] > 0 and topological_levels[j] > max_lvl):
                max_lvl = topological_levels[j]

        topological_levels[i] = max_lvl+1

    for i in range(len(graph)):
        size.append(random.randint(smin, smax))


