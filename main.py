import random
import config, utils, pso_method, adpsoga, cedces
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

#-db DATABASE -u USERNAME -p PASSWORD -size 20000
parser.add_argument("-num", dest = "num", default = 24, type=int)
parser.add_argument("-itr", dest = "itr", default = 5, type=int)
parser.add_argument("-p", dest = "p", default = 6, type=int)
parser.add_argument("-D", dest = "D", default = 5, type=float)
parser.add_argument("-smin", dest = "smin", default = 10, type=int)
parser.add_argument("-smax", dest = "smax", default = 10**3, type=int)

args = parser.parse_args()

config.providers = args.p
config.smin = args.smin
config.smax = args.smax

costs = [0, 0, 0]
spans = [0, 0, 0, 0]
fails = [0, 0, 0]
deviation = [0, 0, 0]
den = [0, 0, 0]

for gen in range(args.itr):
    print("Iteration: ", gen+1)
    config.init(args.num)

    min_span = utils.heft()
    D = args.D * min_span
    print("Deadline:", D)
    spans[3] += D

    s, c = pso_method.pso(D)   
    print(f"Graph size: {len(config.graph)} Algo: PSO Span: {s} Cost: {c}") 
    costs[0] += c
    spans[0] += s

    if(s > D):
        fails[0] += 1
        deviation[0] += (s-D)
        den[0] += D

    s, c = adpsoga.gpso(D)   
    print(f"Graph size: {len(config.graph)} Algo: ADPSOGA Span: {s} Cost: {c}") 
    costs[1] += c
    spans[1] += s

    if(s > D):
        fails[1] += 1
        deviation[1] += (s-D)
        den[1] += D
  
    s, c = cedces.my_pso(D, 1)   
    print(f"Graph size: {len(config.graph)} Algo: CEDCES Span: {s} Cost: {c}")
    costs[2] += c 
    spans[2] += s

    if(s > D):
        fails[2] += 1 
        deviation[2] += (s-D)
        den[2] += D

    print("\n")
 
for i in range(len(costs)):
    spans[i] = spans[i]/args.itr
    costs[i] = costs[i]/args.itr
    if(den[i] != 0):
        deviation[i] = deviation[i]/den[i]

print(f"Graph size: {len(config.graph)} Algo: PSO Span: {spans[0]} Cost: {costs[0]} Fails: {fails[0]} Deviation: {deviation[0]}")
print(f"Graph size: {len(config.graph)} Algo: ADSPOGA Span: {spans[1]} Cost: {costs[1]} Fails: {fails[1]} Deviation: {deviation[1]}")
print(f"Graph size: {len(config.graph)} Algo: CEDCES Span: {spans[2]} Cost: {costs[2]} Fails: {fails[2]} Deviation: {deviation[2]}")

algos = ["PSO", "ADPSOGA", "CEDCES"]

plt.subplot(1, 2, 1)
plt.bar(algos, costs, color ='blue')
plt.xlabel("Algorithms")
plt.ylabel("Cost($)")
plt.title("Cost comparison")

plt.subplot(1, 2, 2)
plt.bar(algos + ["Deadline"], spans, color ='red')
plt.xlabel("Algorithms")
plt.ylabel("Makespan(sec)")
plt.title("Makespan comparison")

plt.show()