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

x0SliderDefault = .5 #Slider for Initial x's default value on program startup
rSliderDefault = 3.3 #Slider for r's default value on program startup
sliderPrecision = .1 #Universal Slider Precision's default value on program startup
figureDPI = 50 #DPI value for main figure
fontSizeDefault = 20 #Default font size

##End Default Values


root = tkinter.Tk()
root.title('Lyapunov GUI')
#root.geometry("2000x1125")
def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

##Begin Font Section

fontStyle = tkFont.Font(family="Times New Roman", size=fontSizeDefault)

##End Font Section

##Begin Universal Variables Section

rCallVar = DoubleVar()
precisionCallVar = IntVar()
fontSizeCallVar = IntVar()

##End Universal Variables Section


##Begin Universal Variables Section

rCallVar = DoubleVar()
x0CallVar = DoubleVar()
precisionCallVar = IntVar()
fontSizeCallVar = IntVar()

##End Universal Variables Section


##Begin Slider Section

r_sizelabel_var = DoubleVar()
r_frame = Frame(root)
rSlider_label = Label(r_frame,text="R_A", font=fontStyle)
rSlider_label.pack()
#rEntry = Entry(r_frame, textvariable=rCallVar, font=fontStyle, validate="focusout", validatecommand=rEntryPause(self.get())) #attempts to use validate to force the entry to use the most recent version of an entry (2/2)
rEntry = Entry(r_frame, textvariable=rCallVar, font=fontStyle)
rEntry.pack()
#rSlider_sizelabel = Label(r_frame, textvariable=r_sizelabel_var, font=fontStyle)
#rSlider_sizelabel.pack()
rSlider = Scale(r_frame, from_=0, to=4,orient=HORIZONTAL, variable=rCallVar, font=fontStyle, showvalue=0, length=200, resolution=sliderPrecision)
rCallVar.set(rSliderDefault)
rSlider.pack()
r_frame.grid(row=4, column=0)

##End r Slider Section

##Begin x0 Slider Section

def getx0Slider(): #Function that returns x0 from the slider
    return x0Slider.get()

x0_sizelabel_var = DoubleVar()
x0_frame = Frame(root)
x0Slider_label = Label(x0_frame,text="Initial X Value", font=fontStyle)
x0Slider_label.pack()
x0Entry = Entry(x0_frame, textvariable=x0CallVar, font=fontStyle)
x0Entry.pack()
#x0Slider_sizelabel = Label(x0_frame, textvariable=x0_sizelabel_var, font=fontStyle)
#x0Slider_sizelabel.pack()
x0Slider = Scale(x0_frame, from_=0, to=1,orient=HORIZONTAL, variable=x0CallVar, font=fontStyle, showvalue=0, length=200, resolution=sliderPrecision)
x0CallVar.set(x0SliderDefault)
x0Slider.pack()
x0_frame.grid(row=4, column=1)


##End x0 Slider Section

##Begin Slider Precision Slider Section

def setSliderPrecision(var):
    if sliderPrecisionSlider.get() == 1:
        sliderPrecision = 1 #TODO fix scope issue
        
    else:
        tempPrecision = "."
        for _ in range((sliderPrecisionSlider.get()-2)):
            tempPrecision = tempPrecision + "0"
        sliderPrecision = float(tempPrecision + "1") #TODO fix scope issue
    rSlider.configure(resolution=sliderPrecision)
    x0Slider.configure(resolution=sliderPrecision)
    sliderPrecision_sizelabel_var.set(sliderPrecisionSlider.get())


sliderPrecision_sizelabel_var = IntVar()
sliderPrecision_frame = Frame(root)
sliderPrecisionSlider_label = Label(sliderPrecision_frame,text="Slider Precision", font=fontStyle)
sliderPrecisionSlider_label.pack()
sliderPrecisionSlider_sizelabel = Label(sliderPrecision_frame, textvariable=sliderPrecision_sizelabel_var, font=fontStyle)
sliderPrecisionSlider_sizelabel.pack()
sliderPrecisionSlider = Scale(sliderPrecision_frame, from_=1, to=10,orient=HORIZONTAL, command=setSliderPrecision, font=fontStyle, showvalue=0, length=200)
sliderPrecisionSlider.set(2)
sliderPrecisionSlider.pack()
sliderPrecision_frame.grid(row=4, column=2)


