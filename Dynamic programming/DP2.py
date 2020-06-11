import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
# from numpy.random import normal as normal
from scipy.stats import norm as norm


def generateDist(N, prob):
	dist = np.zeros(N + 1)
	for i in range(N + 1):
		dist[i] = binom.pmf(i, N, prob)
	print(dist)
	print(np.sum(dist))
	return dist

def dp(p, c, N, T, prob):
	V=np.zeros((N+1, T+1))
	Y=np.zeros((N+1, T+1))

	dist = generateDist(N, prob)

	for t in range(1,T+1):
		for q in range(N+1):
			# print(t,q)
			cand=[]
			for yt in range(q, N+1):

				pi=0
				for x in range(yt+1):
					pi+=x*dist[x]
				for x in range(yt+1, N+1):
					pi+=yt*dist[x]
				pi=pi*p-(yt-q)*c

				e=0
				for x in range(yt+1):
					e+=V[yt-x][t-1]*dist[x]
				for x in range(yt+1, N+1):
					e+=V[0][t-1]*dist[x]
				print(e)
				cand.append((pi+e, yt))
			pick=max(cand)
			V[q][t]=pick[0]
			Y[q][t]=pick[1]
			# print(V)
			# print(max(cand))
	return Y, V

def drawVq(N,Y,V,t):
	x=[i for i in range(N+1)]
	y=[V[i][t] for i in range(N+1)]
	plt.style.use('ggplot')
	plt.plot(x,y, marker='o', color='blue')
	plt.xlabel("on-hand inventory before ordering")
	plt.ylabel("expected profit to the end")
	plt.title("period = " + str(t))
	plt.show()
def drawVt(T,Y,V,q):
	x=[i for i in range(T+1)]
	y=[V[q][i] for i in range(T+1)]
	plt.style.use('ggplot')
	plt.plot(x,y, marker='o', color='blue')
	plt.xlabel("period")
	plt.ylabel("expected profit to the end")
	plt.title("on-hand inventory before ordering = " + str(q))
	plt.show()
def drawYq(N,Y,V,t):
	x=[i for i in range(N+1)]
	y=[Y[i][t] for i in range(N+1)]
	plt.style.use('ggplot')
	plt.plot(x,y, marker='o', color='blue')
	plt.xlabel("on-hand inventory before ordering")
	plt.ylabel("on-hand inventory after ordering")
	plt.title("period = " + str(t))
	plt.show()
def drawYt(T,Y,V,q):
	x=[i for i in range(T+1)]
	y=[Y[q][i] for i in range(T+1)]
	plt.style.use('ggplot')
	plt.plot(x,y, marker='o', color='blue')
	plt.xlabel("period")
	plt.ylabel("on-hand inventory after ordering")
	plt.title("on-hand inventory before ordering = " + str(q))
	plt.show()

def print_nicely(V):
    for t in range(len(V)):
        for y in range(len(V[0])):
            print(V[t][y], end = " ")
        print()
    print()



# def dp(p, c, N, T, prob):
Y,V=dp(5, 2, 10, 5, 0.3)
print_nicely(Y)
print_nicely(V)
# def draw(N,V,t):
drawVt(5,Y,V,4)
drawVq(10,Y,V,2)
drawYt(5,Y,V,1)
drawYq(10,Y,V,2)





	