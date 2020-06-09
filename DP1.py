def minimum_cost(T, D, C, H, V, max_demand, total_demand):
    for t in range(1, T + 1):
        for y in range(total_demand + 1):
            min_qty = max(D[T - t] - y, 0)                                                                              # 
            max_qty = total_demand - y + D[T - t]

            if t == 1:
                min_cost = 9999999
                opt_x = -1
                for x in range(min_qty, max_demand + 1):
                    cost = C[T - t] * x + H * (y + x - D[T - t]) 
                    if cost < min_cost: 
                        min_cost = cost
                        opt_x = x
            else: 
                min_cost = 9999999
                opt_x = -1
                for x in range(min_qty, max_qty + 1):
                    cost = V[t - 1][y + x - D[T - t]] + C[T - t] * x + H * (y + x - D[T - t])
                    if cost < min_cost: 
                        min_cost = cost
                        opt_x = x
    
            V[t][y] = min_cost

def print_min_cost(V):
    for t in range(len(V)):
        for y in range(len(V[0])):
            print(V[t][y], end = " ")
        print()
    print()

period = 4
D = [3, 2, 1, 2]
C = [4, 6, 4, 6]
H = 1
y_init = 0
V = [0] * (period + 1)
for i in range(len(V)):
    V[i] = [0] * (sum(D) + 1)
print_min_cost(V)
minimum_cost(period, D, C, H, V, max(D), sum(D))
print_min_cost(V)


