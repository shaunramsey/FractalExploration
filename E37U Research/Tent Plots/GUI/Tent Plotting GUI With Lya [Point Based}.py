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

        self.isPointBased = False
        #TODO Add logic for handling if nothing is passed in, i.e. also a "self.isMB_Based"

        if self.m == None:
            self.m = 0.0

        if self.b == None:
            self.b = 0.0


        self.xi = kwargs.get('xi')
        self.xf = kwargs.get('xf')
        self.yi = kwargs.get('yi')
        self.yf = kwargs.get('yf')

        if self.xi != None or self.xf != None or self.yi != None or self.yf == None:
            self.isPointBased = True
        #TODO clean up logic here
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
        if self.isPointBased == True:
            self.m = ((self.yf - self.yi)/(self.xf - self.xi))
            self.b = (self.yi - self.m * self.xi)
    def getString(self):
        if self.m == 0:
            return self.b
        if self.b > 0:
            return "{0:.2f}".format(self.m) + "x+" + "{0:.2f}".format(self.b)
        elif self.b < 0:
            return "{0:.2f}".format(self.m) + "x" + "{0:.2f}".format(self.b)
        else:
            return "{0:.2f}".format(self.m) + "x"
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
        #print("M:" + str(self.m) + " B:" + str(self.b) + " x:" + str(x) + " y:" + str((x * self.m)+self.b))
        return((x * self.m)+self.b)

    def setInitialPoint(self, x, y):
        self.xi = x
        self.yi = y
        self.isPointBased = True
        self.calcEQ()
    def setFinalPoint(self, x, y):
        self.xf = x
        self.yf = y
        self.isPointBased = True
        self.calcEQ()

class tentEquation:
    def __init__(self, equation0, equation1):
        self.equation0 = equation0
        self.equation1 = equation1
    #def getX(self, y): #Cant pass only one point back because, well you know, so not writing now for ease
    def getIntersection(self):
        x = self.equation0.xf
        y = self.equation0.yf
        return (x,y)

    def getY(self, x):
        if x <= self.getIntersection()[0]:
            return self.equation0.getY(x)
        else:
            return self.equation1.getY(x)
    def getSlope(self, x):
        if x <= self.getIntersection()[0]:
            return self.equation0.m
        else:
            return self.equation1.m

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

initialXCallVar = DoubleVar()
initialYCallVar = DoubleVar()

peakXCallVar = DoubleVar()
peakYCallVar = DoubleVar()

endXCallVar = DoubleVar()
endYCallVar = DoubleVar()

##Begin Initial Slider Section

initialXSlider = slider(title="Initial Point X Slider", min=0, max=.9, default=0, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=0, column=4, callVar=initialXCallVar)
initialXSlider.makeSlider()

