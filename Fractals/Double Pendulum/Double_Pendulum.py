#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:20:31 2018
Double Pendulum Code taken from
@author: Michelle
"""

"""
===========================
The double pendulum problem
===========================

This animation illustrates the double pendulum problem.
Original Code from matplotlib.org

Pendulum tracking code added by Michelle Ly
"""

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from numpy import sin, cos
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg


def derivs(state, t):

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

# create a time array from 0..100 sampled at 0.05 second steps
dt = 0.05
t = np.arange(0.0, 200 * dt, dt)

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)

th1 = -170.0
w1 = 0.0
th2 = 170.00
w2 = 0.0

# initial state -- passing in th1, th2, w1, w2 as radians
state = np.radians([th1, w1, th2, w2])
#print("state", state)
# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)
#print(y)
print(y.shape)
#print(len(y))
#multiply sin/cos of everything at index 0/2 by L1/l2 (the length of the pendulums)
#these are our x and y coordinates for the pendulums
#this slice command says in the 2d array y, print everything in the first dimension
#and print every value at index 0 in the second dimension
x1 = L1*sin(y[:, 0])
y1 = -L1*cos(y[:, 0])
#print(x1.shape)
#print(y1.shape)

x2 = L2*sin(y[:, 2]) + x1
y2 = -L2*cos(y[:, 2]) + y1

#plots all the second x and y coordinates on a separate graph all at once
#plt.scatter(x2, y2, s = 2, c = 'b')

#CREATE THE FIGURE WHERE WE GRAPH THE PENDULUM
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))


ax.grid()

line, = ax.plot([], [], 'o-', lw=.5, color = "m")
pendulum1, = ax.plot([], [], '--', lw= 0.5, color = "r")
pendulum2, = ax.plot([], [], '--', lw= 0.5, color = "b")
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    
    time_text.set_text('')
    return line, time_text


def animate(i):
    #for every value of i, thisx and thisy are assigned with the x and y coordinates at i
    #as an array, so both can be graphed onto line at once
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data( thisx, thisy )
    pendulum1.set_data(x1[:i], y1[:i])
    pendulum2.set_data(x2[:i], y2[:i])
  
    time_text.set_text(time_template % (i*dt))
    return line, pendulum1, pendulum2, time_text


ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=15, init_func=init)


plt.rcParams['animation.convert_path'] = "/ImageMagick-7.0.7/bin/magick"

ani.save('15_double_pendulum.gif', fps=75, writer = 'imagemagick')

