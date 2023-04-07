import random
import config, utils, pso_method, adpsoga, cedces
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("-ff", dest = "ff", default = "Montage_25.xml", type=str)
parser.add_argument("-itr", dest = "itr", default = 1, type=int)
parser.add_argument("-aws", dest = "aws", default = 2, type=int)
parser.add_argument("-gcp", dest = "gcp", default = 2, type=int)
parser.add_argument("-ma", dest = "ma", default = 2, type=int)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**3, type=int)

args = parser.parse_args()

config.smin = args.smin
config.smax = args.smax


dd = [1.5, 2, 5, 8, 15]
algos = ["PSO", "ADPSOGA", "CEDCES"]
costs = [[0 for _ in range(len(algos))] for _ in range(len(dd))]
spans = [[0 for _ in range(len(algos)+1)] for _ in range(len(dd))]
fails = [[0 for _ in range(len(algos))] for _ in range(len(dd))]
deviation = [[0 for _ in range(len(algos))] for _ in range(len(dd))]
den = [[0 for _ in range(len(algos))] for _ in range(len(dd))]

config.init(args.aws, args.ma, args.gcp, args.ff)
min_span = utils.heft()

for r in range(len(dd)):
    D = dd[r] * min_span
    print("Deadline:", D)
    for gen in range(args.itr):
        s, c = pso_method.pso(D)   
        print(f"Graph size: {len(config.graph)} Algo: PSO Span: {s} Cost: {c}") 
        costs[r][0] += c
        spans[r][0] += s

        if(s > D):
            fails[r][0] += 1
            deviation[r][0] += (s-D)
            den[r][0] += D

        s, c = adpsoga.gpso(D)   
        print(f"Graph size: {len(config.graph)} Algo: ADPSOGA Span: {s} Cost: {c}") 
        costs[r][1] += c
        spans[r][1] += s

        if(s > D):
            fails[r][1] += 1
            deviation[r][1] += (s-D)
            den[r][1] += D
        
        s, c = cedces.my_pso(D, f = 1, f1 = 0.9)   
        print(f"Graph size: {len(config.graph)} Algo: CEDCES Span: {s} Cost: {c}")
        costs[r][2] += c 
        spans[r][2] += s

        if(s > D):
            fails[r][2] += 1 
            deviation[r][2] += (s-D)
            den[r][2] += D

        print("\n")
 
    for i in range(len(costs[r])):
        spans[r][i] = spans[r][i]/args.itr
        costs[r][i] = costs[r][i]/args.itr
        if(den[r][i] != 0):
            deviation[r][i] = deviation[r][i]/den[r][i]
    
    spans[r][-1] = D

print("Spans:", spans)
print("Costs:", costs)
print("Deviation:", deviation)
print("Fails:", fails)
