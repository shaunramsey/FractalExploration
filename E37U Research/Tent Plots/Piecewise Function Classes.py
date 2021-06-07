import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation
import math
from random import *


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
        else:
            print("Error, duplicate point") #TODO make this an error on the GUI
    
    def removePoint(self, point):
        try:
            self.pointList.remove(point)
            self.listSort
        except:
            print("Error, point not found") #TODO make this an error on the GUI
    
    def getLength(self):
        return len(self.pointList)
    
    def getPointByIndex(self, index):
        return self.pointList[index]

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
        if x >= equation.getInitialPoint[0] and x <= equation.getFinalPoint[0]:
            return True
        return False

    def getY(self,x):
        for i in range(self.getLength()):
            if self.isXInEQRange(x, self.equationList[i]) == True:
                return self.equationList[i].getY(x)
        print("Error: X not in Register Range") #NOTE This should only call if the if statement is never true inside the previous for loop
    
    def getLength(self):
        return len(self.equationList)

#def pointWindow():
#    precition
#    popup = tkinter.Tk()
#    popup.title('Add Point')
#    tempXCallVar = DoubleVar()
#    xEntry = Entry(popup, textvariable=tempXCallVar, font=fontStyle)
#    xSlider = Scale(popup, from_=0, to=10, orient=HORIZONTAL, variable=tempXCallVar, font=fontStyle, showvalue=0, length=200, resolution=precision)


points = pointRegister()
points.addPoint((0,1))
points.addPoint((7,2))
points.addPoint((3,2))
points.addPoint((4,5))
points.addPoint((1,6))
points.addPoint((1,6))
#for i in range(points.getLength()):
#    print(str(points.pointList[i]))

equations = equationRegister()
equations.buildEquations(points)

#for i in range(equations.getLength()):
#    print(equations.getEQStringByIndex(i))


root = tkinter.Tk()
root.title('Tent Plotting GUI')
def on_closing():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.subplots_adjust(wspace=.5, hspace=.5)#Specifies the space between plots
fig.set_size_inches(4, 4)


seed(1)
def plotting(i):
    equations.buildEquations(points)
    ax1.clear()
    for i in range(equations.getLength()):
        line = equations.getPointsByIndex(i)
        ax1.plot([line[0][0], line[1][0]],[line[0][1], line[1][1]], linewidth=1)
    #ax1.set_title("Tent Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    #ax1.set_xlabel("X Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    #ax1.set_ylabel("Y Values", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    #ax1.set_xlim(0,1)
    #ax1.set_ylim(0,1.5)
    ax1.grid(True)
    #lamCallVar.set(calcLam(teq1=equation1, teq2=equation2, x0=x0CallVar.get()))
    points.addPoint((randint(0,100), randint(0,100)))
    points.addPoint((random(), random()))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)
ani = animation.FuncAnimation(fig, plotting, interval=100)
##End Plot Section

root.mainloop()