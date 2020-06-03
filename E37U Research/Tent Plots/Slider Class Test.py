import tkinter
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import matplotlib.animation as animation
import math

aSliderDefault = 1
root = tkinter.Tk()
aCallVar = DoubleVar()
fontStyle = tkFont.Font(family="Times New Roman", size=20)
class slider:
    callVar = DoubleVar()
    def __init__(self, title, min, max, default, row, column):
        self.title = title
        self.min = min
        self.max = max
        self.default = default
        self.row = row
        self.column = column
        self.callVar.set(default)
    def makeSlider(self):
        self.frame = Frame(root)
        self.sliderLabel = Label(self.frame,text=self.title, font=fontStyle)
        self.sliderLabel.pack()
        self.entry = Entry(self.frame, textvariable=self.callVar, font=fontStyle)
        self.entry.pack()
        self.slider = Scale(self.frame, from_=self.min, to=self.max,orient=HORIZONTAL, variable=self.callVar, font=fontStyle, showvalue=0, length=200, resolution=.1)#TODO Adapt resolution 
        self.slider.pack()
        self.frame.grid(row=self.row, column=self.column)

newSlider = slider("age", 0,0)
newSlider.makeSlider()
newSlider1 = slider(0,1)
newSlider1.makeSlider()
    



##Begin a Slider Section



##End a Slider Section
root.mainloop()