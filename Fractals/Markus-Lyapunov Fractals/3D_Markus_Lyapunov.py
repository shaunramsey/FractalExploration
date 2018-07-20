'''
Adapted from VisPy example volume rendering here: https://github.com/vispy/vispy/blob/master/examples/basics/scene/volume.py

NOTE: Normalization approach credited to Etienne Cmb on Stack Overflow: https://stackoverflow.com/questions/51306488/transparency-with-voxels-in-vispy/51309283#51309283
'''


from numba import jit
import numpy as np

import imageio
from vispy import app, scene
from vispy.color import Colormap

from timeit import default_timer as timer

start = timer()

'''
Computing Fractal
'''

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
anim = True     # change whether to produce a .gif animation of fractal rotating
seq = "ABC"     # sequence to alternate r values
a_lb = 2        # a lower bound
a_ub = 4        # a upper bound
b_lb = 2        # b lower bound
b_ub = 4        # b upper bound
c_lb = 2        # c lower bound
c_ub = 4        # c upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 100             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 100      # number of iterations used to compute the lyapunov exp
steps = 100                   # steps between b1 and b2 values on axes -- higher it is, the better the picture

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

# CREATING FRACTAL IMAGE 
a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
c = np.linspace(c_lb, c_ub, steps)

aa, bb, cc = np.meshgrid(a, b, c, indexing='ij')

fractal_3D = getlyapexponent(aa, bb, cc)

# normalize data between 0 and 1 to be displayed and return chaotic boundary
fractal_3D, chaotic_boundary = normalize(fractal_3D, 0.0)
print("chaotic boundary:", chaotic_boundary)

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


''' Creating animation of rotating fractal '''
if anim:
    file_name = "Anim_3D_Fractal_" + seq + ".gif"
    writer = imageio.get_writer(file_name)
    
    
    # Parameters to change animation
    angle_delta = 10.0  # amount to rotate fractal by each frame
    axes = [[1, 1, 0], [1, .5, .5], [1, 0, 1], [.5, 0, 1], [1, .5, .5]]  # axes to rotate fractal on, in succession
    
    for axis in axes:
        for rotate in range(int(360/angle_delta)):
            im = canvas.render()
            writer.append_data(im)
            view.camera.transform.rotate(angle_delta, axis)
    writer.close()
    

''' Run program '''

if __name__ == '__main__':
    print(__doc__)
    app.run()
    
end = timer()
print("elapsed time: " + str(end - start))
