#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:07:22 2018
The Lyapunov logistic fractal using Fprime to determine when a pattern is found when calculating the Lyapunov 
Exponent. We use the number of times to show the bifurcation of the fractal
@author: Michelle
"""

import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import time
start = time.time()

n = 2                      #number of gaps --the n value in alternating time scale --should match with length of iter_seq
num_warmups = 1000           #our throwaway iterations to get the lyapunov exponent settled
iter = 100                   #iterations --the more iterations the more accurate
steps = 100                 #steps between b1 and b2 values -- the higher the number, the better the image resolution
iter_seq = 'AB'             #the iteration sequence of alternate r values
b1_lb = 2.0                 #b1 lowerbound
b1_ub = 4.0                 #b1 upperbound
b2_lb = 2.0                 #b2 lowerbound
b2_ub = 4.0                 #b2 upperbound
epsilon = 0.1             #the number we compare the relative differene of the lyapunov exponent to
#the higher the epsilon, the less number of changes occur
#the smaller the epsilon, more iterations occur

'''
F FUNCTION GIVES US THE NEXT POINT TO JUMP TO
'''
@jit
def F(x,b):
    
    ans = (b * x) * ( 1 - x )
    
    return ans

'''
THE DERIVATIVE OF THE F FUNCTION
'''

@jit
def Fprime(x,b): # the derivative of F function 
    
    ans = b * (1 - (2 * x) )
    
    return ans

'''
returns which b value we should use at the current point in the time scale
'''

@jit
def getbval(num_iterations, b1, b2):            #NOTE:b1 and b2 are changed over the course of our function so we gotta keep importning them
    index = np.mod(num_iterations, len(iter_seq))
    #if num_iterations % n * 2 < n:
    if  iter_seq[index] == 'A':
        #print("b1")
        return b1
    else:
        #print("b2")
        return b2
'''   
GETTING THE RELATIVE DIFFERENCE BETWEEN TWO LYAPUNOV EXPONENTS
'''
@jit
def relativediff(n1,n2):
  
    return np.abs( np.divide( np.subtract(n1 , n2), ( np.divide((n1 + n2), (n)) ) ) )

'''
GETTING THE NEXT LYAPUNOV EXPONENT GIVEN THE CURRENT LYAPUNOV SUM
running the lyapunov exponents in isolation: 
runs the length of the iteration sequence N, starting from 1

'''
@jit   
def getnextexp(x,lysum, b1, b2):

    for i in range(len(iter_seq)): 
       #print (i) #ideally goes 1, N
        k = iter + num_warmups + i
        lysum += np.log(np.abs( Fprime(x, getbval(k, b1, b2) ) ) )
        x = F(x, getbval(k, b1, b2) )
    lyexp2 = (lysum / (iter + len(iter_seq))) 
    newx = x
    newlysum = lysum
    return lyexp2, newx, newlysum

'''
FINDING THE LYAPUNOV EXPONENT
-since b1 and b2 are single values passed in, getlyexp is called SO MANY TIMES and its so slow
@jit is not used because it iterferes with the pattern statements and any

-IF the difference between any value in pattern and current Fprime is less than a really small number
(in other words they are the same number), it breaks out of the loop because a pattern is found
breaking out of the loop means to do NO MORE iterations
'''


def getlyexp(b1, b2):
    x = 0.3                                     
    
    lysum = 0
    num_iterations = 0
    FPrime_break = iter
    #this warmup for loop brings the x value up to a number hopefully close to the number we need 
    #to get the Lyapunov Exponent
    for i in range(num_warmups):
        x = F(x, getbval(i, b1, b2))
        num_iterations += 1
   
    #we get the first f prime outside of the next for loop so our pattern list has an item to hold
    first_f_prime = np.log(np.abs( Fprime(x, getbval(num_iterations, b1, b2) ) ) )
    pattern = [first_f_prime]   
    
    #these next iterations will actually help in calculating the Lya Exp
    for j in range(num_warmups, iter + num_warmups): 
        #get the next new value of x
        x = F(x, getbval(j, b1, b2) ) 
        
        #find the current F_prime
        F_prime = Fprime(x, getbval(j, b1, b2) ) 
        
        #get the lysum
        lysum += np.log(np.abs( F_prime ) ) 
        
        #get the current log(F_prime), which is equivalent to lysum
        current_Fprime = np.log(np.abs( F_prime ) ) 
        
        
        if any(np.abs((t - current_Fprime)) <= 0.00001 for t in pattern):
        
            FPrime_break = j - num_warmups
            
            break
        
        #otherwise, add current_Fprime to the pattern list
        pattern.append(current_Fprime)
     
    #take the average of Fprime, which is equal to lyapunov exponent
    average_Fprime = np.average(pattern)
    #we return average Fprime because The LyExponent = lysum/iter which is the AVERAGE of all the lysums
    #which is equal to the average of the log(Fprimes) since Fprime and lysum are the same
    if average_Fprime == (np.inf * -1):
        average_Fprime = -3
    
    
    return average_Fprime, FPrime_break
     
    
#CREATING THE FRACTAL GRID
#our lists of b1's and b2's
    
a = np.linspace(b1_lb, b1_ub, steps)        
b = np.linspace(b2_lb, b2_ub, steps)   
       
fractal_grid = []           
fractal1 = [] 
jvalues = []
for d in range(len(a)): #for all in b1
    for c in range(len(b)): #for all in b2
        fractal, jvalue = getlyexp( a[d], b[c] ) #passes in a single set of coordinates from a and b to the function
        fractal1.append(fractal)
        jvalues.append(jvalue)


#reshape fractal_grid for size steps, steps

fractal_grid = np.reshape(fractal1, (steps, steps))
print(fractal_grid.shape)
jgrid = np.reshape(jvalues,(steps,steps))

#ADJUSTING GRAPH LABELS AND CREATING THE IMAGE
#print(change_grid)

lyap_cmap = plt.get_cmap("nipy_spectral")
lyap_cmap.set_over('black')
lyap_cmap.set_under('xkcd:dark blue')


#PLOTTING THE FRACTAL
plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Lyapunov Logistic Fractal")
plt.title("num_warmups = " + str(num_warmups) + " iterations = " + str(iter) + " pixels = " + str(steps) )  
fractal_im = plt.imshow(fractal_grid,cmap= lyap_cmap, vmin = -2, vmax = 0, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(fractal_im)

#PLOT THE NUMBER OF BIFURCATIONS
plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Number of Bifurcations")
plt.title("num_warmups = " + str(num_warmups) + " iterations = " + str(iter) + " pixels = " + str(steps) )  
jgrid_im = plt.imshow(jgrid,cmap= lyap_cmap, vmin = -2, vmax = 128, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(jgrid_im)

plt.show() 

end = time.time()


print("This took", end - start, "seconds to execute")

'''
100 steps:
10 warmups and 10 iterations = 5 seconds
120 warmups and 120 iterations = 62.36 seconds
10 warmups and 100 iterations = 98.95 seconds
1000 warmups and 100 iterations = 166.28 seconds

200 steps:
10-10 = 20.448 seconds
120-120 = 192.946 seconds

500 steps:
10-10 = 96.364 seconds
120-120 = 1186.0747 seconds

'''