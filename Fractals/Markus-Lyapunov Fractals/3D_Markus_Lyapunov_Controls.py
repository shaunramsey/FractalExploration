
'''
This is a version of 3D_Markus_Lyapunov.py, but with controls to create an animation or save a still image. It can be significantly slower than 3D_Markus_Lyapunov.py, so it is included as a seperate file.

Adapted from VisPy example volume rendering here: https://github.com/vispy/vispy/blob/master/examples/basics/scene/volume.py. File dialog taken from here: https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python. Normalization approach credited to Etienne Cmb on Stack Overflow: https://stackoverflow.com/questions/51306488/transparency-with-voxels-in-vispy/51309283#51309283. 

Controls:
    set anim under CONTROLS to True - save .gif of rotating fractal
    set load_file under CONTROLS to file path - load .npy data into canvas
    'l' - load fractal data into canvas
    'e' - export fractal data to .npy file
    's' - save still from canvas to .png
    lmb - rotate
    rmb - zoom
    shift + lmb - pan
    shift + rmb - change field of view
'''

# NUMPY AND OPTIMIZATION
from numba import jit
import numpy as np

# VISPY IMPORTS
import imageio
import vispy.io as io
from vispy import app, scene
from vispy.color import Colormap
from vispy.scene.visuals import Text
from vispy.app.timer import Timer

# FILE DIALOG
import tkinter as tk
from tkinter import filedialog

# TIMER
from timeit import default_timer as timer

start = timer()


'''
Computing Fractal
'''

# CONTROLS
anim = False        # change whether to produce a .gif animation of fractal rotating
load_data = None    # change to complete path of .npy file to load fractal data

# PARAMETERS TO CHANGE THE FRACTAL GENERATED
seq = "ABC"    # sequence to alternate r values
a_lb = 2            # a lower bound
a_ub = 4            # a upper bound
b_lb = 2            # b lower bound
b_ub = 12            # b upper bound
c_lb = 2            # c lower bound
c_ub = 4            # c upper bound

# PARAMETERS REFINING ACCURACY OF FRACTAL PICTURE GENERATED
num_warmups = 200             # number of "warmups" or throwaway iterations before computing lyapunov exponent
num_lyap_iterations = 100     # number of iterations used to compute the lyapunov exp
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

# RETURNS FRACTAL MAP
@jit
def getfractalcolormap(chaotic_boundary):
    fractal_colors = [(1, 0, 1, .5), (0, 0, 1, .5), (.1, .8, .8, .3), (.1, 1, .1, .3), (1, 1, 0, .2), (1, 0, 0, .1), (1, 1, 1, (1 - chaotic_boundary) / 7), (0, 1, .8, (1 - chaotic_boundary) / 8), (0, 0, 0, 0), (0, 0, 0, 0)]
    color_control_pts = [0, (0.6 * chaotic_boundary), (0.7 * chaotic_boundary), (0.8 *  chaotic_boundary), (0.9 * chaotic_boundary), (0.95 * chaotic_boundary), (0.97 * chaotic_boundary), (0.99 * chaotic_boundary), chaotic_boundary, chaotic_boundary, 1.0]

    fractal_map = Colormap(fractal_colors, controls=color_control_pts, interpolation='zero')
    
    return fractal_map

'''
Creating and Preparing 3D Fractal Data
'''

# CREATING FRACTAL IMAGE / LOADING FRACTAL DATA
if load_data == None:
    a = np.linspace(a_lb, a_ub, steps)   #range of b1 values
    b = np.linspace(b_lb, b_ub, steps)   #range of b2 values
    c = np.linspace(c_lb, c_ub, steps)
    
    aa, bb, cc = np.meshgrid(a, b, c, indexing = 'ij') # meshgrid return y, x, z
    
    fractal_data = getlyapexponent(aa, bb, cc)
else:
    fractal_data = np.load(load_data)

# normalize data between 0 and 1 to be displayed and return chaotic boundary
fractal_3D, chaotic_boundary = normalize(fractal_data, 0.0)


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
fractal_map = getfractalcolormap(chaotic_boundary)
volume.cmap = fractal_map


