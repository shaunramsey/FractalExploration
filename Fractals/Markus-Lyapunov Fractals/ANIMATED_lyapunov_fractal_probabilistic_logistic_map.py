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
seq = "AB"                     # sequence to alternate r values
a_lb = 2                       # b1 lower bound
a_ub = 4                       # b1 upper bound
b_lb = 2                       # b2 lower bound
b_ub = 4                       # b2 upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 120      # number of iterations used to compute the lyapunov exp
steps = 300                    # steps between b1 and b2 values on axes -- higher it is, the better the picture
 
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


'''
ANIMATING FRACTAL

Making each frame and creating animation to then save with ImageMagick
'''
plt.rcParams["animation.convert_path"] = r"C:\Program Files\ImageMagick-7.0.7-Q16\magick.exe" 
plt.rcParams['animation.html'] = 'html5'


# INITIALIZING LIN-SPACE FOR FRACTAL GRID
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
aa, bb = np.meshgrid(a, b)

# INITIALIZING GRAPHING ELEMENTS FOR ANIMATION
fig, ax = plt.subplots()
    
# CREATING AND ADJUSTING GRAPH
lyap_cmap = plt.get_cmap('nipy_spectral')   # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                 # any value over vmax is colored black
lyap_cmap.set_under('#5e1d77')              # any value under vmin is colored dark purple
plt.title("Probabilistic Lyapunov fractal / SEQ: " + seq)
plt.xlabel("a")
plt.ylabel("b")

# HOW TO DRAW FRAME NUMBER i
def animate(i):
    print("frame #:", i)       
    probability = i
    
    lyap_exponents = []
    for i in range(10):
        problist = getrandomseq()
        lyap_exponents.append(getlyapexponent( (bb, aa), probability, problist ))

    grid = np.average(lyap_exponents, axis = 0)
    
    return grid

# CREATING FRACTAL IMAGES 
ims = []
for i in range(101):
    grid = animate(i)
    subtitle = ax.text(0.5, 0.95, "Probability values will switch: {}%".format(i), bbox={'facecolor':'w', 'alpha':0.8, 'pad':5}, ha="center", transform=ax.transAxes, )
    im = ax.imshow(grid, cmap = lyap_cmap, vmin = -2, vmax = 0, origin = 'lower', extent = [a_lb, a_ub, b_lb, b_ub]) 
    ims.append([im, subtitle])

anim = animation.ArtistAnimation(fig, ims, interval = 200, blit = True)
anim.save(r"Prob_Lyap_Fractal.gif", writer="imagemagick")

plt.show()

end = timer()
print("elapsed time: " + str(end - start))
