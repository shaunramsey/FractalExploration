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

precisionDefault = 2
figureDPI = 50 #DPI value for main figure
fontSizeDefault = 20 #Default font size

##End Default Values
##Begin Bin Section
##Begin Bin Class Section

class bin:
    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.binContent = kwargs.get('content')
        if self.binContent == None:
            self.binContent = 0
        self.binSize = self.end - self.start
    def setContent(self, content):
        self.binContent = content
    def addContent(self, content):
        self.binContent = self.binContent + content
    def clearContent(self):
        self.binContent = 0
    def getContent(self):
        return self.binContent
    def getID(self):
        return (str(self.start) + "," + str(self.end))
    def percentageOfRange(self, rangeStart, rangeEnd):
        if rangeStart > rangeEnd:
            rangeStart, rangeEnd = rangeEnd, rangeStart
        #The logic for testing if two ranges intersect comes from Ned Batchelder's blog:
        #https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
        if self.end >=rangeStart and rangeEnd >= self.start:  
            #The logic for finding the intersection of the two ranges is inspired by User Oscar Smith's reply on StackExchange:
            #https://codereview.stackexchange.com/questions/178427/given-2-disjoint-sets-of-intervals-find-the-intersections/178432#178432
            return ((min(self.end, rangeEnd)-max(self.start, rangeStart))/(rangeEnd-rangeStart))
        else:
            return 0

##End Bin Class Section
##Begin Bin Initialization Section

def binIni(binSize):
    binList = []
    for i in range(0, int(1/binSize)):
        #print(int(1/binSize))
        binList.append(bin(start=(i*binSize), end=((i*binSize)+binSize)))
        #print("Start= " + str(i*binSize)+ ", End= " + str((i*binSize)+binSize))
    return binList
        
##End Bin Initialization Section
##End Bin Section
##Begin Equation Section
##Begin Equation Class Section

class equation:
    def __init__(self, **kwargs):
        self.m = kwargs.get('m')
        self.b = kwargs.get('b')

        if self.m == None:
            self.m = 0.0

        if self.b == None:
            self.b = 0.0

        self.xi = kwargs.get('xi')
        self.xf = kwargs.get('xf')
        self.yi = kwargs.get('yi')
        self.yf = kwargs.get('yf')

        if self.xi == None:
            self.xi = 0.0

        if self.xf == None:
            self.xf = 1.0

        if self.yi == None:
            self.yi = 0.0

        if self.yf == None:
            self.yf = 1.0

        self.calcEQ()
       
    def calcEQ(self):
        self.m = ((self.yf - self.yi)/(self.xf - self.xi))
        self.b = (self.xi - self.m * self.xi)
    def getString(self):
        if self.m == 0:
            return self.b
        if self.b > 0:
            return str(self.m) + "x+" + str(self.b)
        elif self.b < 0:
            return str(self.m) + "x" + str(self.b)
        else:
            return str(self.m) + "x"
    def getM(self):
        return self.m
    def getB(self):
        return self.b
    def isBNegative(self):
        if self.b < 0:
            return True
        else:
            return False
    def setM(self, m):
        self.m = m
    def setB(self,b):
        self.b = b
    def setFromString(self, equationString): #Pass in equationString in the form of "mx+b", "mx-b", "-mx+b", "-mx-b", "mx" or "-mx"
        if len(equationString) == 0:
            return
        if equationString[0] == "-":
            self.setM(float(equationString[0]+equationString[1]))
            if len(equationString) == 3:
                return
            elif equationString[3] == "-":
                self.setB(float(equationString[3]+equationString[4]))
            else:
                self.setB(float(equationString[4]))
        else:
            self.setM(float(equationString[0]))
            if len(equationString) == 2:
                return
            elif equationString[2] == "-":
                self.setB(float(equationString[2]+equationString[3]))
            else:
                self.setB(float(equationString[3]))
    def getX(self, y):
        return((y-self.b)/self.m)
    def getY(self, x):
        return((x * self.m)+self.b)

    def setInitialPoint(self, x, y):
        self.xi = x
        self.yi = y
        self.calcEQ()
    def setFinalPoint(self, x, y):
        self.xf = x
        self.yf = y
        self.calcEQ()

class tentEquation:
    def __init__(self, equation0, equation1):
        self.equation0 = equation0
        self.equation1 = equation1
    #def getX(self, y): #Cant pass only one point back because, well you know, so not writing now for ease
    def getIntersection(self):
        a = self.equation0.m
        b = self.equation1.m
        c = self.equation0.b
        d = self.equation1.b
        x = ((d-c)/(a-b))
        y = (a * (d-c)/(a-b)+c)
        return (x,y)

    def getY(self, x):
        if x <= self.getIntersection()[0]:
            return self.equation0.getY(x)
        else:
            return self.equation1.getY(x)

##End Equation Class Section
##End Equation Section

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
##Begin Peak Point Slider Section

