import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation



##Begin Default Values

x0SliderDefault = .5 #Slider for Initial x's default value on program startup
rSliderDefault = 3.3 #Slider for r's default value on program startup
sliderPrecision = .1 #Universal Slider Precision's default value on program startup
figureDPI = 50 #DPI value for main figure
numIterations = 100 #Number of iterations in the iteration plot
cobwebStrands = 100 #Number of individual cob web lines to be drawn
fontSizeDefault = 20 #Default font size

##End Default Values


root = tkinter.Tk()
root.title('Plotting GUI')
#root.geometry("2000x1125")
def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

##Begin Font Section

fontStyle = tkFont.Font(family="Times New Roman", size=fontSizeDefault)

##End Font Section

##Begin EXPEREMENTAL Trace Section (1/2)

rCallVar = DoubleVar()
x0CallVar = DoubleVar()
precisionCallVar = IntVar()
fontSizeCallVar = IntVar()

##End EXPEREMENTAL Trace Section (1/2)


##Begin Slider Section
#
#def submitSlider(var): #Note: "var" is needed to overcome an anomaly with scale commands
#    plotting(getRSlider(), getx0Slider(), figureDPI, numIterations, cobwebStrands)
#    x0_sizelabel_var.set(x0Slider.get())
#    r_sizelabel_var.set(rSlider.get())
#    rSliderValue_var.set(rSlider.get())
#
##Begin r Slider Section  
#
#def getRSlider(): #Function that returns r from the slider
#    return rSlider.get()

#def rEntryPause(input): #attempts to use validate to force the entry to use the most recent version of an entry (1/2)
#    time.sleep(1)
#    if input == rEntry.get():
#        return TRUE
#    else:
#        FALSE


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
r_frame.grid(row=1, column=0)

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
#x0Slider.set(x0SliderDefault)
x0CallVar.set(x0SliderDefault)
x0Slider.pack()
x0_frame.grid(row=1, column=1)


##End x0 Slider Section

##Begin Slider Precision Slider Section

def setSliderPrecision(var):
    if sliderPrecisionSlider.get() == 1:
        sliderPrecision = 1 #TODO fix scope issue
        
    else:
        tempPrecision = "."
        for i in range((sliderPrecisionSlider.get()-2)):
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
sliderPrecision_frame.grid(row=1, column=2)


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
fontsize_frame.grid(row=2, column=0)

##End Font Slider Selection


##End Slider Section

fig = plt.figure()
ax1 = fig.add_subplot(111)

def plotting(i):
    #print("r: " + str(r)) #NOTE for Testing
    ax1.clear()
    r= rCallVar.get()
    x0 = x0CallVar.get()

    #Begin Cobweb Plot Section
    ax1.plot([0,1],[0,1]) #plot y=x line (TODO make to fill the maximum bounds of the other plots not just 0-1)
    xs = np.arange(0,1,.001) #x for parabala plot
    ys =(r * xs * (1-xs)) #y for parabala plot
    ax1.plot(xs, ys) #parabala plot
    tempX = x0
    tempY = r * tempX * (-1*tempX + 1)
    ax1.plot([tempX, tempX], [0, tempY]) #first lines 
    ax1.plot([tempY, tempX], [tempY, tempY])#second line
    for i in range(cobwebStrands):#loop that makes the rest of the cobweb lines
        tempY = r * tempX * (-1*tempX + 1)
        ax1.plot([tempX, tempX], [tempX, tempY])
        ax1.plot([tempY, tempX], [tempY, tempY])
        tempX=tempY
    plt.title("Cobweb Plot")
    plt.xlabel("X_n Values")
    plt.ylabel("X_n+1 Values")
    #End Cobweb Plot Section
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0)

ani = animation.FuncAnimation(fig, plotting, interval=1000)
#canvas = FigureCanvasTkAgg(ani, master=root)
#canvas.get_tk_widget().grid(columnspan=3, row=0, column=0)


##Begin Experemental Trace Section (2/2)

#def valueChange(var, indx, mode):#function to handle a change in one of the GUI inputs
#    if rCallVar.get() != rSlider.get():
#        rSlider.set(rCallVar.get())
#    if x0CallVar.get() != x0Slider.get():
#        x0Slider.set(x0CallVar.get())
#    #sliderPrecisionSlider.set(precisionCallVar.get())
#    #fontSlider.set(fontSizeCallVar.get())
#    time.sleep(1)
#    plotting(rCallVar.get(), x0CallVar.get(), figureDPI, numIterations, cobwebStrands)
 
#rCallVar.trace_add("write", valueChange)
#x0CallVar.trace_add("write", valueChange)

##End Experemental Trace Section (2/2)

#submitSlider(0) #First plot which is a placeholder until the r slider is used to select the desired r
#valueChange()
#plotting(rCallVar.get(), x0CallVar.get(), figureDPI, numIterations, cobwebStrands)

root.mainloop()