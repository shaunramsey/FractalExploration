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
##Begin x0 Slider Section

x0CallVar = DoubleVar()
x0Slider = slider(title="X0 Slider", min=0, max=1, default=.5, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), row=4, column=4, callVar=x0CallVar)
x0Slider.makeSlider()

##End x0 Slider Section
##Begin Precision Slider Section

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    x0Slider.setPrecision(resolution=precision)


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
    fontSlider.setFontStyle(fontStyle=fontStyle)
    x0Slider.setFontStyle(fontStyle=fontStyle)
    sliderPrecisionSlider.setFontStyle(fontStyle=fontStyle)

fontSizeCallVar.trace_add("write", fontChange)#Tying the callback to the Variable

##End Font Slider Section
##End Slider Section
##Begin Points and Equations Section
##Begin Points and Equations Classes

class pointRegister:
    def __init__(self):
        self.pointList = []
    
    def listSort(self):
        self.pointList.sort(key = lambda point: point[0])

    def duplicateCheck(self, point):
        for i in range(len(self.pointList)):
            if point[0] == self.pointList[i][0]:
                return True
        return False
        
    
    def addPoint(self, point):
        if self.duplicateCheck(point) == False:
            self.pointList.append(point)
            self.listSort()
            x0Slider.setRange(min=self.getPointByIndex(0)[0], max=self.getPointByIndex(self.getLength()-1)[0])
            x0CallVar.set(self.getPointByIndex(0)[0])
        else:
            print("Error, duplicate point") #TODO make this an error on the GUI
    
    def removePoint(self, point):
        try:
            self.pointList.remove(point)
            self.listSort
            x0Slider.setRange(min=self.getPointByIndex(0)[0], max=self.getPointByIndex(self.getLength()-1)[0])
            x0CallVar.set(self.getPointByIndex(0)[0])
        except:
            print("Error, index out of range") #TODO make this an error on the GUI

    def removePointByIndex(self, index):
        try:
            del self.pointList[index]
            self.listSort
            x0Slider.setRange(min=self.getPointByIndex(0)[0], max=self.getPointByIndex(self.getLength()-1)[0])
            x0CallVar.set(self.getPointByIndex(0)[0])
        except:
            print("Error, point not found") #TODO make this an error on the GUI
    
    def getLength(self):
        return len(self.pointList)
    
    def getPointByIndex(self, index):
        return self.pointList[index]

    def getPointList(self):
        return self.pointList

    def getPointStringList(self):
        tempList = []
        for _ in range(self.getLength):
            tempList.append()
        return self.pointList

class equationRegister:
    def __init__(self):
        self.equationList = []
    
    class equation:
        def __init__(self, initialPoint, finalPoint):
            self.initialPoint = initialPoint
            self.finalPoint = finalPoint

            self.m = 0
            self.b = 0

            self.calcEQ()
        
        def calcEQ(self):
            self.m = ((self.finalPoint[1] - self.initialPoint[1])/(self.finalPoint[0] - self.initialPoint[0]))
            self.b = (self.initialPoint[1] - self.m * self.initialPoint[0])

        def getString(self):
            if self.m == 0:
                return "y=" + str(self.b)
            if self.b > 0:
                return "y=" + "{0:.2f}".format(self.m) + "x+" + "{0:.2f}".format(self.b)
            elif self.b < 0:
                return "y=" + "{0:.2f}".format(self.m) + "x" + "{0:.2f}".format(self.b)
            else:
                return "y=" + "{0:.2f}".format(self.m) + "x"
        
        def getM(self):
            return self.m

        def getB(self):
            return self.b
        
        def getX(self, y):
            return((y-self.b)/self.m)

        def getY(self, x):
            return((x * self.m)+self.b)
        
        def getInitialPoint(self):
            return self.initialPoint

        def getFinalPoint(self):
            return self.finalPoint
    
    def listSort(self):
        self.equationList.sort(key = lambda equation: equation.initialPoint[0])
    
    def addEquation(self, initialPoint, finalPoint):
        tempEQ = self.equation(initialPoint, finalPoint)
        self.equationList.append(tempEQ)
        self.listSort()

    def buildEquations(self, pointRegister):
        self.equationList = []
        for i in range(pointRegister.getLength()-1):
            self.addEquation(pointRegister.getPointByIndex(i), pointRegister.getPointByIndex(i+1))
    
    def getEQStringByIndex(self, index):
        return self.equationList[index].getString()

    def getPointsByIndex(self, index):
        return self.equationList[index].getInitialPoint(), self.equationList[index].getFinalPoint()
    

    def isXInEQRange(self, x, equation):
        if x >= equation.getInitialPoint()[0] and x <= equation.getFinalPoint()[0]:
            return True
        return False

    def getY(self,x):
        if x is None:
            print("hey!")
        for i in range(self.getLength()):
            if self.isXInEQRange(x, self.equationList[i]) == True:
                return self.equationList[i].getY(x)
        print("Error: X not in Register Range") #NOTE This should only call if the if statement is never true inside the previous for loop
    
    def getSlope(self,x):
        for i in range(self.getLength()):
            if self.isXInEQRange(x, self.equationList[i]) == True:
                return self.equationList[i].getM()
        print("Error: X not in RRegister Range") #NOTE This should only call if the if statement is never true inside the previous for loop

    def getLength(self):
        return len(self.equationList)