##End Slider Precision Slider Section

##Begin Font Slider Section

def setFontSize(var):
    fontStyle.configure(size=fontSlider.get())
    rSlider.configure(font=fontStyle)
    x0Slider.configure(font=fontStyle)
    fontSlider.configure(font=fontStyle)
    sliderPrecisionSlider.configure(font=fontStyle)
    fontsize_sizelabel_var.set(fontSlider.get())


fontsize_sizelabel_var = IntVar()
fontsize_frame = Frame(root)
fontSlider_label = Label(fontsize_frame,text="Font Size", font=fontStyle)
fontSlider_label.pack()
fontSlider_sizelabel = Label(fontsize_frame, textvariable=fontsize_sizelabel_var, font=fontStyle)
fontSlider_sizelabel.pack()
fontSlider = Scale(fontsize_frame, from_=1, to=30,orient=HORIZONTAL, command=setFontSize, font=fontStyle, showvalue=0, length=200)
fontSlider.set(fontSizeDefault)
fontSlider.pack()
fontsize_frame.grid(row=4, column=3)

##End Font Slider Selection

##End Slider Section

fig = plt.figure()
ax1 = fig.add_subplot(111)
fig.set_size_inches(10, 4)


def plotting(i):
    rBPrecision = 1000

    ax1.clear()
    rBList = np.linspace(2, 4, rBPrecision)
    lamList= []
    for i in range(len(rBList)):
        #print(rBList[i])
        temp = calcLam(rBList[i])
        if temp < -.5:
            lamList.append(-.5)
        else:
            lamList.append(temp)
    ax1.plot(rBList,lamList, linewidth=.5)
    ax1.plot([2,4], [0,0])
    ax1.set_ybound(lower=-.6, upper=1)
    ax1.set_title("R_B/Lambda Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("R_B", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Lambda", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=8, rowspan=4)

ani = animation.FuncAnimation(fig, plotting, interval=1000)

##Begin lyapunov Section

def calcLam(rBIn):
    x = x0CallVar.get()
    rA = rCallVar.get()
    rB = rBIn
    sum = 0
    initialLoopCount = 50
    postLoopCount = 50
    lam = 0
    abList = []
    for i in range((initialLoopCount + postLoopCount)):
        if (i % 2) == 0:
            abList.append(rB)
            #print("i: " + str(i) + " r= " + str(rB))
        else:
            abList.append(rA)
            #print("i: " + str(i) + " r= " + str(rA))
    for i in range(initialLoopCount):
        x = abList[i] * x * (-1*x + 1)
        #print("x: " + str(x))

    for i in range(initialLoopCount, (initialLoopCount + postLoopCount)):
        x = abList[i] * x * (-1*x + 1)
        f=abs(abList[i] * (-2*x +1 ))
        #print("f: "+ str(f))
        if f < 0.0000000001:
            return -1000000 #temporary representative of negative infinity
        else:
            sum = sum + (math.log(f))
            #print("else")
    lam = sum / postLoopCount
    #print("lam: "+ str(lam))
    #print("sum: "+ str(sum))
    return lam

#lamCallVar = DoubleVar()
#lamCallVar.set(calcLam())
#lamFrame = Frame(root)
#lamLabelTitle = Label(lamFrame, text="Lyapunov Exponent:", font=fontStyle)
#lamLabelTitle.pack()
#lamLabel = Label(lamFrame, textvariable=lamCallVar, font=fontStyle)
#lamLabel.pack()
#lamFrame.grid(row=5, column=0)

#End lyapunov Section

root.mainloop()