import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation
import math
from numba import jit
from timeit import default_timer as timer

#a = .1
n=6
steps = 500
##Begin Default Values
aDefault = .5
precisionDefault = 2
figureDPI = 50 #DPI value for main figure
fontSizeDefault = 20 #Default font size

##End Default Values
##Begin Tkinter Initialization

root = tkinter.Tk()
root.title('Super Fractal GUI')
def on_closing():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

##End Tkinter Initialization
##Begin Font Section

fontStyle = tkFont.Font(family="Times New Roman", size=fontSizeDefault)#TODO Change naming from "fontStyle" to "guiFontStyle"

##End Font Section
##Begin Universal Variables Section

aCallVar = DoubleVar()
precisionCallVar = IntVar()
fontSizeCallVar = IntVar()

##End Universal Variables Section
##Begin Slider Section
##Begin Slider Class

class slider:
    def __init__(self, title, min, max, default, fontStyle, precision, row, column, callVar):
        self.title = title
        self.min = min
        self.max = max
        self.default = default
        self.fontStyle = fontStyle
        self.precision = precision
        self.row = row
        self.column = column
        self.callVar = callVar
        self.callVar.set(self.default)
    def makeSlider(self):
        self.frame = Frame(root)
        self.sliderLabel = Label(self.frame,text=self.title, font=self.fontStyle)
        self.sliderLabel.pack()
        self.entry = Entry(self.frame, textvariable=self.callVar, font=self.fontStyle)
        self.entry.pack()
        self.slider = Scale(self.frame, from_=self.min, to=self.max, orient=HORIZONTAL, variable=self.callVar, font=self.fontStyle, showvalue=0, length=200, resolution=self.precision)
        self.slider.pack()
        self.frame.grid(row=self.row, column=self.column)
    def setPrecision(self, resolution):
        self.slider.configure(resolution=resolution)
    def setFontStyle(self, fontStyle):
        self.slider.configure(font=fontStyle)
    def setRange(self, min, max):
        self.slider.configure(from_=min)
        self.slider.configure(to=max)
    def setCommand(self, command):
        self.slider.configure(command=command)

##End Slider Class
##Begin Precision Calculator Function

def calcPrecision(input):#Converts integer range of precision (2-10 on the slider) to the decimal place equivalent
    temp = "."
    for _ in range(input-2):
        temp = temp + "0"
    return float(temp + "1")

##End Precision Calculator Function
##Begin "a" Slider

aSlider = slider(title="a", min=0.1, max=5.9, default=aDefault, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=0, callVar=aCallVar)#TODO Change paramiters for a slider for super fractal
aSlider.makeSlider()

##End "a" Slider
##Begin Precision Slider Section

#def rangeTrunkOverride(precision):
#    aSlider.setRange(min=precision, max=(1-precision))#TODO Change for the constraints for the Super fractal

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    aSlider.setPrecision(resolution=precision)#TODO Change for the constraints for the Super fractal
    #rangeTrunkOverride(precision)#TODO Change for the constraints for the Super fractal

precisionCallVar.trace_add("write", precisionChange)#Tying the callback to the Variable

sliderPrecisionSlider = slider(title="Slider Precision", min=2, max=10, default=precisionDefault, fontStyle=fontStyle, precision=1, row=4, column=2, callVar=precisionCallVar)
sliderPrecisionSlider.makeSlider()
precisionCallVar.set(precisionDefault)

##End Slider Precision Slider Section
##Begin Font Slider Section

fontSlider = slider(title="Font Size", min=1, max=30, default=fontSizeDefault, fontStyle=fontStyle, precision=1, row=4, column=3, callVar=fontSizeCallVar)
fontSlider.makeSlider()

def fontChange(var, indx, mode):#Callback function for when fontSizeCallVar changes
    fontStyle.configure(size=fontSizeCallVar.get())
    aSlider.setFontStyle(fontStyle=fontStyle)
    fontSlider.setFontStyle(fontStyle=fontStyle)
    sliderPrecisionSlider.setFontStyle(fontStyle=fontStyle)

fontSizeCallVar.trace_add("write", fontChange)#Tying the callback to the Variable

##End Font Slider Section
##End Slider Section
##Begin Status Section
##Begin Status Label Class