'''
Implementing key press 
's' - save still from canvas
'a' - begin animation to rotate fractal
'''

# INITALIZING KEY PRESS VARIABLES
# Still images
still_num = 1
num_frames = 20

# Loading data
loaded_data_later = False     # boolean to determine if data has been loaded

# User message
usr_message = Text('Message to user', parent=canvas.scene, color=(1, 1, 1, 0), anchor_x = 'left', anchor_y = 'top') # starts off invisible
usr_message.font_size = 15
usr_message.pos = canvas.size[0] // 22, canvas.size[1] // 22
fade_out = Timer(interval = 0.07, iterations = num_frames)


# Connecting timer to fading out function
@fade_out.connect
def text_fade(event):
    transparency = 1 - ( (event.iteration + 1) * (1 / num_frames) )
    usr_message.color = (1, 1, 1, transparency )

# Implement key presses
@canvas.events.key_press.connect
def on_key_press(event):
    if event.text == 's':
        global still_num
        
        # Stop preexisting animation
        fade_out.stop()
        usr_message.text = 'Saved still image'
        usr_message.color = (1, 1, 1, 0)
        
        # Write screen to .png
        still = canvas.render()
        still_name = str(seq) + "_" + str(still_num) + ".png"
        io.write_png(still_name, still)
        still_num = still_num + 1
        
        # Display and fade saved message
        fade_out.start()
        
    if event.text == 'e':
        global load_data
        
         # Stop preexisting animation
        fade_out.stop()
        usr_message.color = (1, 1, 1, 0)
        
        if load_data == None:
            global fractal_data
            
            # export data created in this program
            file_name = "3D_Fractal_" + seq + "_steps" + str(steps)
            np.save(file_name, fractal_data, allow_pickle=False)
            
            # set user message
            usr_message.text = 'Exported fractal'
        else:
            # set user message
            usr_message.text = 'Cannot export data loaded into program'
        
        # display user message
        fade_out.start()
        
    if event.text == 'l':
        global volume, loaded_data_later
        loaded_data_later = True
        
        # Stop preexisting animation
        fade_out.stop()
        usr_message.color = (1, 1, 1, 0)
        
        # open file dialog to select load data
        root = tk.Tk()
        root.withdraw()
        load_data = filedialog.askopenfilename()
        
        # make sure file extension is .npy
        file_ext = load_data[len(load_data)-3:]
        if file_ext != 'npy':
            usr_message.text = 'Can only load .npy files'
        else:
            usr_message.text = 'Fractal loaded'
            
            # load fractal data 
            fractal_data = np.load(load_data)
            
            # normalize data and get color map
            fractal_3D, chaotic_boundary = normalize(fractal_data, 0.0)
            fractal_map = getfractalcolormap(chaotic_boundary)
            
            # erase old volume
            volume.parent = None
            
            # make new volume from normalized fractal data
            volume = scene.visuals.Volume(fractal_3D, clim=(0, 1), method='translucent', parent=view.scene, threshold=0.225, cmap=fractal_map, emulate_texture=False)
            
        # display user message
        fade_out.start()
        
        
        
''' 
Creating animation of rotating fractal 
'''

if anim:
    file_name = "Anim_3D_Fractal_" + seq + "_steps" + str(steps) + ".gif"
    writer = imageio.get_writer(file_name)
    
    
    # Parameters to change animation
    angle_delta = 10.0  # amount to rotate fractal by each frame
    axes = [[1, 1, 0], [1, .5, .5], [1, 0, 1], [.5, 0, 1], [1, .5, .5]]  # axes to rotate fractal on, in succession
    
    for axis in axes:
        for rotate in range(360 // angle_delta): # integer division of angle deltas in 360 deg
            im = canvas.render()
            writer.append_data(im)
            view.camera.transform.rotate(angle_delta, axis)
    writer.close()
    

''' 
Run program 

'''

if __name__ == '__main__':
    print(__doc__)
    app.run()
    
end = timer()
print("elapsed time: " + str(end - start))

