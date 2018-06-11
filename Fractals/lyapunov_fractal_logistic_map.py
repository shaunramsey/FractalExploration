import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from timeit import default_timer as timer
start = timer()

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "BA"                     # sequence to alternate r values
a_lb = 2                       # b1 lower bound
a_ub = 4                       # b1 upper bound
b_lb = 2                       # b2 lower bound
b_ub = 4                       # b2 upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 120      # number of iterations used to compute the lyapunov exp
steps = 500                    # steps between b1 and b2 values on axes -- higher it is, the better the picture

# LOGISTIC MAP THAT GIVES US THE NEXT X
@jit
def F(x, curr_r):
    return (curr_r * x) * (1 - x)

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, curr_r):
     return curr_r * (1 - (2 * x))
 
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getseqval(curr_iteration, a, b):
    index = np.mod(curr_iteration, len(seq))
    if (seq[index] == 'A'):
        return a
    else:
        return b

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
plt.suptitle("Lyanpuov fractal for logistic map")
plt.title("string = " + seq)
plt.xlabel("a")
plt.ylabel("b")
plt.imshow(fractal_grid, cmap = lyap_cmap, vmax = 0, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))

end = timer()

print("elapsed time for meshgrid: " + str(end - start))