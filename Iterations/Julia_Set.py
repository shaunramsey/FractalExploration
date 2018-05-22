#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:06:43 2018

@author: Michelle 
"""

import matplotlib.pyplot as plt
import numpy as np

initial_zpts = [] #x + iy = (x,y) SEED VALUE
c = .4 - .325j #parameter


high_num = 20000
neg_num = -20000
lowerbound = -1.2
upperbound = 1.2
stepsize = 0.01
#print (dy) 
#for a julia set, you want to change z (the initial value) but keep c the same 

rp = lowerbound
ip = lowerbound

#filling up our initial zpts array with every possible value of complex numbers
while rp < upperbound:
    while ip < upperbound:
        initial_z = complex(rp, ip)    
        z = initial_z #assigns the complex number at initial_zpts[k] to z 
        for i in range(100):
            z = np.multiply(z,z) + c   
            
    #if z goes beyond the set
        if z.real > high_num or z.imag > high_num or z.real < neg_num or z.imag < neg_num:
            plt.scatter(initial_z.real, initial_z.imag, c = 'm', s = 4)
     #if z falls within the set   
            if i > 30:
                color = "m"
            if i <= 30 and i > 10:
                color = "blue"
            else:
                color = "red"
        if z.real < high_num or z.imag < high_num:
            plt.scatter(initial_z.real, initial_z.imag, c = 'k', s = 4)
            
        ip += stepsize    
    rp += stepsize
    ip = lowerbound
    
plt.xlabel("real")
plt.ylabel("imaginary")
plt.title("Julia Set")
plt.show()