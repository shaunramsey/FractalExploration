# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:06:47 2018

@author: Ramsey
"""

import numpy as np
import matplotlib.pyplot as plt
# get a bifurcation plot of x^2+c
# start with x = whatever, maybe 0?

lower_bound = -2
upper_bound = .25
step_size = .0001
initial_iterations = 100
final_iterations = 100
x_init = 0 # could change this to be random

c = np.arange(lower_bound, upper_bound, step_size)
x = x_init

# let things settle to a steady state
for i in range(initial_iterations):
    x = np.multiply(x, x) + c

for i in range(final_iterations):
    x = np.multiply(x, x) + c 
    plt.scatter(c, x, s=1)

plt.show()
    
    
