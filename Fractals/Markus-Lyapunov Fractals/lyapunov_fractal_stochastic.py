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
steps = 500                   # steps between b1 and b2 values on axes -- higher it is, the better the picture

# CREATING RANDOM SEQUENCE WITH A LENGTH OF THE TOTAL NUMBER OF ITERATIONS
# EACH ITERATION THE PROBABILITY WILL BE JUDGED AGAINST THIS LIST
@jit
def getrandomseq():    
    problist = list()    
    for i in range(num_lyap_iterations + num_warmups):
        problist.append(random.randint(0,1))
    return problist

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
def getseqval(curr_iteration, b1, b2, seqlist):
    if (seqlist[curr_iteration] == 0):
        return b1
    else:
        return b2

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(time_scale, seqlist):
    b1, b2 = time_scale
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2, seqlist))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        #print("i", i)
        lyapsum += np.log( np.abs(Fprime(x, getseqval(i, b1, b2, seqlist) ) ) )
        # get next x
        x = F(x, getseqval(i, b1, b2, seqlist))
    
    return (lyapsum / num_lyap_iterations)

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)
            
# COMPUTING AVERAGE IMAGE FROM MULTIPLE RANDOM SEQUENCES        
lyap_exponents = []
for i in range(10):
    problist = getrandomseq()
    lyap_exponents.append(getlyapexponent( (bb, aa), problist ))

fractal_grid = np.average(lyap_exponents, axis = 0)

# CREATING GRAPH
lyap_cmap = plt.get_cmap('nipy_spectral')       # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                     # any value over vmax is colored black
lyap_cmap.set_under('#5e1d77')                  # any value under vmin is colored dark purple
                    
plt.figure()
plt.suptitle("Stochastic Lyanpuov fractal for logistic map")
plt.title("black = chaotic / dark purple = superstable")
plt.xlabel("a")
plt.ylabel("b")
image = plt.imshow(fractal_grid, cmap = lyap_cmap, vmax = 0, vmin = -2, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))
plt.colorbar(image)

end = timer()

print("elapsed time: " + str(end - start))
