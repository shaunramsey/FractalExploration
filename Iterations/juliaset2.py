# -*- coding: utf-8 -*-
"""
Updated on Tue May 22 11:12:14 2018
- switching to 2d numpy arrays and using an implot instead of scatter (huge speed gains)
- pros: gains in speed and fills whole screen with colors
- also added early break when htiting "high" values heading towards infinity"
@author: Ramsey

Created on Mon May 21 15:06:43 2018
@author: Michelle 
"""

import matplotlib.pyplot as plt
import numpy as np


c = .4 - .325j #parameter


high_num = 200 #above this we consider infinity
neg_num = -200 #below this we consider infinity
lowerbound = -1.2 #the lower bound of the values we consider on real and i
upperbound = 1.2  #upper bound of values we considero n real and i
stepsize = 0.001 # increment size between upper and lower bounds
steps = int((upperbound-lowerbound)/stepsize) # how many steps it'll take
iters = 100 #how many iterations we'll take to try to find infinity


stepx = 0  #don't change - counter var
stepy = 0 #don't change - counter var

grid = np.arange(1,steps*steps+1,1) #gets a grid with right number of pts
grid = grid.reshape((steps,steps)) #
#print (dy) 
#for a julia set, you want to change z (the initial value) but keep c the same 

rp = lowerbound
ip = lowerbound
broke = False
#filling up our initial zpts array with every possible value of complex numbers
while rp < upperbound:
    print("Step:",stepx,"/",steps)
    if stepx >= steps: #just in case of some numerical int/float conv
        rp = upperbound+1
        continue
    stepy = 0
    ip = lowerbound
    while ip < upperbound:
        if stepy >= steps: #just in case
            ip = upperbound +1
            continue
        initial_z = complex(rp, ip) #this is our intitial z 
        z = initial_z #assigns the complex number at initial_zpts[k] to z 
        for i in range(iters):
            z = np.multiply(z,z) + c  #get the next z from this z 
            if z.real > high_num or z.imag > high_num or z.real < neg_num or z.imag < neg_num:
                grid[stepx][stepy] = i
                #plt.scatter(initial_z.real, initial_z.imag, c = color, s = 4)
                broke = True
                break
        if broke: #if we hit infinity, just set that grid to whatever our iters are
            grid[stepx][stepy] = i
            #plt.scatter(initial_z.real, initial_z.imag, c = 'k', s = 4)
            
            
        ip += stepsize   
        stepy += 1
    rp += stepsize
    stepx += 1
    
plt.suptitle("Julia Set z=z^2+c")
plt.xlabel("real")
plt.ylabel("imaginary")
plt.title("c="+str(c))
plt.imshow(grid,cmap="terrain")
plt.show()