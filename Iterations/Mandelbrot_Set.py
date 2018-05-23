#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:06:43 2018

@author: Michelle 
"""

# -*- coding: utf-8 -*-
"""
Updated on Wed May 23 10:58:10 2018
- adjusted the orientation of the image to column major
- set origin to bottom left
- switched stepx and stepy in grid so the real and imaginary axis are plotted right
- changed while loops to for loops, deleted if statements
@author Ramsey
Updated on Tue May 22 11:12:14 2018
- switching to 2d numpy arrays and using an implot instead of scatter (huge speed gains)
- pros: gains in speed and fills whole screen with colors
- also added early break when htiting "high" values heading towards infinity"
@author: Ramsey
Created on Mon May 21 15:06:43 2018
@author: Michelle 
"""

#The goal is to graph only the Julia Sets that are connected

import matplotlib.pyplot as plt
import numpy as np

#for a mandelbrot set, you want to change c (the complex number) but keep z the same (the origin 0)


high_num = 200 #above this we consider infinity
neg_num = -200 #below this we consider infinity
lowerbound = -2 #the lower bound of the values we consider on real and i
upperbound = 2  #upper bound of values we considero n real and i
stepsize = 0.01 # increment size between upper and lower bounds
steps = int((upperbound-lowerbound)/stepsize) # how many steps it'll take
iters = 100 #how many iterations we'll take to try to find infinity

grid = np.arange(1,steps*steps+1,1) #gets a grid with right number of pts
grid = grid.reshape((steps,steps)) 

rp = lowerbound 
ip = lowerbound

#filling up our c array with every possible value of complex numbers
for stepx in range(steps): #we want to get all the numbers from the lowerbound to the upperbound
    print("Step:",stepx,"/",steps)
    ip = lowerbound
    for stepy in range(steps):
        c = complex(rp, ip) #this is our initial c 
        z = 0
        for i in range(iters):
            z = np.multiply(z,z) + c  #get the next z from this z 
            if z.real > high_num or z.imag > high_num or z.real < neg_num or z.imag < neg_num:
                break
        grid[stepy][stepx] = i #the graph is colored according to how long it takes to get to infinity
            #by switching the stepy and stepx, you get a set thats oriented like online images -- real axis as x, imaginary as y
        ip += stepsize       
    rp += stepsize
   
    
plt.suptitle("Mandelbrot Set")
plt.xlabel("real")
plt.ylabel("imaginary")
plt.title("c="+str(c))
plt.imshow(grid,cmap="terrain", origin = 'lower')
plt.show()