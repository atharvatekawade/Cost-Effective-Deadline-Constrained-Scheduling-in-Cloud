import random
import math
import config

def ranks():
    l = [[i, 0] for i in range(len(config.graph))]
    s = 0
    m = 0
    for pr in range(len(config.center)):
        for cl in range(len(config.center[pr])):
            m = m + 1/config.center[pr][cl]
            s += 1
    
    for i in range(len(config.graph)-1, -1, -1):
        l[i][1] = l[i][1] + m*config.size[i]/s
        ct = 0
        for j in range(len(config.graph)):
            if(config.graph[i][j] > 0):
                ct = max(ct, l[j][1] + config.graph[i][j]/config.ext)
        
        l[i][1] = l[i][1] + ct
    
    l.sort(key=lambda x: x[1], reverse=True)
    l = [l[i][0] for i in range(len(config.graph))]

    return l

def add_task(task, order, l):
    flag = 0
    for j in range(len(config.graph)):
        if(config.graph[j][task] > 0 and j not in order):
            add_task(j, order, l)
    
    order.append(task)
    l.remove(task)

def precedence(order):
    l = [i for i in range(len(config.graph))]
    while(len(l) > 0):
        task = random.choice(l)
        add_task(task, order, l)

    for i in range(len(config.graph)):
        if(i not in order):
            print("Computed order missing task",i)
            quit()

    return order

def repair(x, max_tasks):
    for i in range(len(x[0])):
        if(x[0][i] < 0):
            x[0][i] = 0
        if(x[0][i] >= len(config.center)):
            x[0][i] = len(config.center) - 1
        
        if(x[1][i] < 0):
            x[1][i] = 0
        if(x[1][i] >= len(config.center[x[0][i]])):
            x[1][i] = len(config.center[x[0][i]]) - 1
        
        if(x[2][i] < 0):
            x[2][i] = 0
        
        if(x[2][i] >= max_tasks):
            x[2][i] = max_tasks-1
    
    return x

def met():
    R = {}
    M = {}

    pr1 = -1
    cl1 = -1

    for pr in range(len(config.center)):
        for cl in range(len(config.center[pr])):
            if(config.center[pr1][cl1] < config.center[pr][cl]):
                pr1 = pr
                cl1 = cl
    
    for i in range(len(config.graph)):
        exec_time = config.size[i]/config.center[pr1][cl1]
        s = config.boot_time
        transfer = 0

        for j in range(len(config.graph)):
            if(config.graph[j][i] > 0):
                s = max(s, M[j][2])
            
            if(config.graph[j][i] > 0):
                transfer += config.graph[j][i]/config.inter
        
        f = s + exec_time + transfer
        id = random.randint(1, 10**9)
        R[id] = [pr1, cl1, s, f]
        M[i] = [id, s, f]
    
    makespan = 0
    for task in M:
        makespan = max(makespan, M[task][2])
    
    cost = 0
    for id in R:
        time = R[id][3] - R[id][2]
        pr = R[id][0]
        cl = R[id][1]

        if(pr < config.aws_providers):
            slots = math.ceil(time/3600)
        elif(pr < config.aws_providers + config.ma_providers):
            slots = math.ceil(time/60)
        else:
            cost += config.fixed_price[pr-config.aws_providers-config.ma_providers][cl]
            slots = max(math.ceil(time/60) - 10, 0)
            
        cost += slots*config.prices[pr][cl]

    return makespan, cost

