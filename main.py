import random
import config, utils, pso_method, adpsoga, cedces
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-ff", dest = "ff", default = "Montage_25.xml", type=str)
parser.add_argument("-itr", dest = "itr", default = 1, type=int)
parser.add_argument("-aws", dest = "aws", default = 2, type=int)
parser.add_argument("-gcp", dest = "gcp", default = 2, type=int)
parser.add_argument("-ma", dest = "ma", default = 2, type=int)
parser.add_argument("-D", dest = "D", default = 5, type=float)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**3, type=int)

args = parser.parse_args()

config.smin = args.smin
config.smax = args.smax


dd = [1.5, 2, 5, 8, 15]
fracs = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
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

    # for gen in range(args.itr):
    #     for i in range(len(fracs)):
    #         s, c = cedces.my_pso(D, f = 1, f1 = fracs[i])   
    #         print(f"Graph size: {len(config.graph)} Algo: CEDCES-{fracs[i]} Span: {s} Cost: {c}")
    #         costs[r][i] += c 
    #         spans[r][i] += s

    #         if(s > D):
    #             fails[r][i] += 1 
    #             deviation[r][i] += (s-D)
    #             den[r][i] += D


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

# for i in range(len(frac)):
#     print(f"Graph size: {len(config.graph)} Algo: CEDCES-{frac[i]} Span: {spans[i]} Cost: {costs[i]} Fails: {fails[i]} Deviation: {deviation[i]}")

# print(f"Graph size: {len(config.graph)} Algo: PSO Span: {spans[0]} Cost: {costs[0]} Fails: {fails[0]} Deviation: {deviation[0]}")
# print(f"Graph size: {len(config.graph)} Algo: ADSPOGA Span: {spans[1]} Cost: {costs[1]} Fails: {fails[1]} Deviation: {deviation[1]}")
# print(f"Graph size: {len(config.graph)} Algo: CEDCES Span: {spans[2]} Cost: {costs[2]} Fails: {fails[2]} Deviation: {deviation[2]}")



# algos = ["PSO", "ADPSOGA", "CEDCES"]

# plt.subplot(1, 2, 1)
# plt.bar(algos, costs, color ='blue')
# plt.xlabel("Algorithms")
# plt.ylabel("Cost($)")
# plt.title("Cost comparison")

# plt.subplot(1, 2, 2)
# plt.bar(algos + ["Deadline"], spans, color ='red')
# plt.xlabel("Algorithms")
# plt.ylabel("Makespan(sec)")
# plt.title("Makespan comparison")

# plt.show()