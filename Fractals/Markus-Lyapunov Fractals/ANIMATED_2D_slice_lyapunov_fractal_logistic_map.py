import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from numba import jit
from timeit import default_timer as timer
import random

start = timer()

'''
FRACTAL

Functions and parameters to change the appearance and behavior of the fractals generated
'''

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "ABC"                     # sequence to alternate r values
a_lb = 2                        # a lower bound
a_ub = 4                        # a upper bound
b_lb = 2                        # b lower bound
b_ub = 4                        # b upper bound
c_lb = 2                        # c lower bound
c_ub = 4                        # c upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 120      # number of iterations used to compute the lyapunov exp
steps = 300                    # steps between b1 and b2 values on axes -- higher it is, the better the picture

# LOGISTIC MAP THAT GIVES US THE NEXT X
@jit
def F(x, curr_r):
    return (curr_r * x) * (1 - x)

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, curr_r):
    ans = curr_r * (1 - (2 * x))
    ans[ans == 0] = 0.00001
    ans[ans == -np.inf] = -1000
    ans[ans == np.inf] = 1000
    return ans
 
# CREATING RANDOM SEQUENCE WITH A LENGTH OF THE TOTAL NUMBER OF ITERATIONS
# EACH ITERATION THE PROBABILITY WILL BE JUDGED AGAINST THIS LIST
@jit
def getrandomseq():    
    problist = list()    
    for i in range(num_lyap_iterations + num_warmups):
        problist.append(random.randint(0,99))
    return problist
    

# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getseqval(curr_iteration, a, b, c):
    index = np.mod(curr_iteration, len(seq))
    if (seq[index] == 'A'):
        return a
    elif (seq[index] == 'B'):
        return b
    else:
        return c

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(a, b, c):
    x = .5          # initial value of x
    lyap_sum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, a, b, c))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):        
        lyap_sum += np.log( np.abs(Fprime(x, getseqval(i, a, b, c) ) ) )
        
        # get next x
        x = F(x, getseqval(i, a, b, c))
    
    return (lyap_sum / num_lyap_iterations)

'''
ANIMATING FRACTAL

Making each frame and creating animation to then save with ImageMagick
'''
plt.rcParams["animation.convert_path"] = r"C:\Program Files\ImageMagick-7.0.7-Q16\magick.exe" 
plt.rcParams['animation.html'] = 'html5'


# INITIALIZING LIN-SPACE FOR FRACTAL GRID
a = np.linspace(a_lb, a_ub, steps)   #range of a values
b = np.linspace(b_lb, b_ub, steps)   #range of b values
c = np.linspace(c_lb, c_ub, steps)   #range of c values
aa, bb = np.meshgrid(a, b)

# INITIALIZING GRAPHING ELEMENTS FOR ANIMATION
fig, ax = plt.subplots()
    
# CREATING AND ADJUSTING GRAPH
lyap_cmap = plt.get_cmap('nipy_spectral')   # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                 # any value over vmax is colored black
lyap_cmap.set_under('#5e1d77')              # any value under vmin is colored dark purple
plt.title("2D slice of 3D Lyapunov fractal / SEQ: " + seq)
plt.xlabel("A value")
plt.ylabel("B value")

# HOW TO DRAW FRAME NUMBER i
def animate(i):
    print("frame #:", i)

    grid = getlyapexponent( bb, aa, c[i] ) 
    
    return grid

# CREATING FRACTAL IMAGES 
ims = []
for i in range(steps):
    grid = animate(i)
    subtitle = ax.text(0.5, 0.95, "C value: {}".format(c[i]), bbox={'facecolor':'w', 'alpha':0.8, 'pad':5}, ha="center", transform=ax.transAxes,)
    im = ax.imshow(grid, cmap = lyap_cmap, vmin = -2, vmax = 0, origin = 'lower', extent = [a_lb, a_ub, b_lb, b_ub]) 
    ims.append([im, subtitle])

anim = animation.ArtistAnimation(fig, ims, interval = 200, blit = True)
anim.save(r"Lyap_3D_slice.gif", writer="imagemagick")

plt.show()

end = timer()
print("elapsed time: " + str(end - start))