def simulate_pso(particle, mapping, l = []):
    if(l == []):
        l = [i for i in range(len(config.graph))]

    R = {}
    M = {}
    for i in range(len(l)):
        pr1, cl1, _ = mapping[particle[l[i]]]
        exec_time = config.size[l[i]]/config.center[pr1][cl1]
        s = 0
        transfer = 0

        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                s = max(s, M[j][2])
                
            if(config.graph[l[i]][j] > 0):
                pr2, _, _ = mapping[particle[j]]
                    
                if(particle[l[i]] == particle[j]):
                    continue
                    
                elif(pr1 == pr2):
                    transfer += config.graph[l[i]][j]/config.inter
                    
                else:
                    transfer += config.graph[l[i]][j]/config.ext
            
        if(particle[l[i]] in R):
            s = max(s, R[particle[l[i]]][3])
            
        else:
            s = max(s, config.boot_time)
            R[particle[l[i]]] = [pr1, cl1, s-config.boot_time, s]

        f = s + exec_time + transfer
        M[l[i]] = [particle[l[i]], s, f]
        R[particle[l[i]]][3] = f
        
    makespan = 0
    for task in M:
        makespan = max(makespan, M[task][2])
        
    cost = 0
    for id in R:
        time = R[id][3] - R[id][2]
        if(time < 0):
            print("Something went wrong negative time", R[id][3], R[id][2])
            quit()

        pr = R[id][0]
        cl = R[id][1]

        if(pr < config.aws_providers):
            slots = math.ceil(time/3600)
        elif(pr < config.aws_providers + config.ma_providers):
            slots = math.ceil(time/60)
        else:
            slots = max(math.ceil(time/60)-10, 0)
            cost += config.fixed_price[pr-config.aws_providers-config.ma_providers][cl]
                
        cost += slots*config.prices[pr][cl]
    
    for i in range(len(config.graph)):
        pr1 = R[particle[i]][0]
        for j in range(len(config.graph)):
            pr2 = R[particle[j]][0]
            if(config.graph[i][j] > 0):
                data = config.graph[i][j]/1000
                if(pr1 == pr2):
                    continue
                
                if(pr1 < config.aws_providers):
                    if(pr2 < config.aws_providers):
                        cost += 0.02*data
                    elif(data <= 100):
                        cost += 0
                    elif(data <= 10*1000):
                        cost += 0.09*data
                    elif(data <= 40*1000):
                        cost += 0.085*data
                    elif(data <= 100*1000):
                        cost += 0.07*data
                    else:
                        cost += 0.05*data
                        
                elif(pr1 < config.aws_providers + config.ma_providers):
                    if(pr2 < config.aws_providers + config.ma_providers):
                        cost += 0.08*data
                    elif(data <= 100):
                        cost += 0
                    elif(data <= 10*1000):
                        cost += 0.11*data
                    elif(data <= 40*1000):
                        cost += 0.075*data
                    elif(data <= 100*1000):
                        cost += 0.07*data
                    else:
                        cost += 0.06*data
                        
                else:
                    if(pr2 >= config.aws_providers + config.ma_providers):
                        cost += 0.05*data
                    elif(data <= 1*1000):
                        cost += 0.19*data
                    elif(data <= 10*1000):
                        cost += 0.18*data
                    else:
                        cost += 0.15*data
    
    return makespan, cost

def heft():
    l = ranks()
    R = {}
    M = {}
    makespan = 0

    mapping = {}
    ctr = 0
    for t in range(len(config.graph)):
        for pr in range(len(config.center)):
            for cl in range(len(config.center[pr])):
                mapping[ctr] = [pr, cl, t]
                R[ctr] = [pr, cl, 0, 0]
                ctr += 1

    assert(ctr == len(mapping))

    # s, c = simulate_pso(particle, mapping, orders[it])
    for i in range(len(l)):
        min_vm = -1
        min_fin = float('inf')
        for vm in mapping:
            s = 0
            if(R[vm][3] != 0):
                s = R[vm][3]
                pr = R[vm][0]
                cl = R[vm][1]
                exec_time = config.size[l[i]]/config.center[pr][cl]
                for j in range(len(config.graph)):
                    if(config.graph[j][l[i]] > 0):
                        pr1 = R[M[j][0]][0]
                        if(vm != M[j][0]):
                            if(pr == pr1):
                                s = max(s, M[j][2] + config.graph[j][l[i]]/config.inter)
                            else:
                                s = max(s, M[j][2] + config.graph[j][l[i]]/config.ext)
                        
                        else:
                            s = max(s, M[j][2])
            
            else:
                s = config.boot_time
                pr = R[vm][0]
                cl = R[vm][1]
                exec_time = config.size[l[i]]/config.center[pr][cl]
                for j in range(len(config.graph)):
                    if(config.graph[j][l[i]] > 0):
                        pr1 = R[M[j][0]][0]
                        if(pr == pr1):
                            s = max(s, M[j][2] + config.graph[j][l[i]]/config.inter)
                        else:
                            s = max(s, M[j][2] + config.graph[j][l[i]]/config.ext)
            
            f = s + exec_time
            if(f < min_fin):
                min_vm = vm
                min_fin = f
        
        pr = R[min_vm][0]
        cl = R[min_vm][1]
        s = min_fin - config.size[l[i]]/config.center[pr][cl]

        if(R[min_vm][3] == 0):
            R[min_vm][2] = s - config.boot_time

        R[min_vm][3] = min_fin
        M[l[i]] = [min_vm, s, min_fin]
        makespan = max(makespan, min_fin)
    
    return makespan

