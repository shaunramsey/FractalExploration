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

def binCalc(numBins, equations):
    binList = []
    binSize = 1/numBins
    for i in range(numBins):
        binList.append(bin(start=(i*binSize), end=((i*binSize)+binSize)))   
    
    for i in range(numBins): #Loop to populate bins in binList with approperate contents
        yStart = equations.getY(i * binSize)
        yEnd = equations.getY((i+1) * binSize)
        contentTotal = 0
        for j in range(len(binList)):
            tempPercentage = binList[j].percentageOfRange(rangeStart = yStart, rangeEnd = yEnd)
            binList[j].addContent(tempPercentage)
            contentTotal = contentTotal + tempPercentage
            if contentTotal >= 1:
                break

    return binList
        
##End Bin Initialization Section
##End Bin Section

root = tkinter.Tk()
#root.geometry('1920x1080')
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
##Begin Slider In Frame Class

class sliderInFrame(slider):
    def __init__(self, root, title, min, max, default, fontStyle, precision, callVar):
        self.root = root
        self.title = title
        self.min = min
        self.max = max
        self.default = default
        self.fontStyle = fontStyle
        self.precision = precision
        self.callVar = callVar
        self.callVar.set(self.default)
    def makeSlider(self):
        self.frame = Frame(self.root)
        self.sliderLabel = Label(self.frame,text=self.title, font=self.fontStyle)
        self.sliderLabel.pack()
        self.entry = Entry(self.frame, textvariable=self.callVar, font=self.fontStyle)
        self.entry.pack()
        self.slider = Scale(self.frame, from_=self.min, to=self.max, orient=HORIZONTAL, variable=self.callVar, font=self.fontStyle, showvalue=0, length=200, resolution=self.precision)
        self.slider.pack()

    def pack(self):
        self.frame.pack()
    
    def packSide(self, side):
        self.frame.pack(side=side)

##End Slider In Frame Class
##Begin Precision Calculator Function

def calcPrecision(input):#Converts integer range of precision (2-10 on the slider) to the decimal place equivalent
    temp = "."
    for _ in range(input-2):
        temp = temp + "0"
    return float(temp + "1")

##End Precision Calculator Function
##Begin Initial Variable Sliders

iniVarFrame = Frame(root)

##Begin x0 Slider Section

x0CallVar = DoubleVar()
x0CallVar.set(.5)
x0Slider = sliderInFrame(root=iniVarFrame, title="x0 Slider", min=0, max=1, default=.5, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), callVar=x0CallVar)
x0Slider.makeSlider()
x0Slider.packSide(LEFT)

##End x0 Slider Section
##Begin r Slider Section

rCallVar = DoubleVar()
rCallVar.set(3)
rSlider = sliderInFrame(root=iniVarFrame, title="r Slider", min=0, max=4, default = 3, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), callVar=rCallVar)
rSlider.makeSlider()
rSlider.packSide(RIGHT)

##End r Slider Section

iniVarFrame.grid(row=1, column=4)

##End Initial Variable Sliders
##Begin Logistic Curve Point Count Section

numLogisticPointCallVar = IntVar()
numLogisticPointCallVar.set(5)

logisticOverrideOn= BooleanVar()
logisticOverrideOn.set(False)
logisticFrame = Frame(root, borderwidth=1, highlightbackground="black", highlightthickness=1)
logisticOverrideFrame = Frame(logisticFrame)

logisticOverrideButton = Checkbutton(logisticOverrideFrame, text="Override With Logistic Points", variable=logisticOverrideOn, font=fontStyle)
logisticOverrideButton.pack(side=LEFT)

numLogisticPointSlider = sliderInFrame(root=logisticOverrideFrame, title="Points On The Logistic Curve", min=3, max=50, default=5, fontStyle=fontStyle, precision=1, callVar=numLogisticPointCallVar)
numLogisticPointSlider.makeSlider()
numLogisticPointSlider.packSide(RIGHT)

logisticOverrideFrame.pack()

binNumCallVar = IntVar()
binNumSlider = sliderInFrame(root=logisticFrame, title="Number of Bins", min=1, max=50, default=2, fontStyle=fontStyle, precision=1, callVar=binNumCallVar)
binNumSlider.makeSlider()
binNumSlider.pack()

logisticFrame.grid(row=2, column=4)

##End Logistic Curve Point Count Section
##Begin Precision Slider Section

def precisionChange(var, indx, mode):#Callback function for when precisionCallVar changes
    precision = calcPrecision(precisionCallVar.get())
    x0Slider.setPrecision(resolution=precision)
    #pointAddXSlider.setPrecision(resolution=precision) #FIXME
    #pointAddYSlider.setPrecision(resolution=precision) #FIXME


precisionCallVar.trace_add("write", precisionChange)#Tying the callback to the Variable

sliderPrecisionSlider = slider(title="Slider Precision", min=2, max=10, default=precisionDefault, fontStyle=fontStyle, precision=1, row=3, column=4, callVar=precisionCallVar)
sliderPrecisionSlider.makeSlider()
precisionCallVar.set(precisionDefault)

##End Slider Precision Slider Section
##Begin Font Slider Section

