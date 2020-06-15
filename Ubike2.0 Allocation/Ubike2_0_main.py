from Ubike2_0_config import *
from Ubilke2_0_func import *


# Variable
V = [ 0 for i in range(Period +1)]

# Calculate
for i in range(len(V)):												# set stop for every period
    V[i] = [0] * (PillarNum)




print_min_cost(V)
minimum_cost(Period, CostPerBike, CosrPerStop, PillarNum,V)
print_min_cost(V)


