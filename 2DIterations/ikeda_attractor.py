# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

#constants
a = 0.85
b = 0.9
k = 0.4
c = 7.7

z = 0.1 + 0.1j #seed value

for _ in range(5000):
    z = a + (b * z) * np.exp(1j * (k - (c / (1 + (np.multiply( abs(z), abs(z) ) ) ) ) ) ) 
    plt.scatter(z.real, z.imag, s = 0.1)

plt.xlabel("real")
plt.ylabel("imaginary")
plt.title("Ikeda attractor")
plt.show()