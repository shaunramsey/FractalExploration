# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D

# constants (in original model of convection, parameters describing the character of the model)
sigma = 10.0    # sigma - ratio of gas viscosity to thermal conductivity
rho = 28.0      # rho - horizontal temp distribution
beta = 8.0/3.0  # beta - vertical temp distribution

# differential equations for odeint to integrate
def lorenzeqs(system_state, t):
    x, y, z = system_state
    
    # calculate solutions using Lorenz equations
    solutions = [sigma * (y - x), (rho * x) - y - (x * z), (x * y) - (beta * z)]
    return solutions
    
 # create 3D plot to plot iterations
fig = plt.figure()
_3Dplt = fig.add_subplot(111, projection='3d')

# time range to iterate over
time = np.arange(0, 50, 0.01)
    
#iterate over y range from 1 to 10, creating 10 different versions of the attractor with diff initial y-coords
for y in range(1, 10):
    # initial x, y, z    
    initial_conditions = [1.0, y, 5.0]
    # create points with odeint, using the Lorenz equations, the initial conditions, and time range
    lorenz_attractor = odeint(lorenzeqs, initial_conditions, time)

     #':' graphs EVERY element--so, ':, 0' graphs every element in the first index, the x index
    _3Dplt.plot(lorenz_attractor[:, 0], lorenz_attractor[:, 1], lorenz_attractor[:, 2]) 
   
_3Dplt.set_title("Lorenz attractor")
plt.show()