class statusLabel:
    def __init__(self, title, default, fontStyle, row, column, callVar):
        self.title = title
        self.default = default
        self.fontStyle = fontStyle
        self.row = row
        self.column = column
        self.callVar = callVar
        self.callVar.set(self.default)
    def makeLabel(self):
        self.frame = Frame(root)
        self.title = Label(self.frame,text=self.title, font=self.fontStyle)
        self.title.pack()
        self.status = Label(self.frame, textvariable=self.callVar, font=self.fontStyle)
        self.status.pack()
        self.frame.grid(row=self.row, column=self.column)
    def setFontStyle(self, fontStyle):
        self.title.configure(font=fontStyle)
        self.status.configure(font=fontStyle)
    def update(self):
        self.status.update()
    def setStatus(self, status, **kwargs):
        self.callVar.set(status)
        self.status.config(foreground = kwargs.get('color'))
        self.status.update()

##End Status Label Class
##Begin Calc Status Label

calcStatusCallVar = StringVar()
calcStatusLabel = statusLabel(title="Calculation Status:", default="Idle", fontStyle=fontStyle, row=1, column=4, callVar=calcStatusCallVar)
calcStatusLabel.makeLabel()

##End Calc Status Label
##Begin Calc Time Label

calcTimeCallVar = StringVar()
calcTimeLabel = statusLabel(title="Last Calculation Time:", default="0", fontStyle=fontStyle, row=2, column=4, callVar=calcTimeCallVar)
calcTimeLabel.makeLabel()

##End Calc Time Label
##End Status Section
##Begin Fractal Functions

@jit
def lowerBound(a): #Lower bound for b for a given a
    return (np.exp(a) + 1)

@jit
def upperBound(a): #Upper bound for b for a given a
    return ((np.sqrt(np.exp(2 * a) + 8 * np.exp(a)) + np.exp(a) + 2)/2)

@jit
def getB(i, b1, b2):#Return the correct value for the cuttent iteration
    if( i % (2 * n)< n):
        return b1
    else:
        return b2

@jit
def Func(x, b, a): #FUnction for lyapunov equation
    top = (np.exp(a) * x * (((np.exp(a)-1) * x)- (b * x) + b + 1))
    bottom = ((((np.exp(a)-1) * x) + 1)**2)
    return (top / bottom)

@jit
def Funcp(x, b, a):
    top = (-1 * np.exp(a) * ((x * np.exp(a) + x - 1) * b - (x * np.exp(a)) + x - 1))
    bottom =  (((np.exp(a) - 1 ) * x + 1 )**3)
    return (top / bottom)

@jit
def calcLam(a, b1, b2):
    x = .5
    sum = 0
    initialLoopCount = 1200
    postLoopCount = 100
    totalLoopCount = initialLoopCount + postLoopCount
    lam = 0
    for i in range(initialLoopCount):
        x = Func(x, getB(i, b1, b2), a)
    for i in range(initialLoopCount, totalLoopCount):
        x = Func(x, getB(i, b1, b2), a)
        f=np.abs(Funcp(x, getB(i, b1, b2), a))
        #if f < 0.0000000001:#TODO Determine if necessary 
        #    return -1000000 #Representative of negative infinity
        #else:
        #    sum = sum + (np.log(f))
        sum = sum + (np.log(f))
    lam = sum / postLoopCount
    return lam
##End Fractal Functions
##Begin Plot Section

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
fig.set_size_inches(4, 4)

def plotting(i):
    print("running")
    startTime = timer()
    #calcStatusCallVar.set("Running")
    calcStatusLabel.setStatus("Running", color="Red")
    #calcStatusLabel.update()
    a = aCallVar.get()
    lowerB = lowerBound(a)
    upperB = upperBound(a)
    bList = np.linspace(lowerB, upperB, steps)
    fractal2D = []
    for b1 in bList:
        for b2 in bList:
            fractal2D.append(calcLam(a=a, b1=b1, b2=b2))
    fractal3D = np.reshape(fractal2D, (steps, steps))
    lycm = plt.get_cmap('nipy_spectral')
    lycm.set_over('black')
    ax1.clear()
    ax1.imshow(fractal3D, cmap = lycm, origin = "lower", vmax = 0, extent = (lowerB, upperB, lowerB, upperB))
    ax1.set_title("Super Fractal", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("b1", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("b2", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    #ax1.set_xlim(0,1)#Set limits
    #ax1.set_ylim(0,1.5)#Set limits
    print("idle")
    #calcStatusCallVar.set("Idle")
    calcStatusLabel.setStatus("Idle", color="Green")
    #calcStatusLabel.update()
    endTime = timer()
    calcTimeCallVar.set(str(endTime-startTime)+ " Seconds")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=5000)

#End Plot Section

root.mainloop()