##End Points and Equations Classes

points = pointRegister()
points.addPoint((0,0))
points.addPoint((.5,1))
points.addPoint((1,0))
points.addPoint((2,3))
points.addPoint((5,0))

equations = equationRegister()
equations.buildEquations(points)

##End Points and Equations Section
##Begin Point Entry Section

pointEntryFrame = Frame(root)

##Begin Point Dropdown

pointEntryDropdownFrame = Frame(pointEntryFrame)

pointSelectionCallVar = StringVar() ##TODO Maybe theres a way to modify the definition to work with tuples
pointSelectionCallVar.set(str(points.getPointByIndex(0)))

pointEntryDropdownLabel = Label(pointEntryDropdownFrame, text="Select Point:", font=fontStyle)
pointEntryDropdownLabel.pack()

pointDropDown = OptionMenu(pointEntryDropdownFrame, pointSelectionCallVar, *points.getPointList()) #NOTE Ignore warning
pointDropDown.pack()

pointEntryDropdownFrame.pack()

##End Point Dropdown

def deletePoint():
    for i in range(points.getLength()):
        if pointSelectionCallVar.get() == str(points.getPointByIndex(i)):
            points.removePointByIndex(i)
            equations.buildEquations(points)
            pointDropDown["menu"].delete(i)
            pointSelectionCallVar.set(points.getPointByIndex(0))
            #pointDropDown.configure(value=)
            break

deletePointButton = Button(pointEntryFrame, text="Delete Selected Point", command=deletePoint)
deletePointButton.pack()

pointEntryFrame.grid(row=0, column=4)

##End Point Entry Section
##Begin Lam Calculation Section

def calcLam(x0):
    x = x0
    sum = 0
    initialLoopCount = 100
    postLoopCount = 100
    totalLoopCount = initialLoopCount + postLoopCount
    lam = 0
    #print("eq1: " + teq1.getString())
    #print("eq2: " + teq2.getString())
    for _ in range(initialLoopCount):
        #print("I: " + str(i) + " X: " + str(x))
        x = equations.getY(x)
    for _ in range(initialLoopCount, totalLoopCount):
        m = equations.getSlope(x)
        f=np.log(np.abs(m))
        x = equations.getY(x)
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

#eq1LabelCallVar = StringVar()
#eq1LabelFrame = Frame(root)
#q1LabelTitle = Label(eq1LabelFrame, text="Equation 1:", font=fontStyle)
#eq1LabelTitle.pack()
#eq1Label = Label(eq1LabelFrame, textvariable=eq1LabelCallVar, font=fontStyle)
#eq1Label.pack()
#eq1LabelFrame.grid(row=4, column=1)

##End Equation Labels
##Begin Plot Section

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
fig.set_size_inches(4, 4)

def plotting(i):
    equations.buildEquations(points)
    ax1.clear()
    for i in range(equations.getLength()):
        line = equations.getPointsByIndex(i)
        ax1.plot([line[0][0], line[1][0]],[line[0][1], line[1][1]], linewidth=1)
    ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    #ax1.set_xlim(0,1)
    #ax1.set_ylim(0,1.5)
    ax1.grid(True)
    lamCallVar.set(calcLam(x0=x0CallVar.get()))
    #eq1LabelCallVar.set(equation1.getString())

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)
##End Plot Section

root.mainloop()