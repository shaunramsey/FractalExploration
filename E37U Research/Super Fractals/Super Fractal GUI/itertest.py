import numpy as np
num =100
a = 0.1
n = 6
e_to_the_a = np.exp(a)   
bC1 = 0
bC2 = 0
steps = 50
def L(a):
    return e_to_the_a + 1

def U(a):
    return ( np.sqrt(np.exp(2 * a) + (8 * e_to_the_a) ) + e_to_the_a + 2) / 2

lowerbound = L(a)
upperbound = U(a)

def getbval(curr_iteration, b1, b2):
    if (curr_iteration % (2 * n) < n):
        global bC1
        bC1 += 1
        return b1
    else:
        global bC2
        bC2 += 1
        return b2

# RETURNS THE LYAPUNOV EXPONENT BASED ON THE SPECIFIED B1 AND B2 VALUES
def getlyapexponent(b1, b2):
    for i in range(num):
        getbval(i, b1, b2)


b1 = np.linspace(lowerbound, upperbound, steps)   #range of b1 values
b2 = np.linspace(lowerbound, upperbound, steps)   #range of b2 values

for i in b1:
    for j in b2: 
        getlyapexponent(i, j)

print("b1: " + str(bC1))
print("b2: " + str(bC2))