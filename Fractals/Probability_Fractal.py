#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 08:38:09 2018
Probability Logistic Fractal
@author: Michelle
"""
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import time
import random
start = time.time()

#n = 6                   #number of gaps --the n value in alternating time scale
num_warmups = 1120        #our iterations for getting the system to a steady state
iter = 1200              #iterations --the more iters the more accurate
steps = 1000             #steps between b1 and b2 values -- the higher the number, the better hte res
iter_seq = 'AB'
probability = 75 #75% percent of the time
b1_lb = 2.0                
b1_ub = 4.0
b2_lb = 2.0
b2_ub = 4.0

#random.seed(20)

@jit
def getbval(curr_iter, A, B):                    #the probability function
   
    percent = random.randint(0, 100)           #choose a random number from 0-3
    index = np.mod(curr_iter, len(iter_seq))    #determines where you are in the sequence
    if iter_seq[index] == 'A':                  # if we are in the A part of the sequence
       if percent < probability:                #if the random number is less than the probability 
           return A                             #return A -- A is unchanged
       else:
           return B #the 25% of the other time
    else: # if we are in Bd lands
        if percent < probability:               #if the random number is less than the probability
            return B                            #A is changed to B
        else:
            return A
    
@jit
def F(x,b):             #the regular F function --gives us the next point
    
    ans = (b * x) * (1-x)
    
    return ans

@jit
def Fprime(x,b): # the derivative of F function 
    
    ans = b * (1 - (2 * x))
    
    return ans


        
#our warm up iterations -- allows the system to reach a steady state

a = np.linspace(b1_lb, b1_ub, steps)        #our lists of b1's and b2's
b = np.linspace(b2_lb, b2_ub, steps)
aa,bb = np.meshgrid(a,b)   
        #creating a meshgrid does the work of making b1 and b2 coordinates 
fractal_grid = []   

@jit
def getlyexp(b1, b2):
    
    x = .5                                      #the x value we start with -- ASK FOR CLARIFICATION
                                                #note: the initial value shouldnt really matter 
    #b1, b2 = time_scale                         #unpack the b1 and b2 from time_scale
    for i in range(num_warmups): #our throwaways iterations
        x = F(x, getbval(i, b1, b2))
    #print ("warm ups work")
    lysum = 0
    
    for j in range(num_warmups, iter + num_warmups): #from start to stop
            #print ("Fprime val is " , x0)
        b_val = getbval(j, b1, b2)
        lysum += np.log(np.abs(Fprime(x, b_val)  ) )#the lyapunov equation!
        
        x = F(x, b_val )                    #we test many values of x     
        
    lyexp = (float)(1 / iter) * lysum
    #print ("lyworks")
    return lyexp

#CREATING THE FRACTAL GRID

                                  #our array for the image
fractal_grid.append(getlyexp(bb, aa))                   #get all the lyexps and add them to our array
    
fractal_grid = np.reshape(fractal_grid, (steps, steps)) #reshape fractal_grid for size steps, steps
    

lyap_cmap = plt.get_cmap("nipy_spectral")
lyap_cmap.set_over('black')

plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Logistic Fractal with probability determining Sequence Changes")
plt.title("Sequence = " + iter_seq +  " Probability of Change = " + str(probability) + "%")
plt.imshow(fractal_grid,cmap= lyap_cmap, vmax = 0, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.show() 
end = time.time()

print("This took", end - start, "seconds to execute")