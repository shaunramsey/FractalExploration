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
a = 0.1                        # length of continuous time intervals
n = 6                          # n value in alternating time scale
e_to_the_a = np.exp(a)          # e^a -- used for many equations

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 1200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 120      # number of iterations used to compute the lyapunov exp
steps = 300                   # steps between b1 and b2 ticks on axes -- higher it is, the better the picture

# LOWER BOUND OF AREA OF INTEREST IN A TIME SCALE WITH THE SPECIFIED A VALUE
@jit
def L(a):
    return e_to_the_a + 1

# UPPER BOUND OF AREA OF INTEREST IN A TIME SCALE WITH THE SPECIFIED A VALUE
@jit
def U(a):
    return ( np.sqrt(np.exp(2 * a) + (8 * e_to_the_a) ) + e_to_the_a + 2) / 2

# DIFFERENCE OPERATOR -- MAP THAT GIVES US THE LEFT ENDPOINT OF THE NEXT CONTINUS TIME INTERVAL
@jit
def F(x, b):
    top = ( e_to_the_a * x ) * ( ( (e_to_the_a - 1) * x ) - (b * x) + b + 1 )
    bottom = ( ( e_to_the_a - 1 ) * x + 1 )**2
    return top/bottom

# DERIVATIVE OF F -- USED TO COMPUTE THE LYAPUNOV EXPONENT
@jit
def Fprime(x, b):
     top = -1 * e_to_the_a * ( ( x * e_to_the_a + x - 1 ) * b - (x * e_to_the_a) + x - 1 )
     bottom =  ( ( e_to_the_a - 1 ) * x + 1 )**3
     return top/bottom
 
@jit
def getrandomseq():    
    problist = list()    
    for i in range(num_lyap_iterations + num_warmups):
        problist.append(random.randint(0,99))
    return problist    
    
    
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getseqval(curr_iteration, b1, b2, probability, problist):
    randnum = problist[curr_iteration]
    if (curr_iteration % (2 * n) < n):
        if (probability <= randnum):
            return b1
        else:
            return b2
    else:
        if (probability <= randnum):
            return b2
        else:
            return b1

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(time_scale, probability, problist):
    b1, b2 = time_scale
    lyap_prob = probability
    #print("b1", b1, "b2", b2, "prob", lyap_prob)
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getseqval(i, b1, b2, lyap_prob, problist))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        lyapsum += np.log( np.abs(Fprime( x, getseqval(i, b1, b2, lyap_prob, problist) ) ) )
        # get next x
        x = F( x, getseqval(i, b1, b2, lyap_prob, problist) )
    
    return (lyapsum / num_lyap_iterations)

'''
ANIMATING FRACTAL

Making each frame and creating animation to then save with ImageMagick
'''
plt.rcParams["animation.convert_path"] = r"C:\Program Files\ImageMagick-7.0.7-Q16\magick.exe" 
plt.rcParams['animation.html'] = 'html5'


# DETERMING UPPER AND LOWER BOUND FOR THIS SPECIFIC A -- TO BE USED TO COMPUTE THE RANGE OF B-VALS
lowerbound = L(a)
upperbound = U(a)

# CREATING FRACTAL IMAGE
b1 = np.linspace(lowerbound, upperbound, steps)   # range of b1 values
b2 = np.linspace(lowerbound, upperbound, steps)   # range of b2 values
bb1, bb2 = np.meshgrid(b1, b2)

# INITIALIZING GRAPHING ELEMENTS FOR ANIMATION
fig, ax = plt.subplots()
    
# CREATING AND ADJUSTING GRAPH
lyap_cmap = plt.get_cmap('nipy_spectral')   # creating our own colormap to use "set_over" with    
lyap_cmap.set_over('black')                 # any value over vmax is colored black
lyap_cmap.set_under('#5e1d77')              # any value under vmin is colored dark purple
plt.suptitle("Probabilistic Alternating Pulse TS")
plt.title("a =" + str(a) + ", n =" + str(n))
plt.xlabel("B1 value")
plt.ylabel("B2 value")

# HOW TO DRAW FRAME NUMBER i
def animate(i):
    print("frame #:", i)       
    probability = i
    
    '''
    #Create average of all exponents - VERY slow but a less shaky picture
    lyap_exponents = []
    for i in range(10):
        problist = getrandomseq()
        lyap_exponents.append(getlyapexponent( (bb2, bb1), probability, problist ))

    grid = np.average(lyap_exponents, axis = 0)
    '''
    problist = getrandomseq()
    grid = getlyapexponent( (bb2, bb1), probability, problist )
    
    return grid

# CREATING FRACTAL IMAGES 
ims = []
for i in range(101):
    grid = animate(i)
    subtitle = ax.text(0.5, 0.95, "Probability values will switch: {}%".format(i), bbox={'facecolor':'w', 'alpha':0.8, 'pad':5}, ha="center", transform=ax.transAxes,)
    im = ax.imshow(grid, cmap = lyap_cmap, vmin = -2, vmax = 0, origin = 'lower', extent = [lowerbound, upperbound, lowerbound, upperbound]) 
    ims.append([im, subtitle])

anim = animation.ArtistAnimation(fig, ims, interval = 500, blit = True)
anim.save(r"Avg_Probabilistic_Pulse_TS.gif", writer="imagemagick")

plt.show()

end = timer()
print("elapsed time: " + str(end - start))