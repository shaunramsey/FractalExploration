#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:41:41 2018

@author: Michelle
"""

import matplotlib.pyplot as plt
import numpy as np

x = .5  #seed 
hori_x_range = np.arange(.5, 1, .001) #range of c-values to iterate over

for i in range (1, 100): #throws away first 100 
    x = np.multiply(hori_x_range, (1 - (2 * abs(x- .5) ) ) ) 

for j in range(1,100): #goes through next 100 iterations, where the orbit has settled down by now
    x = np.multiply(hori_x_range, (1 - (2 * abs(x- .5) ) ) )    #x mapped onto x squared plus c
    plt.scatter(hori_x_range, x, s = 1) #plots the orbit

plt.xlabel("c")
plt.ylabel("orbits")
plt.title("Bifurcation Diagram")
plt.show()
