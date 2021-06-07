import matplotlib.pyplot as plt
import numpy as np
from numba import jit

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
a = 0.1                        # length of continuous time intervals
n = 6                           # n value in alternating time scale
e_to_the_a = np.exp(a)          # e^a -- used for many equations

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200               # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 100      # number of iterations used to compute the lyapunov exp
steps = 500                     # steps between b1 and b2 values on axes -- higher it is, the better the picture

# LOWER BOUND OF AREA OF INTEREST IN A TIME SCALE WITH THE SPECIFIED A VALUE
#@jit
def L(a):
    return e_to_the_a + 1

# UPPER BOUND OF AREA OF INTEREST IN A TIME SCALE WITH THE SPECIFIED A VALUE
#@jit
def U(a):
    return ( np.sqrt(np.exp(2 * a) + (8 * e_to_the_a) ) + e_to_the_a + 2) / 2

# DIFFERENCE OPERATOR -- MAP THAT GIVES US THE LEFT ENDPOINT OF THE NEXT CONTINUS TIME INTERVAL
#@jit
def F(x, b):
    top = ( e_to_the_a * x ) * ( ( (e_to_the_a - 1) * x ) - (b * x) + b + 1 )
    bottom = ( ( e_to_the_a - 1 ) * x + 1 )**2
    return top/bottom

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
#@jit
def Fprime(x, b):
     
     top = -1 * e_to_the_a * ( ( x * e_to_the_a + x - 1 ) * b - (x * e_to_the_a) + x - 1 )
     bottom =  ( ( e_to_the_a - 1 ) * x + 1 )**3
     return top/bottom
 
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
#@jit
def getbval(curr_iteration, b1, b2):
    if (curr_iteration % (2 * n) < n):
        return b1
    else:
        return b2

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
#@jit
def getlyapexponent(time_scale):
    b1, b2 = time_scale
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getbval(i, b1, b2))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        lyapsum += np.log( np.abs(Fprime(x, getbval(i, b1, b2) ) ) )
        # get next x
        x = F(x, getbval(i, b1, b2))
    
    lyapexponent = (lyapsum / num_lyap_iterations)
    
    return lyapexponent

# DETERMING UPPER AND LOWER BOUND FOR THIS SPECIFIC A -- TO BE USED TO COMPUTE THE RANGE OF B-VALS
lowerbound = L(a)
upperbound = U(a)

# CREATING FRACTAL IMAGE
b1 = np.linspace(lowerbound, upperbound, steps)   #range of b1 values
b2 = np.linspace(lowerbound, upperbound, steps)   #range of b2 values

points = list()                         # points is a list of points in the b1-b2 plane 
for i in b1:                            # it has all possible points of the ranges of b1 and b2
    for j in b2: 
        points.append( (i, j) )         # each element is a tuple coordinate pair
               
fractal_grid = []                               # "grid" containing lyapunov exponents for each point in points
for time_scale in points:
    exp = getlyapexponent(time_scale)
    fractal_grid.append(exp)                    # fractal_grid is initialized as a list so we can append to it
    
fractal_grid = np.reshape(fractal_grid, (steps, steps)) # fractal_grid is then reshaped into a grid

lyap_cmap = plt.get_cmap('nipy_spectral')         # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                 # any value over vmax is colored black

plt.suptitle("Lyanpuov fractal for Alternating Pulse Time Scale")
plt.title("a = " + str(a) + ", n = " + str(n))
plt.xlabel("b1")
plt.ylabel("b2")
plt.imshow(fractal_grid, cmap = lyap_cmap, origin = "lower", vmax=0, extent = (lowerbound, upperbound, lowerbound, upperbound))
plt.show()