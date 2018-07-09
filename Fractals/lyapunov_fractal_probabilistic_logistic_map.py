import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from timeit import default_timer as timer
import random
start = timer()

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "AB"                     # sequence to alternate r values
probability = 75               # probability that a given value in the sequence will switch
a_lb = 2                       # a lower bound
a_ub = 4                       # a upper bound
b_lb = 2                       # b lower bound
b_ub = 4                       # b upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 300      # number of iterations used to compute the lyapunov exp
steps = 500                    # steps between b1 and b2 values on axes -- higher it is, the better the picture

# CREATING RANDOM SEQUENCE WITH A LENGTH OF THE TOTAL NUMBER OF ITERATIONS
# EACH ITERATION THE PROBABILITY WILL BE JUDGED AGAINST THIS LIST
@jit
def getrandomseq():    
    problist = list()    
    for i in range(num_lyap_iterations + num_warmups):
        problist.append(random.randint(0,99))
    return problist

# LOGISTIC MAP THAT GIVES US THE NEXT X
@jit
def F(x, curr_r):
    return (curr_r * x) * (1 - x)

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, curr_r):
     return curr_r * (1 - (2 *x))
 
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getseqval(curr_iteration, a, b, probability, problist):
    randnum = problist[curr_iteration]
    index = np.mod(curr_iteration, len(seq))
    if (seq[index] == 'A'):
        if (probability <= randnum):
            return a
        else:
            return b
    else:
        if (probability <= randnum):
            return b
        else:
            return a

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(time_scale, probability, problist):
    b1, b2 = time_scale
    lyap_prob = probability
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2, lyap_prob, problist))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        lyapsum += np.log( np.abs(Fprime(x, getseqval(i, b1, b2, lyap_prob, problist) ) ) )
        # get next x
        x = F(x, getseqval(i, b1, b2, lyap_prob, problist))
    
    return (lyapsum / num_lyap_iterations)

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)
            
# COMPUTING AVERAGE IMAGE FROM MULTIPLE RANDOM SEQUENCES        
lyap_exponents = []
for i in range(10):
    problist = getrandomseq()
    lyap_exponents.append(getlyapexponent( (bb, aa), probability, problist ))

fractal_grid = np.average(lyap_exponents, axis = 0)


 # CREATING AND ADJUSTING GRAPH
plt.figure()       # creating new window for each graph that is run

plt.subplots_adjust(top = 0.825, bottom = 0.1, left = 0.11, right = 0.9, hspace = 0.2, wspace = 0.2)
plt.suptitle("Probabilistic Lyanpuov fractal for logistic map")
plt.title("Pattern: " + seq + "\n Probability that a given value\n in the pattern will switch: " + str(probability) + "%")

plt.xlabel("a")
plt.ylabel("b")

im = plt.imshow(fractal_grid, cmap = lyap_cmap, vmin = -2, vmax = 0, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))
plt.colorbar(im)

end = timer()

print("elapsed time: " + str(end - start))
