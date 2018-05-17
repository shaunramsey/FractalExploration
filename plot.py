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
    
plt.show()
