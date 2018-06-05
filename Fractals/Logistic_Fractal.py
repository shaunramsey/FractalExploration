#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:07:22 2018
The Lyapunov logistic fractal
@author: Michelle
"""

import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import time
start = time.time()

#n = 6                   #number of gaps --the n value in alternating time scale
num_warmups = 1200        #our iterations for getting the system to a steady state
iter = 120              #iterations --the more iters the more accurate
steps = 500             #steps between b1 and b2 values -- the higher the number, the better hte res
iter_seq = 'AB'
b1_lb = 2.0                
b1_ub = 4.0
b2_lb = 2.0
b2_ub = 4.0


@jit
def F(x,b):             #the regular F function --gives us the next point
    
    ans = (b * x) * (1-x)
    
    return ans

@jit
def Fprime(x,b): # the derivative of F function 
    
    ans = b * (1 - (2 * x))
    
    return ans


#returns which b value we should use at that point in the time scale
@jit
def getbval(num_iterations, b1, b2):            #NOTE:b1 and b2 are chagned over the course of our function so we gotta keep importning them
    index = np.mod(num_iterations, len(iter_seq))
    #if num_iterations % n * 2 < n:
    if  iter_seq[index] == 'A':
        #print("b1")
        return b1
    else:
        #print("b2")
        return b2

#our warm up iterations -- allows the system to reach a steady state
@jit
def getlyexp(b1, b2):
    x = .5                                      #the x value we start with -- ASK FOR CLARIFICATION
                                                #note: the initial value shouldnt really matter 
    #b1, b2 = time_scale                         #unpack the b1 and b2 from time_scale
    for i in range(num_warmups): #our throwaways iterations
        x = F(x, getbval(i, b1, b2))
    lysum = 0
    
    for j in range(num_warmups, iter + num_warmups):
            #print ("Fprime val is " , x0)
        lysum += np.log(np.abs( Fprime(x, getbval(j, b1, b2) ) ) )#the lyapunov equation!
        x = F(x, getbval(j, b1, b2) )                    #we test many values of x     
        
    lyexp = (float)(1 / iter) * lysum
    return lyexp

#CREATING THE FRACTAL GRID

a = np.linspace(b1_lb, b1_ub, steps)        #our lists of b1's and b2's
b = np.linspace(b2_lb, b2_ub, steps)
aa,bb = np.meshgrid(a,b)   
        #creating a meshgrid does the work of making b1 and b2 coordinates 
fractal_grid = []                                       #our array for the image
fractal_grid.append(getlyexp( bb, aa ) )                         #add it to our array
    
fractal_grid = np.reshape(fractal_grid, (steps, steps)) #reshape fractal_grid for size steps, steps
    

lyap_cmap = plt.get_cmap("nipy_spectral")
lyap_cmap.set_over('black')

plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Lyapunov Logistic Fractal")
plt.title("string = " + iter_seq)  
plt.imshow(fractal_grid,cmap= lyap_cmap, vmax = 0, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.show() 

end = time.time()



print("This took", end - start, "seconds to execute")