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
#aCallVar = DoubleVar()
fontStyle = tkFont.Font(family="Times New Roman", size=20)
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
        self.slider.configure(min=min)
        self.slider.configure(max=max)

ageCallVar = DoubleVar()
newSlider = slider(title="age", min=0, max=100, default=20, fontStyle=fontStyle, precision=.1, row=0, column=0, callVar=ageCallVar)
newSlider.makeSlider()
heightCallVar = DoubleVar()
newSlider1 = slider(title="height", min=0, max=50, default=25, fontStyle=fontStyle, precision=.1, row=0, column=1, callVar=heightCallVar)
newSlider1.makeSlider()
ageLabel = Label(textvariable=ageCallVar)
ageLabel.grid(row=1, column=0)
    



##Begin a Slider Section



##End a Slider Section
root.mainloop()