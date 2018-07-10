#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:55:25 2018
The double pendulum fractal image, restarting from a fresh perspective

This code measures how long it takes for a double pendulum to flip
@author: Michelle
"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import time
from numba import jit

start_timer = time.time()
G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg

#different limits of time steps to test

limit_green = (10 * ( np.sqrt(L1/G) )  )
limit_red = (100 * ( np.sqrt(L1/G) ) ) 
limit_purple = (1000 *  (np.sqrt(L1/G ) ) ) 
limit_blue = (10000 * ( np.sqrt(L1/G ) ) ) 
limits = [0.0, limit_green, limit_red, limit_purple, limit_blue]
print(limits)

#th1 and th2 are initial angles (in radians)
#w1 and w1 are initial velocities
pixels = 100
w1 = 0.0
w2 = 0.0

th1 = np.linspace(-3, 3, pixels) 
th2 = np.linspace(-3, 3, pixels) 

'''
get the system over t 
'''

@jit
def system_over_t(state, t):

    #create dydx as an array of zeros with the same width and height as state
    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2] - state[0]
    den1 = ( M1 + M2 ) * L1 - M2 * L1 * cos(del_) * cos(del_)
    dydx[1] = ( M2 * L1 * state[1] * state[1] * sin(del_) * cos(del_) +
               M2 * G * sin(state[2]) * cos(del_) +
               M2 * L2 * state[3] * state[3] * sin(del_) -
               (M1 + M2) * G * sin(state[0]) )/ den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(state[0])*cos(del_) -
               (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
               (M1 + M2)*G*sin(state[2]))/den2

    return dydx

'''
This function takes in a starting value and an limiting value for the timescale, and then runs system under t
to return the state of theta movements

'''
@jit
def get_next_system(start, lim, th1, th2):
    dt = 0.05
    t = np.arange(start * dt, lim * dt, dt)
    tht_state = []
        # initial state -- saving the four initial settings to a single list
    state = [th1, w1, th2, w2]
    # integrating and then appending our radians to a list
    tht_state = integrate.odeint(system_over_t, state, t)
    
    return tht_state

'''
takes a theta state and checks if a flip occurs

RETURNS either the number at i or the 0
'''
@jit
def find_that_flip(theta):
     flip_yes = 0
     temp = 0
     for i in range(len(theta) ): #for the length of the theta value
         if(theta[i] - theta[0]) > (2 * np.pi) or (theta[i] - theta[0]) < (-2 * np.pi):
             temp = i
             flip_yes += 1 
             break
             
     if flip_yes > 0:
        #print("flip found!")
        return temp
        
     return flip_yes
        
            
   
'''
run the for loop, where each iteration of i uses tests within one of the color limits
if a flip is found, it breaks out of the for loop and returns that value
if no flip is found, the next iteration of i is used
'''
def tests(theta_1, theta_2):

    '''
    this for loop takes each limit time step defined at the start and sets them as parameters
    for the timerange of the system. then slices are taken of those systems to be all the theta1 and theta2
    '''
    for i in range(len(limits) - 1):
        
        system = get_next_system(limits[i], limits[i + 1], theta_1, theta_2 )
        
        theta1 = (system[:, 0])
        theta2 = (system[:, 2])
        
        theta_flip = find_that_flip(theta1)
        
        if theta_flip != 0:
            break
        
        else:   
            theta_flip = find_that_flip(theta2)
        
            if theta_flip != 0:
                break
        
    #now we must test the system and see if a flip occurs in theta1 OR theta2
    
    #the function ultimately returns where the first flip is found and what test
    return theta_flip

'''
#this way creates a grid of zeros that are written over with the flip times
fractal_grid = np.zeros([pixels,pixels])
for i in range(pixels):
    for j in range(pixels):
        fractal_grid[i,j] = tests(th1[j], th2[i])

'''

@jit
def run_it(tht1, tht2):
    fractal_grid = []
    for i in tht1:
        for j in tht2:
            fractal_grid.append( tests(j,i) ) 
            
    fractal_grid = np.reshape(fractal_grid, [pixels, pixels])
    
    return fractal_grid


init_theta1 = th1
init_theta2 = th2
fractal_grid = run_it(init_theta1, init_theta2)
#print(fractal_grid)

'''
CREATING THE FRACTAL IMAGE
so 0 in the fractal_grid represents that a flip doesn't occur within any of the limits
so 0 = over 10000 * sqrt(L/G)

'''
lyap_cmap = plt.get_cmap("nipy_spectral")
#lyap_cmap.set_over('white')
lyap_cmap.set_under('white')

plt.figure()
plt.xlabel("Initial Theta 1")
plt.ylabel("Initial Theta 2")
plt.suptitle("Double Pendulum Fractal")
plt.title("Pixels = " + str(pixels))
fractal_im = plt.imshow(fractal_grid, cmap = lyap_cmap, vmin = 1)
plt.colorbar(fractal_im)

end_timer = time.time()
print("This took", end_timer - start_timer, "seconds to execute")


'''
times

These times test two different ways to create the fractal image
zeros = creating a grid outright and filling it up
reshape = filling up a list and then shaping it to be a grid
5 pixels:
    np zeros: 2.33 seconds
    np reshape: 2.81 seconds
    
10 pixels:
    zeros: 7.55 seconds
    reshape: 6.78 seconds
    
15 pixels:
    zeros: 15.49 seconds 
    reshape: 15.94 seconds

25 pixels:
    zeros: 43.72 seconds
    reshape: 41.10 seconds

50 pixels:
    zeros: 168.45 seconds
    reshape: 168.35 seconds
    
100 pixels:
    zeros: 735. 823 seconds
    reshape: 713.06 seconds
'''
