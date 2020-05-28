import tkinter as tk

def __init__(self):
    self.root = tk.Tk()
    self._job = None
    self.slider = tk.Scale(self.root, from_=0, to=256, 
                            orient="horizontal", 
                            command=self.updateValue)
    self.slider.pack()
    self.root.mainloop()

def updateValue(self, event):
    if self._job:
        self.root.after_cancel(self._job)
    self._job = self.root.after(500, self._do_something)

def _do_something(self):
    self._job = None
    print ("new value:", self.slider.get())
