import random
import numpy as np
import xml.etree.ElementTree as ET

def init(aws, ma, gcp, ff):
    global aws_providers
    global ma_providers
    global gcp_providers
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

    aws_providers = aws
    ma_providers = ma
    gcp_providers = gcp

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

    for i in range(gcp_providers):
        fixed_price.append([])
            
    for i in range(aws_providers + ma_providers + gcp_providers):
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
                if(i < aws_providers):
                    c = c*60*(1-random.randint(1,3)/10000)
                    prices[i].append(round(c,2))
                            
                else:
                    prices[i].append(round(c,2))
                    if(i >= aws_providers + ma_providers):
                        fixed_price[i-aws_providers-ma_providers].append(c*random.randint(11, 14)/10)
                j += 1


    dd = {}
    tree = ET.parse(ff)
    root = tree.getroot()

    for child in root:
        if(child.tag[-5:] == "child"):
            pp = child.getchildren()
            c = int(child.attrib['ref'][2:])
            for p in pp:
                pa = int(p.attrib['ref'][2:])

                if pa not in dd:
                    dd[pa] = []

                dd[pa].append(c)
            
            if c not in dd:
                dd[c] = []

    # print(dd)

    graph = []
    for i in range(len(dd) + 2):
        graph.append([])
        for _ in range(len(dd) + 2):
            graph[i].append(0)
    
    for p in dd:
        for c in dd[p]:
            graph[p+1][c+1] = random.randint(smin, smax)
    
    for p in dd:
        if(dd[p] == []):
            graph[p+1][-1] = 1

    for i in dd:
        flag = 0
        for j in dd:
            if(i in dd[j]):
                flag = 1
                break
        
        if(flag == 0):
            graph[0][i+1] = 1


    topological_levels = [0 for _ in range(len(graph))]

    for i in range(1, len(graph)):
        max_lvl = 0
        for j in range(len(graph)):
            if(graph[j][i] > 0 and topological_levels[j] > max_lvl):
                max_lvl = topological_levels[j]

        topological_levels[i] = max_lvl+1

    for i in range(len(graph)):
        size.append(random.randint(smin, smax))


