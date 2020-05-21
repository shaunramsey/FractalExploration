import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##Begin Default Values

x0SliderDefault = .5 #Slider for Initial x's default value on program startup
rSliderDefault = 3.3 #Slider for r's default value on program startup
sliderPrecision = .1 #Universal Slider Precision's default value on program startup
figureDPI = 100 #DPI value for main figure
numIterations = 100 #Number of iterations in the iteration plot
cobwebStrands = 100 #Number of individual cob web lines to be drawn

##End Default Values


root = tkinter.Tk()
root.title('Plotting GUI')
#root.geometry("2000x1125")
def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


##Begin Slider Section

def submitSlider(var): #Note: "var" is needed to overcome an anomaly with scale commands
    plotting(getRSlider(), getx0Slider(), figureDPI, numIterations, cobwebStrands)

##Begin r Slider Section  

def getRSlider(): #Function that returns r from the slider
    return rSlider.get()

## This is for if you want to auto update r with the slider but its very slow (Begin)
rSlider = Scale(root, from_=0, to=4, orient=HORIZONTAL, resolution=sliderPrecision, label="R Value", command=submitSlider)
## This is for if you want to auto update r with the slider but its very slow (End)

## This is for if you want submit based r slider, faster but not as cool (Begin)
#rSlider = Scale(root, from_=0, to=4, orient=HORIZONTAL, resolution=sliderPrecision, label="R Value")
#submitButton = Button(root, text="Submit", command=submitSlider)
#submitButton.grid(row=1, column=1)
## This is for if you want submit based r slider, faster but not as cool (End)

rSlider.set(rSliderDefault)
rSlider.grid(row=1, column=0)

##End r Slider Section

##Begin x0 Slider Section

def getx0Slider(): #Function that returns x0 from the slider
    return x0Slider.get()

x0Slider = Scale(root, from_=0, to=1, orient=HORIZONTAL, resolution=sliderPrecision, label="Initial X Value", command=submitSlider)
x0Slider.set(x0SliderDefault)
x0Slider.grid(row=1, column=1)

##End x0 Slider Section

##Begin Slider Precision Slider Section

def setSliderPrecision():
    if sliderPrecisionSlider.get() == 1:
        sliderPrecision = 1 #TODO fix scope issue
        
    else:
        tempPrecision = "."
        for i in range((sliderPrecisionSlider.get()-2)):
            tempPrecision = tempPrecision + "0"
        sliderPrecision = float(tempPrecision + "1") #TODO fix scope issue 

sliderPrecisionSlider = Scale(root, from_=1, to=10, label="Slider Precision", command=setSliderPrecision)
sliderPrecisionSlider.grid(row=1, column=2)

##End Slider Precision Slider Section


##End Slider Section

def plotting(r,x0, figureDPI, numIterations, cobwebStrands):
    #print("r: " + str(r)) #NOTE for Testing
    fig1 = plt.figure(dpi=figureDPI)
    fig1.set_size_inches(10, 4)

    #Begin Iteration Plot Section
    points = [x0] #creates the list that will hold all the points and initializes the list ith the initial point which is required for a iterative equation
    intervalList = [0]
    interval = 1/numIterations
    for i in range(1,numIterations):#makes a big list of intervals between 0 and 1 spaced one "interval" apart
        intervalList.append(i*interval)
    for i in range(1,numIterations): #Creates the list of all the iterations by referencing the previous entry in the list
        points.append((r * points[i-1]) * (1- points[i-1]))
    for i in range(0, numIterations): #NOTE for testing, shows all the points that will be passed to the graph and their iterator starting with x0
        print(i, points[i])
    x = intervalList
    plt.subplot(121)
    plt.title("Iterations Plot")
    plt.xlabel("Iterations")
    plt.ylabel("X Values")
    plt.plot(x, points)
    #End Iteration Plot Section

    #Begin Cobweb Plot Section
    plt.subplot(122)
    plt.plot([0,1],[0,1]) #plot y=x line (TODO make to fill the maximum bounds of the other plots not just 0-1)
    xs = np.arange(0,1,.001) #x for parabala plot
    ys =(r * xs * (1-xs)) #y for parabala plot
    plt.plot(xs, ys) #parabala plot
    tempX = x0
    tempY = r * tempX * (-1*tempX + 1)
    plt.plot([tempX, tempX], [0, tempY]) #first lines 
    plt.plot([tempY, tempX], [tempY, tempY])#second line
    for i in range(cobwebStrands):#loop that makes the rest of the cobweb lines
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

submitSlider(0) #First plot which is a placeholder until the r slider is used to select the desired r

tkinter.mainloop()