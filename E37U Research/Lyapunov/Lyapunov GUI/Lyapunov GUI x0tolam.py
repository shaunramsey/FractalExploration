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


##Begin Slider Section

r_sizelabel_var = DoubleVar()
r_frame = Frame(root)
rSlider_label = Label(r_frame,text="R", font=fontStyle)
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
sliderPrecision_frame.grid(row=4, column=1)


##End Slider Precision Slider Section

##Begin Font Slider Section

def setFontSize(var):
    fontStyle.configure(size=fontSlider.get())
    rSlider.configure(font=fontStyle)
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
fontsize_frame.grid(row=4, column=2)

##End Font Slider Selection

##End Slider Section

fig = plt.figure()
ax1 = fig.add_subplot(121)
fig.set_size_inches(10, 4)

def plotting(i):
    ax1.clear()
    xList = np.arange(0,1, .001)
    yList= []
    for i in range(len(xList)):
        yList.append(calcLam(xList[i]))
    ax1.plot(xList,yList)
    ax1.set_title("Cobweb Plot", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-8))
    ax1.set_xlabel("Initial X", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))
    ax1.set_ylabel("Lambda", fontname=fontStyle.actual("family"), fontsize=(fontStyle.actual("size")-10))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=4)

ani = animation.FuncAnimation(fig, plotting, interval=1000)

##Begin lyapunov Section

def calcLam(inx):
    x = inx
    r = rCallVar.get()
    sum = 0
    n = 50
    lam = 0
    for _ in range(100):
        x = r * x * (-1*x + 1)

    for _ in range(n):
        x = r * x * (-1*x + 1)
        f=abs(r * (-2*x +1 ))
        if f < 0.0000000001:
            return -1000000 #temporary representative of negative infinity
        else:
            sum= sum + (math.log(f))
    lam = sum / n
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