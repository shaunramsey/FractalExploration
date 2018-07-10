#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:07:22 2018
Finding the relative difference between Lyapunov Exponents
@author: Michelle
"""

import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import time
start = time.time()

#n = 2                      #number of gaps --the n value in alternating time scale --should match with length of iter_seq
num_warmups = 120             #our throwaway iterations to get the lyapunov exponent settled
iter = 100                    #iterations --the more iterations the more accurate
steps = 250                 #steps between b1 and b2 values -- the higher the number, the better the image resolution
iter_seq = 'AB'             #the iteration sequence of alternate r values
b1_lb = 2.0                 #b1 lowerbound
b1_ub = 4.0                 #b1 upperbound
b2_lb = 2.0                 #b2 lowerbound
b2_ub = 4.0                 #b2 upperbound
epsilon = 0.1             #the number we compare the relative differene of the lyapunov exponent to
#the higher the epsilon, the less number of changes occur
#the smaller the epsilon, more iterations occur



#F FUNCTION GIVES US THE NEXT POINT TO JUMP TO
@jit
def F(x, current_r):             #the regular F function --gives us the next point
    
    ans = (current_r * x) * ( 1 - x )
    
    return ans

#THE DERIVATIVE OF THE F FUNCTION
@jit
def Fprime(x,current_r): # the derivative of F function 
    
    ans = current_r * (1 - (2 * x) )
    
    return ans


#returns which b value we should use at that point in the time scale
@jit
def getbval(num_iterations, b1, b2):            
    #NOTE:b1 and b2 are changed over the course of our function so we gotta keep importning them
    index = np.mod(num_iterations, len(iter_seq))
    #if num_iterations % n * 2 < n:
    if  iter_seq[index] == 'A':
        return b1
    else:
        #print("b2")
        return b2

#GETTING THE RELATIVE DIFFERENCE BETWEEN TWO LYAPUNOV EXPONENTS
@jit
def relativediff(n1,n2):
    #print("wow!")
    return np.abs( np.divide( np.subtract(n1 , n2), ( np.divide( (n1 + n2), (len(iter_seq) ) ) ) ) ) 

#GETTING THE NEXT LYAPUNOV EXPONENT GIVEN THE CURRENT LYAPUNOV SUM
@jit   
def getnextexp(x,lysum, b1, b2):
    #running the lyapunov exponents in isolation: runs the length of the iteration sequence N, starting from 1
    #print("x",x,"lysum",lysum,"b",b1,"b",b2)
    for i in range(len(iter_seq)): 
       #print (i) #ideally goes 1, N
        k = iter + num_warmups + i
        lysum += np.log(np.abs( Fprime(x, getbval(k, b1, b2) ) ) )
        x = F(x, getbval(k, b1, b2) )
    lyexp2 = (lysum / (iter + len(iter_seq))) 
    newx = x
    newlysum = lysum
    return lyexp2, newx, newlysum

#FINDING THE LYAPUNOV EXPONENT
@jit
def getlyexp(b1, b2):
    x = .5                                      
                                                
    lysum = 0
 
    #print("the shape of b1 is ", b1.shape)
    #print("the shape of b2 is ", b2.shape)
    
    for i in range(num_warmups):
        x = F(x, getbval(i, b1, b2))
    
    #the REAL iterations
    for j in range(num_warmups, iter + num_warmups):
            #print ("Fprime val is " , x0)
        
        lysum += np.log(np.abs( Fprime(x, getbval(j, b1, b2) ) ) )
        #we test many values of x     
        x = F(x, getbval(j, b1, b2) )            
    
    
    #THE LYAPUNOV EXPONENT  
    lyexp = (lysum / iter) 

    newlyexp, new_x, new_lysum = getnextexp(x, lysum, b1,b2)
    print("new x's are ", new_x)
    print("new lysums are ", new_lysum)
    print("the next ly exp is ", newlyexp)
    
    #the difference between the current lyexp and the next ly exp
    relerror = relativediff(newlyexp, lyexp) #an array of arrays 
    
    ogreldiff = relerror
   
    #this relativechanges holds the number of changes occuring in the while loop at that specific element
    relativechanges = np.zeros((steps,steps))
    
    print("rel diff ", relerror)
    
    
    #this nested for loop goes through every array element of array element in the array
    #since every object is an array, we have to access specific elements to pass through ([i][j])
    for i in range(len(relerror)):
        
        for j in range(len(relerror[i])):
            #so a lot of the relerrors do need to go through this while loop. BUt how many go more than once
            #print("old relative difference", i, j, relerror[i][j]) #greater than epsilon
            #print("old exp ", newlyexp[i][j])
            ogexp = newlyexp #the very first newlyexp made outside this loop
            while (relerror[i][j] >= epsilon): #or whilearray[i][j] < 10) and whilearray[i][j] < 20: #while the relative error at ij is greater than epsilon
                #this while loop would ideally bring all relerror elements below epsilon
                relativechanges[i][j] += 1 
                
                newlyexp[i][j], new_x[i][j], new_lysum[i][j] = getnextexp( new_x[i][j], 
                        new_lysum[i][j], b1[i][j], b2[i][j] ) #run another seq of iters and get a new exponent
                    
                    #find the relative difference between the new exp and old exp
                relerror[i][j] = relativediff( newlyexp[i][j], ogexp[i][j] )
              
           
    return lyexp, relerror, relativechanges, ogreldiff


#USE RELATIVE ERROR TO GET EPSILON
#find the relative error of the lyexp2 and lyexp1 and compare to epsilon
    #for all relative errors in lyexp2 and 1
#if the relative error is greater than epsilon, keep running iterations until
#the relative error is less than epsilon



#CREATING THE FRACTAL GRID
#creating a meshgrid does the work of making b1 and b2 coordinates 
#our lists of b1's and b2's
    
a = np.linspace(b1_lb, b1_ub, steps)        
b = np.linspace(b2_lb, b2_ub, steps)            
aa, bb = np.meshgrid(a,b)  
                  
fractal_grid = []  
fractal1, error1, myrelchanges, real_diff = getlyexp( bb, aa )



#ADJUSTING GRAPH LABELS AND CREATING THE IMAGE
    
lyap_cmap = plt.get_cmap("nipy_spectral")
lyap_cmap.set_over('k') #any value over vmax is magenta
lyap_cmap.set_under('xkcd:dark blue') #any value under vmin is dark blue


plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Original Relative Difference")
plt.title("epsilon = " + str(epsilon) )   
realdiff_im = plt.imshow(real_diff, cmap= lyap_cmap, vmin = 0.0, vmax = epsilon, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(realdiff_im)

plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Lyapunov Logistic Fractal")
plt.title("num_warmups = " + str(num_warmups) + " iterations = " + str(iter) + " steps = " + str(steps))  
fractal_im = plt.imshow(fractal1,cmap= lyap_cmap, vmin = -2, vmax = 0, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(fractal_im)


#PRINTING THE DIFFERENCE BETWEEN LY1 AND LY2 

plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Relative Difference with changes where RD > epsilon")
plt.title("epsilon = " + str(epsilon) )  
error_im = plt.imshow(error1,cmap= lyap_cmap, vmin = 0.0,vmax = epsilon, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(error_im)

#plotting the number of relative changes
plt.figure()
plt.xlabel("b1")  
plt.ylabel("b2") 
plt.suptitle("Number of Changes to Relative Difference")
plt.title("epsilon = " + str(epsilon) ) 
myrelchanges_im = plt.imshow(myrelchanges, cmap= lyap_cmap, origin = 'lower', extent =[b1_lb, b1_ub, b2_lb, b2_ub]) #origin = lower sets the 0,0 point on the axis to the bottom left
plt.colorbar(myrelchanges_im)

plt.show() 

end = time.time()


print("This took", end - start, "seconds to execute")


'''
100 steps:
10 warm ups and 10 iterations = 26.269 seconds
120 WU and 120I = 7.322 seconds
10 warmups and 100 iterations = 7.74 seconds

200 steps:
10-10 = 8.723 seconds
120-120 = 7.318 seoncds

500 steps:
10-10 =
120-120 = 18.436

'''