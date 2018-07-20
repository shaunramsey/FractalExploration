'''
Adapted from VisPy example volume rendering here: https://github.com/vispy/vispy/blob/master/examples/basics/scene/volume.py. NOTE: Normalization approach credited to Etienne Cmb on Stack Overflow: https://stackoverflow.com/questions/51306488/transparency-with-voxels-in-vispy/51309283#51309283
'''


from numba import jit
import numpy as np

from vispy import app, scene
from vispy.color import Colormap

from timeit import default_timer as timer

start = timer()


'''
Computing Fractal
'''

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
a = 0.1                     # length of continuous time intervals
n = 6                       # n value in alternating time scale
e_to_the_a = np.exp(a)      # e^a -- used for many equations

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 100             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 100     # number of iterations used to compute the lyapunov exp
steps = 100                   # steps between b1 and b2 ticks on axes -- higher it is, the better the picture


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
 
# RETURNS THE CORRECT B-VALUE BASED ON THE CURRENT ITERATION
@jit
def getbval(curr_iteration, b1, b2, b3):
    val = curr_iteration % (3 * n)
    if (val < n):
        return b1
    elif (val < (n * 2)):
        return b2
    else:
        return b3

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
@jit
def getlyapexponent(time_scale):
    b1, b2, b3 = time_scale
    
    x = .5          # initial value of x
    lyapsum = 0     # initializing lyapunov sum for use later
    
    # do warmups, to discard the early values of the iteration to allow the orbit to settle down
    for i in range(num_warmups):
        x = F(x, getbval(i, b1, b2, b3))
        
    
    for i in range(num_warmups, num_lyap_iterations + num_warmups):
        lyapsum += np.log( np.abs(Fprime(x, getbval(i, b1, b2, b3) ) ) )
        # get next x
        x = F(x, getbval(i, b1, b2, b3))
    
    return (lyapsum / num_lyap_iterations)

# RETURNS DATA NORMALIZED TO VALUES BETWEEN 0 AND 1, AS WELL AS THE NORMALIZED VALUE OF BOUNDARY_OLD
@jit
def normalize(data, boundary_old):
    orig_max = data.max()
    orig_min = data.min()
    
    # normalized boundary
    boundary_norm = boundary_old - orig_min
    boundary_norm = boundary_norm / (orig_max - orig_min)
    
    data = np.subtract(data, orig_min)
    data = np.divide(data, orig_max - orig_min)
    
    return data, boundary_norm


'''
Creating and Preparing 3D Fractal Data
'''

# DETERMING UPPER AND LOWER BOUND FOR THIS SPECIFIC A -- TO BE USED TO COMPUTE THE RANGE OF B-VALS
lowerbound = L(a)
upperbound = U(a)

# CREATING FRACTAL IMAGE 
b1 = np.linspace(lowerbound, upperbound, steps)   # range of b1 values
b2 = np.linspace(lowerbound, upperbound, steps)   # range of b2 values
b3 = np.linspace(lowerbound, upperbound, steps)   # range of b3 values

bb1, bb2, bb3 = np.meshgrid(b1, b2, b3, indexing='ij')

fractal_3D = getlyapexponent( (bb1, bb2, bb3) )

# Normalize data between 0 and 1 to be displayed and return chaotic boundary
fractal_3D, chaotic_boundary = normalize(fractal_3D, 0.0)


'''
Creating 3D projection of data
'''

# Prepare canvas
canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
canvas.measure_fps()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()
camera = scene.cameras.ArcballCamera(parent=view.scene, fov=60, scale_factor=steps*3, center = (0, 0, 0))
view.camera = camera  

# Create the volume
volume = scene.visuals.Volume(fractal_3D, clim=(0, 1), method='translucent', parent=view.scene, threshold=0.225,emulate_texture=False)

volume.transform = scene.STTransform(translate=(-steps//2, -steps//2, -steps//2))

# Creating color map to display fractal
fractal_colors = [(1, 0, 1, .5), (0, 0, 1, .5), (.1, .8, .8, .3), (.1, 1, .1, .3), (1, 1, 0, .2), (1, 0, 0, .1), (0, 1, 1, (1 - chaotic_boundary) / 7), (0, 1, .8, (1 - chaotic_boundary) / 8), (0, 0, 0, 0), (0, 0, 0, 0)]
color_control_pts = [0, (0.6 * chaotic_boundary), (0.7 * chaotic_boundary), (0.8 * chaotic_boundary), (0.9 * chaotic_boundary), (0.95 * chaotic_boundary), (0.97 * chaotic_boundary), (0.99 * chaotic_boundary), chaotic_boundary, chaotic_boundary, 1.0]

fractal_map = Colormap(fractal_colors, controls=color_control_pts, interpolation='zero')

# Assigning newly made color map to volume data
volume.cmap = fractal_map


''' 
Run program 
'''

if __name__ == '__main__':
    print(__doc__)
    app.run()
    
end = timer()
print("elapsed time: " + str(end - start))
