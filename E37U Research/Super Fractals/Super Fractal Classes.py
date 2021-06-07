import numpy as np

a = 4.9
n=6

def lowerBound(a): #Lower bound for b for a given a
    return (np.exp(a) + 1)

def upperBound(a): #Upper bound for b for a given a
    return ((np.sqrt(np.exp(2 * a) + 8 * np.exp(a)) + np.exp(a) + 2)/2)

def calcLam(a, b1, b2):
    x = .5
    sum = 0
    initialLoopCount = 50
    postLoopCount = 50
    totalLoopCount = initialLoopCount + postLoopCount
    lam = 0
    for i in range(initialLoopCount):
        x = b * x * (-1*x + 1)
    for i in range(initialLoopCount, totalLoopCount):
        x = b * x * (-1*x + 1)
        f=abs(b * (-2*x +1 ))
        if f < 0.0000000001:
            return -1000000 #Representative of negative infinity
        else:
            sum = sum + (np.log(f))
    lam = sum / postLoopCount
    return lam
    