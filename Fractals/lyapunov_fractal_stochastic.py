# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 14:44:20 2018

@author: Rachel
"""
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from timeit import default_timer as timer
import random
start = timer()

# PARAMETERS TO CHANGE THE FRACTAL PICTURE GENERATED
a_lb = 2                       # a lower bound
a_ub = 4                       # a upper bound
b_lb = 2                       # b lower bound
b_ub = 4                       # b upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 200      # number of iterations used to compute the lyapunov exp
steps = 1000                   # steps between b1 and b2 values on axes -- higher it is, the better the picture

random.seed(9001)
# CREATING RANDOM "AB" SEQUENCE WITH A LENGTH OF THE TOTAL NUMBER OF ITERATIONS THAT WILL USE THE SEQUENCE
# 0 IS A, 1 IS B
seqlist = list()    
for i in range(num_lyap_iterations + num_warmups):
    seqlist.append(random.randint(0,1))

# LOGISTIC MAP THAT GIVES US THE NEXT X
@jit
def F(x, b):
    return (b * x) * (1 - x)

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, b):
    return b * (1 - (2 *x))

         
        
 
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getseqval(curr_iteration, b1, b2):
    if (seqlist[curr_iteration] == 0):
        return b1
    else:
        return b2

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(time_scale):
    b1, b2 = time_scale
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        #print("i", i)
        lyapsum += np.log( np.abs(Fprime(x, getseqval(i, b1, b2) ) ) )
        # get next x
        x = F(x, getseqval(i, b1, b2))
    
    return (lyapsum / num_lyap_iterations)

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)
            
fractal_grid = []                                # "grid" containing lyapunov exponents for each point in points
fractal_grid.append(getlyapexponent( (bb, aa) )) 
fractal_grid = np.reshape(fractal_grid, (steps, steps)) # fractal_grid is then reshaped into a grid

lyap_cmap = plt.get_cmap('nipy_spectral')         # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')              # any value over vmax is colored black

plt.figure()
plt.title("Stochastic Lyanpuov fractal for logistic map")
plt.xlabel("a")
plt.ylabel("b")
plt.imshow(fractal_grid, cmap = lyap_cmap, vmax = 0, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))

end = timer()

print("elapsed time for meshgrid: " + str(end - start))