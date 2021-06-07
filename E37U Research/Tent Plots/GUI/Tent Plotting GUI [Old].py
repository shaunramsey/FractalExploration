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

aSliderDefault = 1
bSliderDefault = .5
sliderPrecision = .1 #Universal Slider Precision's default value on program startup
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

#def binIni(binSize):
    #for i in range(binSize):
        #TODO

##End Bin Initialization Section

root = tkinter.Tk()
root.title('Tent Plotting GUI')
def on_closing():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)

##Begin Font Section

fontStyle = tkFont.Font(family="Times New Roman", size=fontSizeDefault)

##End Font Section
##Begin Universal Variables Section

aCallVar = DoubleVar()
bCallVar = DoubleVar()
precisionCallVar = IntVar()
fontSizeCallVar = IntVar()

##End Universal Variables Section
##Begin Slider Section
##Begin a Slider Section

a_frame = Frame(root)
aSlider_label = Label(a_frame,text="a", font=fontStyle)
aSlider_label.pack()
aEntry = Entry(a_frame, textvariable=aCallVar, font=fontStyle)
aEntry.pack()
aSlider = Scale(a_frame, from_=0, to=1,orient=HORIZONTAL, variable=aCallVar, font=fontStyle, showvalue=0, length=200, resolution=sliderPrecision)
aCallVar.set(aSliderDefault)
aSlider.pack()
a_frame.grid(row=4, column=0)

##End a Slider Section
##Begin b Slider Section

b_frame = Frame(root)
bSlider_label = Label(b_frame,text="b", font=fontStyle)
bSlider_label.pack()
bEntry = Entry(b_frame, textvariable=bCallVar, font=fontStyle)
bEntry.pack()
bSlider = Scale(b_frame, from_=0, to=1, orient=HORIZONTAL, variable=bCallVar, font=fontStyle, showvalue=0, length=200, resolution=sliderPrecision)
bCallVar.set(bSliderDefault)
bSlider.pack()
b_frame.grid(row=4, column=1)

##End b Slider Section
##Begin Slider Precision Slider Section

def setSliderPrecision(var):
    if sliderPrecisionSlider.get() == 1:
        sliderPrecision = 1 #TODO fix scope issue
    else:
        tempPrecision = "."
        for _ in range((sliderPrecisionSlider.get()-2)):
            tempPrecision = tempPrecision + "0"
        sliderPrecision = float(tempPrecision + "1") #TODO fix scope issue
    aSlider.configure(resolution=sliderPrecision)
    bSlider.configure(resolution=sliderPrecision)
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
    aSlider.configure(font=fontStyle)
    bSlider.configure(font=fontStyle)
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