def initialXTrace(ver, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    AX = initialXCallVar.get()
    if 0 <= AX and AX < min(equation2.xi, equation2.xf):#NOTE Deliberate choice to use equation 2's peak x, should not affect math        
        equation1.setInitialPoint(x=AX, y=equation1.yi)
    else:
        print("Initial X Error: Slider out of range")

initialXCallVar.trace_add("write", initialXTrace) #Tying the trace to the variable so when the variable changes the equations are modified

initialYSlider = slider(title="Initial Point Y Slider", min=0, max=.9, default=0, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=0, column=5, callVar=initialYCallVar)
initialYSlider.makeSlider()

def initialYTrace(ver, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    AY = initialYCallVar.get()
    if 0 <= AY and AY < equation1.yf:#NOTE Deliberate choice to use equation 1's peak y, should not affect math
        equation1.setInitialPoint(x=equation1.xi, y=AY)
    else:
        print("Initial Y Error: Slider out of range")

initialYCallVar.trace_add("write", initialYTrace) #Tying the trace to the variable so when the variable changes the equations are modified

##End Initial Slider Section
##Begin Peak Slider Section

peakXSlider = slider(title="Peak X Slider", min=.1, max=.9, default=.5, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=1, column=4, callVar=peakXCallVar)
peakXSlider.makeSlider()

def peakXTrace(var, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    BX = peakXCallVar.get()
    if equation1.xi < BX and BX < equation2.xf:
        equation1.setFinalPoint(x=BX, y=equation1.yf)
        equation2.setInitialPoint(x=BX, y=equation2.yi)
    else:
        print("Peak X Error: Slider out of range")

peakXCallVar.trace_add("write", peakXTrace) #Tying the trace to the variable so when the variable changes the equations are modified

peakYSlider = slider(title="Peak Y Slider", min=.1, max=1, default=1, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=1, column=5, callVar=peakYCallVar)
peakYSlider.makeSlider()

def peakYTrace(var, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    BY = peakYCallVar.get()
    if max(equation1.yi, equation2.yf) < BY and BY <= 1:
        equation1.setFinalPoint(x=equation1.xf, y=BY)
        equation2.setInitialPoint(x=equation2.xi, y=BY)
    else:
        print("Peak Y Error: Slider out of range")

peakYCallVar.trace_add("write", peakYTrace) #Tying the trace to the variable so when the variable changes the equations are modified

##End Peak Slider Section
##Begin End Slider Section

endXSlider = slider(title="End Point X Slider", min=.1, max=1, default=1, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=2, column=4, callVar=endXCallVar)
endXSlider.makeSlider()

def endXTrace(var, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    CX = endXCallVar.get()
    if max(equation1.xi, equation1.xf) < CX and CX <= 1: #NOTE Deliberate choice to use equation 1's peak x, should not affect math
        equation2.setFinalPoint(x=CX, y=equation2.yf)
    else:
        print("End X Error: Slider out of range")

endXCallVar.trace_add("write", endXTrace) #Tying the trace to the variable so when the variable changes the equations are modified

endYSlider = slider(title="End Point Y Slider", min=0, max=.9, default=0, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=2, column=5, callVar=endYCallVar)
endYSlider.makeSlider()

def endYTrace(var, indx, mode): #Trace to handle testing for sensible input and if verified, modifying the equations
    CY = endYCallVar.get()
    if 0 <= CY and CY < equation2.yi: #NOTE Deliberate choice to use equation 2's peak y, should not affect math
        equation2.setFinalPoint(x=equation2.xf, y=CY)
    else:
        print("End Y Error: Slider out of range")

endYCallVar.trace_add("write", endYTrace) #Tying the trace to the variable so when the variable changes the equations are modified

##End End Slider Section
##End Peak Point Slider Section
##Begin x0 Slider Section

x0CallVar = DoubleVar()
x0Slider = slider(title="X0 Slider", min =0, max =1, default=.5, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=4, callVar=x0CallVar)
x0Slider.makeSlider()

##End x0 Slider Section
##Begin Precision Slider Section
def rangeTrunkOverride(precision):
    initialXSlider.setRange(min=0, max=(1-precision))
    initialYSlider.setRange(min=0, max=(1-precision))
    
    peakXSlider.setRange(min=precision, max=(1-precision))
    peakYSlider.setRange(min=precision, max=1)

    endXSlider.setRange(min=precision, max=1)
    endYSlider.setRange(min=0, max=(1-precision))

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    x0Slider.setPrecision(resolution=precision)

    initialXSlider.setPrecision(resolution=precision)
    initialYSlider.setPrecision(resolution=precision)

    peakXSlider.setPrecision(resolution=precision)
    peakYSlider.setPrecision(resolution=precision)

    endXSlider.setPrecision(resolution=precision)
    endYSlider.setPrecision(resolution=precision)

    rangeTrunkOverride(precision)

precisionCallVar.trace_add("write", precisionChange)#Tying the callback to the Variable

sliderPrecisionSlider = slider(title="Slider Precision", min=2, max=10, default=precisionDefault, fontStyle=fontStyle, precision=1, row=3, column=4, callVar=precisionCallVar)
sliderPrecisionSlider.makeSlider()
precisionCallVar.set(precisionDefault)

##End Slider Precision Slider Section
##Begin Font Slider Section

fontSlider = slider(title="Font Size", min=1, max=30, default=fontSizeDefault, fontStyle=fontStyle, precision=1, row=3, column=5, callVar=fontSizeCallVar)
fontSlider.makeSlider()

def fontChange(var, indx, mode):#Callback function for when fontSizeCallVar changes
    fontStyle.configure(size=fontSizeCallVar.get())
    initialXSlider.setFontStyle(fontStyle=fontStyle)
    initialYSlider.setFontStyle(fontStyle=fontStyle)
    peakXSlider.setFontStyle(fontStyle=fontStyle)
    peakYSlider.setFontStyle(fontStyle=fontStyle)
    endXSlider.setFontStyle(fontStyle=fontStyle)
    endYSlider.setFontStyle(fontStyle=fontStyle)
    fontSlider.setFontStyle(fontStyle=fontStyle)
    x0Slider.setFontStyle(fontStyle=fontStyle)
    sliderPrecisionSlider.setFontStyle(fontStyle=fontStyle)
    #eq1LabelTitle.setFontStyle(fontStyle=fontStyle)#FIXME
    #eq1Label.setFontStyle(fontStyle=fontStyle)#FIXME
    #eq2LabelTitle.setFontStyle(fontStyle=fontStyle)#FIXME
    #eq2Label.setFontStyle(fontStyle=fontStyle)#FIXME

fontSizeCallVar.trace_add("write", fontChange)#Tying the callback to the Variable

##End Font Slider Section
##End Slider Section
##Begin Lam Calculation Section

def calcLam(teq1, teq2, x0):
    x = x0
    sum = 0
    tempEquation = tentEquation(teq1, teq2)
    #print("e1: " + str(teq1.m) + " e2: " + str(teq2.m))
    initialLoopCount = 100
    postLoopCount = 100
    totalLoopCount = initialLoopCount + postLoopCount
    lam = 0
    #print("eq1: " + teq1.getString())
    #print("eq2: " + teq2.getString())
    for i in range(initialLoopCount):
        #print("I: " + str(i) + " X: " + str(x))
        x = tempEquation.getY(x)
    for _ in range(initialLoopCount, totalLoopCount):#TODO FIXME FIXME FIXME
        m = tempEquation.getSlope(x)
        f=np.log(np.abs(m))#TODO FIXME FIXME FIXME
        x = tempEquation.getY(x)
        #print(str(m), str(x))
        sum = sum + f
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
lamFrame.grid(row=4, column=0)

##End Lam Label
##Begin Equation Labels

eq1LabelCallVar = StringVar()
eq1LabelFrame = Frame(root)
eq1LabelTitle = Label(eq1LabelFrame, text="Equation 1:", font=fontStyle)
eq1LabelTitle.pack()
eq1Label = Label(eq1LabelFrame, textvariable=eq1LabelCallVar, font=fontStyle)
eq1Label.pack()
eq1LabelFrame.grid(row=4, column=1)

eq2LabelCallVar = StringVar()
eq2LabelFrame = Frame(root)
eq2LabelTitle = Label(eq2LabelFrame, text="Equation 2:", font=fontStyle)
eq2LabelTitle.pack()
eq2Label = Label(eq2LabelFrame, textvariable=eq2LabelCallVar, font=fontStyle)
eq2Label.pack()
eq2LabelFrame.grid(row=4, column=2)

##End Equation Labels
##Begin Plot Section

fig = plt.figure(dpi=figureDPI)
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
#fig.set_size_inches(4, 4)

def plotting(i):
    ax1.clear()
    ax1.plot([equation1.xi, equation1.xf], [equation1.yi, equation1.yf], linewidth=1) #first lines 
    ax1.plot([equation2.xi, equation2.xf], [equation2.yi, equation2.yf], linewidth=1) #second line
    ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    #ax1.set_xlim(0,1)
    #ax1.set_ylim(0,1.5)
    ax1.grid(True)
    lamCallVar.set(calcLam(teq1=equation1, teq2=equation2, x0=x0CallVar.get()))
    eq1LabelCallVar.set(equation1.getString())
    eq2LabelCallVar.set(equation2.getString())

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)
##End Plot Section

root.mainloop()