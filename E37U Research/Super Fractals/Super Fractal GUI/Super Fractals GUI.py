import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation
import math

a = 4.9
n=6
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
#Begin Fractal Functions
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
##End Fractal Functions
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

aSlider = slider(title="a", min=0.1, max=0.9, default=aDefault, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=0, callVar=aCallVar)#TODO Change paramiters for a slider for super fractal
aSlider.makeSlider()

##End "a" Slider
##Begin Precision Slider Section

def rangeTrunkOverride(precision):
    aSlider.setRange(min=precision, max=(1-precision))#TODO Change for the constraints for the Super fractal

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    aSlider.setPrecision(resolution=precision)#TODO Change for the constraints for the Super fractal
    rangeTrunkOverride(precision)#TODO Change for the constraints for the Super fractal

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
##Begin Plot Section

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
fig.set_size_inches(4, 4)

def plotting(i):
    ax1.clear()
    #TODO Add plot for the super fractal
    ax1.set_title("Super Fractal", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("b1", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("b2", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_xlim(0,1)#Set limits
    ax1.set_ylim(0,1.5)#Set limits
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)

#End Plot Section

root.mainloop()