fontSlider = slider(title="Font Size", min=1, max=30, default=fontSizeDefault, fontStyle=fontStyle, precision=1, row=4, column=4, callVar=fontSizeCallVar)
fontSlider.makeSlider()

def fontChange(var, indx, mode):#Callback function for when fontSizeCallVar changes
    fontStyle.configure(size=fontSizeCallVar.get())
    fontSlider.setFontStyle(fontStyle=fontStyle)
    x0Slider.setFontStyle(fontStyle=fontStyle)
    #pointAddXSlider.setFontStyle(fontStyle=fontStyle) #FIXME
    #pointAddYSlider.setFontStyle(fontStyle=fontStyle) #FIXME
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

            x0Temp = x0CallVar.get()
            if logisticOverrideOn.get() == False:
                x0Slider.setRange(min=self.getPointByIndex(0)[0], max=self.getPointByIndex(self.getLength()-1)[0])
                if self.isInRange(x0Temp) == False:
                    x0CallVar.set(self.getLastPoint()[0])
            else:
                x0Slider.setRange(min=0, max=1)
                if x0Temp < 0 or x0Temp > 1:
                    x0CallVar.set(.5)
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
            x0Temp = x0CallVar.get()
            x0Slider.setRange(min=self.getPointByIndex(0)[0], max=self.getPointByIndex(self.getLength()-1)[0])
            if self.isInRange(x0Temp) == False:
                x0CallVar.set(self.getLastPoint()[0])
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
        for p in self.getPointList():
            tempList.append(str(p))
        return tempList

    def getLastPoint(self):
        return self.getPointByIndex(self.getLength()-1)

    def isInRange(self, x):
        if x >= self.getPointByIndex(0)[0] and x <= self.getLastPoint()[0]:
            return True
        return False

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

        def getWidth(self):
            return (self.getFinalPoint()[0]-self.getInitialPoint()[0])
    
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
    
    def getEQByIndex(self, index):
        try:
            return self.equationList[index]
        except:
            print("Error: indext out of range")

##End Points and Equations Classes

points = pointRegister()
points.addPoint((0,0))
points.addPoint((.5,1))
points.addPoint((1,.25))

equations = equationRegister()
equations.buildEquations(points)

##End Points and Equations Section
##Begin Point Entry Section

pointFrame = Frame(root, borderwidth=1, highlightbackground="black", highlightthickness=1)

##Begin Point Selection And Deletion Section

pointDeleteFrame = Frame(pointFrame)

##Begin Point Dropdown

pointDropdownFrame = Frame(pointDeleteFrame)

pointSelectionCallVar = StringVar()
pointSelectionCallVar.set(str(points.getPointByIndex(0)))

pointSelectionLabel = Label(pointDropdownFrame, text="Select Point:", font=fontStyle)
pointSelectionLabel.pack()


pointSelectionDropDown = OptionMenu(pointDropdownFrame, pointSelectionCallVar, *points.getPointStringList()) #NOTE Ignore warning
pointSelectionDropDown.pack()

pointDropdownFrame.pack(side=LEFT)

##End Point Dropdown
##Begin Point Delete Button

def deletePoint():
    for i in range(points.getLength()):
        if pointSelectionCallVar.get() == str(points.getPointByIndex(i)):
            points.removePointByIndex(i)
            equations.buildEquations(points)
            pointSelectionDropDown["menu"].delete(i)
            pointSelectionCallVar.set(str(points.getPointByIndex(0)))
            break

deletePointButton = Button(pointDeleteFrame, text="Delete Selected Point", command=deletePoint)
deletePointButton.pack(side=RIGHT)

##End Point Delete Button

pointDeleteFrame.pack()

##End Point Selection And Deletion Section
##Begin Point Add Section

pointAddFrame = Frame(pointFrame)

pointAddTitle = Label(pointAddFrame,text="Add Point:", font=fontStyle)
pointAddTitle.pack()

pointAddXCallVar = DoubleVar()
pointAddXCallVar.set(0) #TODO Change to a variable default value

pointAddXSlider = sliderInFrame(root = pointAddFrame, title="X Value", min=0, max= 10, default=0, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), callVar=pointAddXCallVar)#FIXME What max?
pointAddXSlider.makeSlider()
pointAddXSlider.packSide(LEFT)

pointAddYCallVar = DoubleVar()
pointAddYCallVar.set(0) #TODO Change to a variable default value

pointAddYSlider = sliderInFrame(root = pointAddFrame, title="Y Value", min=0, max= 10, default=0, fontStyle=fontStyle, precision=calcPrecision(precisionDefault), callVar=pointAddYCallVar)#FIXME What max?
pointAddYSlider.makeSlider()
pointAddYSlider.packSide(RIGHT)

##Begin Point Add Button

def addPoint():
    newPoint = (pointAddXCallVar.get(), pointAddYCallVar.get())
    points.addPoint(newPoint)
    equations.buildEquations(points)
    pointSelectionCallVar.set(str(newPoint))
    pointSelectionDropDown["menu"].delete(0, "end")
    for p in points.getPointStringList():
        pointSelectionDropDown["menu"].add_command(label=str(p), command = lambda pStr= p: pointSelectionCallVar.set(pStr))
    pointSelectionCallVar.set(str(newPoint))

