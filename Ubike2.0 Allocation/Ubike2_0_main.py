from Ubike_config import *


# Variable
V = [ 0 for i in range(Period +1)]

# Calculate
for i in range(len(V)):												# set stop for every period
    V[i] = [0] * (StopNum)
    for j in range(lenV[i]):											# set X for every stop, according to their pillarNum
		if j ==1:
			V[i][j] = [PillarNum[j]] * (PillarNum[j])
		else:
			V[i][j] = [0] * (PillarNum[j])




print_min_cost(V)
minimum_cost(period, D, C, H, V, max(D), sum(D))
print_min_cost(V)


