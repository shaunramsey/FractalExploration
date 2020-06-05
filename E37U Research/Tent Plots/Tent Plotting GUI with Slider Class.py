import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation
import math

##Begin Default Values

aDefault = .5
bDefault = .5
precisionDefault = 2
figureDPI = 50 #DPI value for main figure
fontSizeDefault = 20 #Default font size

##End Default Values
##Begin Bin Class Section

class bin:
    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.binContent = kwargs.get('content')
    def setContent(self, content):
        self.binContent = content
    def clearContent(self):
        self.binContent = 0
    def getContent(self):
        return self.binContent
    def getID(self):
        return str(self.start) + "," + str(self.end)

##End Bin Class Section
##Begin Bin Initialization Section

def binIni(binSize):
    binList= []
    for i in range(1/binSize):
        binList.append(bin(start=(i*binSize), end=((i*binSize)+binSize)))
    return binList
        

##End Bin Initialization Section

root = tkinter.Tk()
root.title('Tent Plotting GUI')
def on_closing():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

##Begin Font Section

fontStyle = tkFont.Font(family="Times New Roman", size=fontSizeDefault)#TODO Change naming from "fontStyle" to "guiFontStyle"

##End Font Section
##Begin Universal Variables Section

aCallVar = DoubleVar()
bCallVar = DoubleVar()
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

aSlider = slider(title="a", min=0.1, max=0.9, default=aDefault, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=0, callVar=aCallVar)
aSlider.makeSlider()

##End "a" Slider
##Begin "b" Slider

bSlider = slider(title="b", min=0, max=1, default=bDefault, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=1, callVar=bCallVar)
bSlider.makeSlider()

##End "b" Slider
##Begin Precision Slider Section

def rangeTrunkOverride(precision):
    aSlider.setRange(min=precision, max=(1-precision))
    #bSlider.setRange(min=precision, max=(1-precision))

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    aSlider.setPrecision(resolution=precision)
    bSlider.setPrecision(resolution=precision)
    rangeTrunkOverride(precision)

precisionCallVar.trace_add("write", precisionChange)#Tying the callback to the Variable

sliderPrecisionSlider = slider(title="Slider Precision", min=2, max=10, default=precisionDefault, fontStyle=fontStyle, precision=1, row=4, column=2, callVar=precisionCallVar)
sliderPrecisionSlider.makeSlider()
precisionCallVar.set(5)

##End Slider Precision Slider Section
##Begin Font Slider Section

fontSlider = slider(title="Font Size", min=1, max=30, default=fontSizeDefault, fontStyle=fontStyle, precision=1, row=4, column=3, callVar=fontSizeCallVar)
fontSlider.makeSlider()

def fontChange(var, indx, mode):#Callback function for when fontSizeCallVar changes
    fontStyle.configure(size=fontSizeCallVar.get())
    aSlider.setFontStyle(fontStyle=fontStyle)
    bSlider.setFontStyle(fontStyle=fontStyle)
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
    ax1.plot([0, aCallVar.get()], [0, bCallVar.get()], linewidth=1) #first lines 
    ax1.plot([aCallVar.get(), 1], [bCallVar.get(), 0], linewidth=1) #second line
    ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1.5)
    ax1.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)

#End Plot Section

root.mainloop()