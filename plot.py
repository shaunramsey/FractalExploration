# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:58:24 2018

@author: Ramsey
"""

import matplotlib.pyplot as plt
import numpy as np

def x(xo, param, iters, plt):
    for i in range(iters):
        #this is the function that we're plotting...
        xo = xo*xo + param
    pts = []
    for i in range(iters):
        #the function we're plotting
        #it is repeated here -- perhaps should place elsewhere
        xo = xo*xo + param
        plt.scatter(param, xo, s=1)


# Fixing random state for reproducibility
np.random.seed(19680801)



iters = 100
stored = 100
param_low = -2
param_high = 0.25
totalsteps = 10.0

step = (param_high - param_low) / totalsteps
print("totalsteps=", totalsteps)
i = param_low
while i < param_high:
    print("i is now:", i)
    pts = x(1, i, iters, plt)
    i = i + step

#N = 100
#r0 = 0.6
#x = 0.9 * np.random.rand(N)
#y = 0.9 * np.random.rand(N)
#area = (20 * np.random.rand(N))**2  # 0 to 10 point radii
#c = np.sqrt(area)
#r = np.sqrt(x * x + y * y)
#area1 = np.ma.masked_where(r < r0, area)
#area2 = np.ma.masked_where(r >= r0, area)
#plt.scatter(x, y, s=area1, marker='^', c=c)
#plt.scatter(x, y, s=area2, marker='o', c=c)
# Show the boundary between the regions:
#theta = np.arange(0, np.pi / 2, 0.01)
#plt.plot(r0 * np.cos(theta), r0 * np.sin(theta))

plt.show()