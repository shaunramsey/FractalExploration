# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:22:39 2018

@author: Ramsey
"""

import numpy as np
import matplotlib.pyplot as plt
# get a bifurcation plot of x^2+c
# start with x = whatever, maybe 0?

def func(x, c):
    return np.multiply(x,x) + c

lower_bound = -2
upper_bound = .25
step_size = .0001
initial_iterations = 10
final_iterations = 20
x_init = 0 # could change this to be random

#c = 0.4 - 0.325j
c = 0 + 0j

plt.plot([-1,0,1],[0,0,0],c="r")
plt.plot([0,0,0],[-1,0,1],c="r")

# let things settle to a steady state
num_points = 360
for xs in range(num_points):
    yp = [ pow(2,0.5)/2 ]
    xp = []
    x = xs/5 - 1 + 1j*yp[0]
    x = -pow(2,0.5)/2 +1j*yp[0]
    x = np.cos(2*np.pi*xs/ num_points) + np.sin(2*xs*np.pi/num_points) * 1j
    if abs(x) > 1:
        continue
    yp =[]
    yp.append(x.imag)
    xp.append(x.real)
    print(x)
    plt.scatter(x.real,x.imag)
    for i in range(initial_iterations):
        x = func(x, c)
        xp.append(x.real)
        yp.append(x.imag)
        plt.scatter(x.real,x.imag)
    plt.plot(xp,yp)

    

plt.show()
