import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tkinter.Tk()
root.title('Plotting GUI')
#root.geometry("2000x1125")

    

def getRSlider(): #Function that returns r from the slider
    return rSlider.get()

def submitFunc(): #Function that updates the plots for a new r retrieved from the slider
    plotting(getRSlider())


#  This is for if you want to auto update with the slider but its very slow (1/2)

#def submitSlide(var):
#    plotting(getRSlider())
#rSlider = Scale(root, from_=0, to=4, orient=HORIZONTAL, resolution=.1, label="R Value", command=submitSlide)

#  This is for if you want to auto update with the slider but its very slow (2/2)

rSlider = Scale(root, from_=0, to=4, orient=HORIZONTAL, resolution=.1, label="R Value")
rSlider.grid(row=1, column=0)
submitButton = Button(root, text="Submit", command=submitFunc)
submitButton.grid(row=1, column=1)

def plotting(rIN):
    r = rIN
    print("r: " + str(r))
    fig1 = plt.figure(dpi=100)
    fig1.set_size_inches(10, 4)

    #Begin Iteration Plot Section
    numIterations = 100 #Number of discrete points in the plot, the resolution per say, TODO make a more accurate name
    x0 = 0.8
    points = [x0] #creates the list that will hold all the points and initializes the list ith the initial point which is required for a iterative equation
    intervalList = [0]
    interval = 1/numIterations
    for i in range(1,numIterations):#makes a big list of intervals between 0 and 1 spaced one "interval" apart
        intervalList.append(i*interval)
    for i in range(1,numIterations): #Creates the list of all the iterations by referencing the previous entry in the list
        points.append((r * points[i-1]) * (1- points[i-1]))
    for i in range(0, numIterations): #for testing, shows all the points that will be passed to the graph and their iterator starting with x0
        print(i, points[i])
    x = intervalList
    plt.subplot(121)
    plt.title("Iterations Plot")
    plt.xlabel("Iterations")
    plt.ylabel("X Values")
    plt.plot(x, points)
    #End Iteration Plot Section

    #Begin Cobweb Plot Section
    cobwebIterations = 100 #number of individual cob web lines to be drawn
    startX = x0 #Input the starting x point here
    plt.subplot(122)
    plt.plot([0,1],[0,1]) #plot y=x line (TODO make to fill the maximum bounds of the other plots not just 0-1)
    xs = np.arange(0,1,.001) #x for parab plot
    ys =(r * xs * (1-xs)) #y for parab plot
    plt.plot(xs, ys) #parab plot
    tempX = startX
    tempY = r * tempX * (-1*tempX + 1)
    plt.plot([tempX, tempX], [0, tempY]) #first lines 
    plt.plot([tempY, tempX], [tempY, tempY])#second line
    for i in range(cobwebIterations):#loop that makes the reset of the cobweb lines
        tempY = r * tempX * (-1*tempX + 1)
        plt.plot([tempX, tempX], [tempX, tempY])
        plt.plot([tempY, tempX], [tempY, tempY])
        tempX=tempY
    plt.title("Cobweb Plot")
    plt.xlabel("X_n Values")
    plt.ylabel("X_n+1 Values")
    #End Cobweb Plot Section

    plt.subplots_adjust(hspace=.5)#Specifies the space between plots
    canvas = FigureCanvasTkAgg(fig1, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

plotting(0) #First plot which is a placeholder until the r slider is used to select the desired r

tkinter.mainloop()