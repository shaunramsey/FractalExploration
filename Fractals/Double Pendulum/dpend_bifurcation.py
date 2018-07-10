# -*- coding: utf-8 -*-

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from timeit import default_timer as timer

start_timer = timer()

# CONSTANTS OF DOUBLE PENDULUM MOTION
G = 9.8   # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg

# DIFFERENTIAL EQUATIONS TO SOLVE TO FIND OUT MOTION OF DOUBLE PENDULUM
def derivs(state, t):
    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2] - state[0]
    den1 = (M1 + M2)*L1 - M2*L1*cos(del_)*cos(del_)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_) +
               M2*G*sin(state[2])*cos(del_) +
               M2*L2*state[3]*state[3]*sin(del_) -
               (M1 + M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(state[0])*cos(del_) -
               (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
               (M1 + M2)*G*sin(state[2]))/den2

    return dydx

# INTEGRATING TH2 SYSTEM
# range of initial theta values (i.e., x-axis fidelity)
start = -10
end = 10
stepsize = .05

# creating time to iterate each initial th2 value over
num_warmups = 0         # number of values to discard when plotting
num_iterations = 30   # number of values to actually plot
dt = 0.05               # timestep of time range to iterate each initial th2 value over
t = np.arange(0, (num_warmups + num_iterations) * dt, dt)   # endpt of t is len * step_size

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = 180.0
w1 = 0.0
th2 = np.arange(start, end, stepsize)
w2 = 0.0

# ACCEPTING ALL TH2 INITIAL VALUES AND THEN ITERATING THEM OVER TIME T
def get_system_over_th2_initial(th2):
    th2_systems_over_time = []
    for curr_initial_th2 in th2:
        state = np.radians([th1, w1, curr_initial_th2, w2])

        th2_systems_over_time.append(integrate.odeint(derivs, state, t))
    
    return th2_systems_over_time
    
# integrating system over time to see what value th2 goes to
# th2_systems = np.mod(np.array(get_system_over_th2_initial(th2)), np.pi)
th2_systems = np.mod(np.degrees(get_system_over_th2_initial(th2)), 180)

# CREATING GRAPH AND PLOTTING DATA
plt.figure()
plt.plot(th2, th2_systems[:, num_warmups:, 2], marker = 'o', markersize = 2, linewidth = 0)

plt.xlabel("initial theta 2 (position of pendulum 2 in degrees)")
plt.ylabel("orbit of theta 2 over time (position of pendulum 2 in degrees)")
plt.suptitle("Bifurcation of double pendulum / " + str(num_warmups) + " warmups, " + str(num_iterations) + " iterations")
plt.title("Constants -- theta 1: " + str(th1) + " / w1: " + str(w1) + " / w2: " + str(w2))
plt.show()

end_timer = timer()
print("elapsed time:", (end_timer - start_timer))