addPointButton = Button(pointAddFrame, text="Add Specified Point", command=addPoint)
addPointButton.pack()

##End Point Add Button

pointAddFrame.pack()

##End Point Add Section

pointFrame.grid(row=0, column=4)

##End Point Entry Section
##Begin Lam Calculation Section

def calcLam(x0, equations):
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
##Begin Plot Section
##Begin Plotting Initialization

fig = plt.figure(dpi=figureDPI)
ax1 = fig.add_subplot(111)
#plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
#fig.set_size_inches(3, 3)

##End Plotting Initialization
##Begin Cobweb Section

plotCobwebOn = BooleanVar()
plotCobwebOn.set(False)

plotCobwebButton = Checkbutton(root, text="Plot Cobweb", variable=plotCobwebOn, font=fontStyle)
plotCobwebButton.grid(row=4, column=1)

def plotCobweb(points, equations):
    cobwebIterations = 200
    #lineInitial = points.getPointByIndex(0)
    #lineFinal = points.getLastPoint()
    #ax1.plot([lineInitial[0],lineFinal[0]],[lineInitial[1],lineFinal[0]], linewidth=.7) #plot y=x line
    x0 = x0CallVar.get()
    a = x0
    c = equations.getY(a)
    ax1.plot([x0, x0], [0, c], linewidth=.5, color='black') #first lines 
    ax1.plot([x0, c], [c, c], linewidth=.5, color='black')#second line
    for _ in range(cobwebIterations):#loop that makes the rest of the cobweb lines
        a = c
        c = equations.getY(a)
        ax1.plot([a, a], [a, c], linewidth=.5, color='black')
        ax1.plot([a, c], [c, c], linewidth=.5, color='black')

##End Cobweb Section
##Begin Logistic Section

def calcLamLogistic(equations):
    numBins = binNumCallVar.get()
    bins = binCalc(numBins, equations)

    weightList = []

    l1width = equations.getEQByIndex(0).getLength()
    l2width = equations.getEQByIndex(1).getLength()

    l2ix = equations.getEQByIndex(1).getInitialPoint()[0] #.5
    l2fx = equations.getEQByIndex(1).getFinalPoint()[0] #1
    
    #temp = 1/((((fx - equations.getEQByIndex(1).getX(ix))/ix) /ix)+ix)
    temp = (((fx - equations.getEQByIndex(1).getX(ix))/ix)/ix)
    print("temp " + str(temp))

    for i in range(equations.getLength()):
        #tempWeight = 0
        tempWeight = i #FIXME put in the weight calculations for each one
        #TODO magic with weights
        weightList.append(tempWeight)

    tempLambda = 0

    for i in range(equations.getLength()):
        tempLambda = tempLambda + (equations.getEQByIndex(i).getWidth() * weightList[i] * np.log(np.abs(equations.getEQByIndex(i).getM())))

    return tempLambda


def calcLogistic(r, x):
    return abs(r*x*(1-x))

def iniLogisticPoints(numPoints, r):
    tempPoints = pointRegister()
    space = (1/(numPoints-1))
    for i in range(numPoints):
        x = (space * i)
        y = calcLogistic(r, x)
        #print((x,y))
        tempPoints.addPoint((x, y))
    return tempPoints

##Begin Logistic Plotting Section

def plotLogistic():
    r = rCallVar.get()
    numPoints = numLogisticPointCallVar.get()
    #numPoints = 5
    xs = np.arange(0,1,.001) #x for parabala plot
    ys =(r * xs * (1-xs)) #y for parabala plot
    ax1.plot(xs, ys, linewidth=.7) #parabala plot

    logisticPoints = iniLogisticPoints(numPoints, r)
    logisticEquations = equationRegister()
    logisticEquations.buildEquations(logisticPoints)
    
    for i in range(numPoints-1):
        #print(i)
        initial = logisticPoints.getPointByIndex(i)
        final = logisticPoints.getPointByIndex(i+1)
        #print((initial[0], final[0]), (initial[1], final[1]))
        ax1.plot([initial[0], final[0]], [initial[1], final[1]])
    if plotCobwebOn.get() == True:
            plotCobweb(logisticPoints, logisticEquations)
    lamCallVar.set(calcLamLogistic(equations=equations))

##End Logistic Plotting Section
##End Logistic Section


def plotting(i):
    ax1.clear()
    if logisticOverrideOn.get() == False:
        ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
        equations.buildEquations(points)
        for i in range(equations.getLength()):
            line = equations.getPointsByIndex(i)
            ax1.plot([line[0][0], line[1][0]],[line[0][1], line[1][1]], linewidth=1)
        lamCallVar.set(calcLam(x0=x0CallVar.get(), equations=equations))
        print(calcLamLogistic(equations=equations))
        if plotCobwebOn.get() == True:
            plotCobweb(points, equations)
        
    else:
        ax1.set_title("Logistic Equation Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
        plotLogistic()

    ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=500)
##End Plot Section

root.mainloop()