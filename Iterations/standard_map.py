'''
This code has been modified from https://github.com/williamgilpin/stdmap/blob/master/stdmap_plotter.py
The license for their code is as follows:
The MIT License (MIT)

Copyright (c) 2014 williamgilpin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from numba import jit



#constant for num of iterations
iterations = 100

# constant k describing stochastity of system
k = .4

@jit
def stdequations(points):
    p, theta = points
    newp = np.mod( p + (k * np.sin(theta) ), 2 * np.pi )
    newtheta = np.mod(theta + newp , 2 * np.pi)
    return newp, newtheta   

# creating grid of all initial points
p0 = np.linspace(0, 2*np.pi, 25)
theta0 = np.linspace(0, 2*np.pi, 25)
grid = list() #meshgrid is a list of coordinates
for ii in range(len(p0)):
    for jj in range(len(theta0)):
        grid.append((p0[ii], theta0[jj]))

#iterating through each point in our grid and then finding the trajectory of that point when iterated through our standard equations
for initialval in grid:
    trajectory = [initialval]
    
    for it in range(0, iterations):
        trajectory.append(stdequations(trajectory[it]))
    
    pvals = np.array(trajectory)[:, 0] #convert pvals in trajectory (which is a list) to array
    thetavals = np.array(trajectory)[:, 1]  #convert thetavals in trajectory (a list) to array
    plt.scatter(thetavals, pvals, s =.1)

plt.xlabel("theta")
plt.ylabel("p")
plt.suptitle("Taylor-Chirikov Standard Map")
plt.title("k = " + str(k))
plt.show()