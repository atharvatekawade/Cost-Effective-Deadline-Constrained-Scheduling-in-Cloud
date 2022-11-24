import random
import numpy as np

def init():
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





