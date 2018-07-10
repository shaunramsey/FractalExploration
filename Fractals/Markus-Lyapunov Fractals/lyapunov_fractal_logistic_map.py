import matplotlib.pyplot as plt
import numpy as np
from numba import jit
from timeit import default_timer as timer
start = timer()

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "AB"                   # sequence to alternate r values
a_lb = 2                       # b1 lower bound
a_ub = 4                       # b1 upper bound
b_lb = 2                       # b2 lower bound
b_ub = 4                       # b2 upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 10             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 100      # number of iterations used to compute the lyapunov exp
steps = 500                   # steps between b1 and b2 values on axes -- higher it is, the better the picture

# LOGISTIC MAP THAT GIVES US THE NEXT X
@jit
def F(x, curr_r):
    return (curr_r * x) * (1 - x)

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, curr_r):
    ans = curr_r * (1 - (2 * x))
    ans[ans == 0] = 0.0001
    ans[ans == -np.inf] = -1000
    ans[ans == np.inf] = 1000
    return ans
 
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
    lyap_sum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        #print("lysum", lyapsum, "i", i)
        
        lyap_sum += np.log( np.abs(Fprime(x, getseqval(i, b1, b2) ) ) )
        
        # get next x
        x = F(x, getseqval(i, b1, b2))
        
        
    
    return (lyap_sum / num_lyap_iterations)

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)
            
fractal_grid = getlyapexponent( (bb, aa) )

# CREATING AND ADJUSTING GRAPH
plt.figure()       # creating new window for each graph that is run
lyap_cmap = plt.get_cmap('nipy_spectral')   # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                 # any value over vmax is colored black
lyap_cmap.set_under('#5e1d77')              # any value under vmin is colored dark purple
plt.suptitle("Lyanpuov fractal for logistic map")
plt.title("Seq: " + seq)
plt.xlabel("a")
plt.ylabel("b")

im = plt.imshow(fractal_grid, cmap = lyap_cmap, vmin = -2, vmax = 0, origin = "lower", extent = (a_lb, a_ub, b_lb, b_ub))
plt.colorbar(im)

end = timer()
print("elapsed time: " + str(end - start))