equation1 = equation(xi=0, xf=.5, yi=0, yf=1)
equation2 = equation(xi=.5, xf=1, yi=1, yf=0)

peakXCallVar = DoubleVar()
peakYCallVar = DoubleVar()

peakXSlider = slider(title="Peak X Slider", min=.1, max=.9, default=.5, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=0, callVar=peakXCallVar)
peakXSlider.makeSlider()

peakYSlider = slider(title="Peak Y Slider", min=.1, max=1, default=1, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=1, callVar=peakYCallVar)
peakYSlider.makeSlider()

def traceX1(var, indx, mode):
    equation1.setFinalPoint(x=peakXCallVar.get(), y=equation1.yf)
def traceX2(var, indx, mode):
    equation2.setInitialPoint(x=peakXCallVar.get(), y=equation2.yi)
def traceY1(var, indx, mode):
    equation1.setFinalPoint(x=equation1.xf, y=peakYCallVar.get())
def traceY2(var, indx, mode):
    equation2.setInitialPoint(x=equation2.xi, y=peakYCallVar.get())

peakXCallVar.trace_add("write", traceX1) #Tying the callback to the Variable
peakXCallVar.trace_add("write", traceX2) #Tying the callback to the Variable

peakYCallVar.trace_add("write", traceY1) #Tying the callback to the Variable
peakYCallVar.trace_add("write", traceY2) #Tying the callback to the Variable

##End Peak Point Slider Section
##Begin Precision Slider Section
def rangeTrunkOverride(precision):
    peakXSlider.setRange(min=precision, max=(1-precision))
    peakYSlider.setRange(min=precision, max=peakYSlider.max)

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    peakXSlider.setPrecision(resolution=precision)
    peakYSlider.setPrecision(resolution=precision)
    rangeTrunkOverride(precision)

precisionCallVar.trace_add("write", precisionChange)#Tying the callback to the Variable

sliderPrecisionSlider = slider(title="Slider Precision", min=2, max=10, default=precisionDefault, fontStyle=fontStyle, precision=1, row=4, column=3, callVar=precisionCallVar)
sliderPrecisionSlider.makeSlider()
precisionCallVar.set(precisionDefault)

##End Slider Precision Slider Section
##Begin Font Slider Section

fontSlider = slider(title="Font Size", min=1, max=30, default=fontSizeDefault, fontStyle=fontStyle, precision=1, row=4, column=4, callVar=fontSizeCallVar)
fontSlider.makeSlider()

def fontChange(var, indx, mode):#Callback function for when fontSizeCallVar changes
    fontStyle.configure(size=fontSizeCallVar.get())
    peakXSlider.setFontStyle(fontStyle=fontStyle)
    peakYSlider.setFontStyle(fontStyle=fontStyle)
    fontSlider.setFontStyle(fontStyle=fontStyle)
    sliderPrecisionSlider.setFontStyle(fontStyle=fontStyle)

fontSizeCallVar.trace_add("write", fontChange)#Tying the callback to the Variable

##End Font Slider Section
##End Slider Section
##Begin Lam Calculation Section

def calcLam(teq1, teq2, x0):
    x = x0
    sum = 0
    tempEquation = tentEquation(teq1, teq2)
    initialLoopCount = 100
    postLoopCount = 100
    totalLoopCount = initialLoopCount + postLoopCount
    lam = 0
    for i in range(initialLoopCount):
        x = tempEquation.getY(x)
    for i in range(initialLoopCount, totalLoopCount):#TODO FIXME FIXME FIXME
        x = tempEquation.getY(x)
        #f=np.abs(Funcp(x, getB(i, b1, b2), a))#TODO FIXME FIXME FIXME
        #if f < 0.0000000001:#TODO Determine if necessary 
        #    return -1000000 #Representative of negative infinity
        #else:
        #    sum = sum + (np.log(f))
        sum = sum + (np.log(x))
    lam = sum / postLoopCount
    return lam

##End Lam Calculation Section
##Begin Lam Label

lamCallVar = DoubleVar()
lamFrame = Frame(root)
lamLabelTitle = Label(lamFrame, text="Lyapunov Exponent:", font=fontStyle)
lamLabelTitle.pack()
lamLabel = Label(lamFrame, textvariable=lamCallVar, font=fontStyle)
lamLabel.pack()
lamFrame.grid(row=0, column=4)

##End Lam Label
##Begin Plot Section

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
fig.set_size_inches(4, 4)

def plotting(i):
    ax1.clear()
    ax1.plot([equation1.xi, equation1.xf], [equation1.yi, equation1.yf], linewidth=1) #first lines 
    ax1.plot([equation2.xi, equation2.xf], [equation2.yi, equation2.yf], linewidth=1) #second line
    ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1.5)
    ax1.grid(True)
    lamCallVar.set(calcLam(teq1=equation1, teq2=equation2, x0=.5))#TODO initial x FIX

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)
##End Plot Section

root.mainloop()