def calculate_xet():
    xet = []
    for i in range(len(config.graph)):
        xet.append([])
        for pr in range(len(config.center)):
            xet[i].append([])
            for cl in range(len(config.center[pr])):
                xet[i][pr].append(0)
    
    for i in range(len(config.graph)-1, -1, -1):
        for pr in range(len(config.center)):
            for cl in range(len(config.center[pr])):
                exec_time = config.size[i]/config.center[pr][cl]
                if(i == len(config.graph)-1):
                    xet[i][pr][cl] = exec_time
                
                else:
                    m = 0
                    for j in range(len(config.graph)):
                        if(config.graph[i][j] > 0):
                            m = max(m, xet[j][pr][cl])
                    
                    xet[i][pr][cl] = exec_time + m
    
    return xet

def my_algo(D, mapping, l = []):
    if(l == []):
        l = []
        l = precedence(l)

    xet = calculate_xet()
    particle = []

    for i in range(len(l)):
        particle.append(-1)

    R = {}
    M = {}

    for i in range(len(l)):
        metrics = []
        for vm in range(len(mapping)):
            pr1, cl1, _ = mapping[vm]
            exec_time = config.size[l[i]]/config.center[pr1][cl1]
            s = 0

            for j in range(len(config.graph)):
                if(config.graph[j][l[i]] > 0):
                    pr2, _, _ = mapping[particle[j]]
                    
                    if(vm == particle[j]):
                        s = max(s, M[j][2])
                    
                    elif(pr1 == pr2):
                        s = max(s, M[j][2] + config.graph[j][l[i]]/config.inter)
                    
                    else:
                        s = max(s, M[j][2] + config.graph[j][l[i]]/config.ext)

            if(vm in R):
                s = max(s, R[vm][3])
                
            else:
                s = max(s, config.boot_time)


            price = 0
            if(pr1 < config.aws_providers):
                price = math.ceil((xet[l[i]][pr1][cl1]+config.boot_time)/3600) * config.prices[pr1][cl1]
            elif(pr1 < config.aws_providers + config.ma_providers):
                price = math.ceil((xet[l[i]][pr1][cl1]+config.boot_time)/60) * config.prices[pr1][cl1]
            else:
                price += config.fixed_price[pr1-config.aws_providers-config.ma_providers][cl1]
                rem = max(math.ceil((xet[l[i]][pr1][cl1]+config.boot_time)/60) - 10, 0)
                price = rem * config.prices[pr1][cl1]
                    
            metrics.append([s + xet[l[i]][pr1][cl1], price, vm])

        best_idx = -1
        best_cost = float('inf')

        min_idx = -1
        min_span = float('inf')

        for j in range(len(metrics)):
            if(metrics[j][0] <= D):
                if(metrics[j][1] < best_cost):
                    best_idx = j
                    best_cost = metrics[j][1]
            
            elif(metrics[j][0] < min_span):
                min_idx = j
                min_span = metrics[j][0]
        
        if(best_idx == -1):
            best_idx = min_idx
        
        vm = metrics[best_idx][2]
        particle[l[i]] = vm
        pr1, cl1, _ = mapping[vm]
        exec_time = config.size[l[i]]/config.center[pr1][cl1]

        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                pr2, _, _ = mapping[particle[j]]
                    
                if(vm == particle[j]):
                    continue
                    
                elif(pr1 == pr2):
                    M[j][2] += config.graph[j][l[i]]/config.inter
                    
                else:
                    M[j][2] += config.graph[j][l[i]]/config.ext
                
                R[particle[j]][3] = max(R[particle[j]][3], M[j][2])

        s = 0
        for j in range(len(config.graph)):
            if(config.graph[j][l[i]] > 0):
                s = max(s, M[j][2])

        transfer = 0

        if(particle[l[i]] in R):
            s = max(s, R[particle[l[i]]][3])
                
        else:
            s = max(s, config.boot_time)
            R[particle[l[i]]] = [pr1, cl1, s-config.boot_time, 0]

        f = s + exec_time + transfer
        R[particle[l[i]]][3] = max(R[particle[l[i]]][3], f)
        M[l[i]] = [particle[l[i]], s, f]

    return particle