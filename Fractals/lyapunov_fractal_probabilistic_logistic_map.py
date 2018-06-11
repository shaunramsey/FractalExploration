import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from timeit import default_timer as timer
import random
start = timer()

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "AB"                     # sequence to alternate r values
probability = 100               # probability that a given value in the sequence will switch
a_lb = 2                       # b1 lower bound
a_ub = 4                       # b1 upper bound
b_lb = 2                       # b2 lower bound
b_ub = 4                       # b2 upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 300      # number of iterations used to compute the lyapunov exp
steps = 500                    # steps between b1 and b2 values on axes -- higher it is, the better the picture

random.seed(9001)
# CREATING RANDOM SEQUENCE WITH A LENGTH OF THE TOTAL NUMBER OF ITERATIONS
# EACH ITERATION THE PROBABILITY WILL BE JUDGED AGAINST THIS LIST
problist = list()    
for i in range(num_lyap_iterations + num_warmups):
    problist.append(random.randint(0,99))


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
def getseqval(curr_iteration, a, b, probability):
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
def getlyapexponent(time_scale, probability):
    b1, b2 = time_scale
    lyap_prob = probability
    #print("b1", b1, "b2", b2, "prob", lyap_prob)
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2, lyap_prob))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        lyapsum += np.log( np.abs(Fprime(x, getseqval(i, b1, b2, lyap_prob) ) ) )
        # get next x
        x = F(x, getseqval(i, b1, b2, lyap_prob))
    
    return (lyapsum / num_lyap_iterations)

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)
            
fractal_grid = getlyapexponent( (bb, aa), probability )

lyap_cmap = plt.get_cmap('nipy_spectral')  # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')              # any value over vmax is colored black

 # CREATING AND ADJUSTING GRAPH
plt.figure()       # creating new window for each graph that is run

plt.subplots_adjust(top = 0.825, bottom = 0.1, left = 0.11, right = 0.9, hspace = 0.2, wspace = 0.2)
plt.suptitle("Probabilistic Lyanpuov fractal for logistic map")
plt.title("Pattern: " + seq + "\n Probability that a given value\n in the pattern will switch: " + str(probability) + "%")

plt.xlabel("a")
plt.ylabel("b")

plt.imshow(fractal_grid, cmap = lyap_cmap, vmax = 0, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))

end = timer()

print("elapsed time for meshgrid: " + str(end - start))