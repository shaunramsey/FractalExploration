# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

x = .25 #seed
r = np.arange(1, 4, .001) #range of c-values to iterate over, step size 0.001

# going through first 500 iterations to throw away
for i in range (1, 500): 
    x = np.multiply(x, r) * np.subtract(1,x)

# goes through next 100 iterations - the orbit has settled down by now
for j in range(1, 100):
    x = np.multiply(x, r) * np.subtract(1,x)
    plt.scatter(r, x, s = 1)  #plot c and x

plt.grid(True)
plt.xlabel("r")
plt.ylabel("orbits")
plt.title("Bifurcation of logistic equation (x = rx(1-x))")
plt.show()