import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np



##Begin Default Values

x0 = .5 #Slider for Initial x's default value on program startup
#r = 3.3 #Slider for r's default value on program startup
figureDPI = 50 #DPI value for main figure
numIterations = 100 #Number of iterations in the iteration plot
cobwebStrands = 100 #Number of individual cob web lines to be drawn
fontSizeDefault = 20 #Default font size

##End Default Values

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

ra=3.3

def animate(i):
    r = 2 + float("."+ str(i))
    ax1.clear()
    ax1.plot([0,1],[0,1]) #plot y=x line (TODO make to fill the maximum bounds of the other plots not just 0-1)
    xs = np.arange(0,1,.001) #x for parabala plot
    ys =(r * xs * (1-xs)) #y for parabala plot
    ax1.plot(xs, ys) #parabala plot
    tempX = x0
    tempY = r * tempX * (-1*tempX + 1)
    ax1.plot([tempX, tempX], [0, tempY]) #first lines 
    ax1.plot([tempY, tempX], [tempY, tempY])#second line
    for i in range(cobwebStrands):#loop that makes the rest of the cobweb lines
        tempY = r * tempX * (-1*tempX + 1)
        ax1.plot([tempX, tempX], [tempX, tempY])
        ax1.plot([tempY, tempX], [tempY, tempY])
        tempX=tempY

ani = animation.FuncAnimation(fig1, animate, interval=100, frames=200, blit=TRUE)
plt.show()