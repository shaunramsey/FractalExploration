# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

a = 1.4
b = 0.3

x = 0.1 #x-axis
y = 0.1 #y-axis
   
for j in range(1, 5000):
    # get new x and y using old values of x and y (with python "swap" technique)
    x, y = b * y, 1 + x - (a * np.multiply(y, y))
    plt.scatter(y, x, s = 0.1)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Henon attractor")
plt.show()