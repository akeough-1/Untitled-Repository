import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Beam():
    def __init__(self, xlength:float):
        self.xlength = xlength
        self.ymax = xlength/2

class Displayable():
    def __init__(self, beam:Beam, number:int, xlocation:float):
        self.beam = beam
        self.number = number
        self.xlocation = xlocation

class Load(Displayable):
    # These are the strings that will be accepted as negative for direction input
    negative_list = ['-','neg','n','down','negative']

    def __init__(self, parent, magnitude:float, direction:str):
        super().__init__(parent)

        self.magnitude = magnitude
        self.direction = direction

class Point(Load):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = f"P{self.number}"
        
        self.width_scale = 0.04 #defines width of arrow as fraction of beam length
        self.height_scale = 0.25 #defines height of entire arrow as fraction of dist from beam to top of plot
        self.arrow_height_scale = 0.25 #defines height of arrow triangle as fraction of arrow height

        self.display_array = self.calculate_display_points
    
    def calculate_display_points(self):
        p = self.xlocation
        w = self.width_scale*self.beam.xlength
        h = self.height_scale*self.beam.ymax
        arrow_h = self.arrow_height_scale*h

        x = np.array([p, p, p-w/2, p+w/2, p])

        if self.direction in self.negative_list:
            y = np.array([h, 0, arrow_h, arrow_h, 0])
        else:
            y = np.array([0, h, h-arrow_h, h-arrow_h, h])

        return np.vstack((x,y))

class Moment(Load):
    def __init__(self, beam:Beam, number:int, xlocation:float, magnitude:float, direction:str):
        super().__init__(beam, number, xlocation, magnitude, direction)

        self.label = f"M{self.number}"
        
        self.rad_scale = 0.15 #defines radius as a fraction of dist from beam to top of plot
        self.arrow_corner_scale = 0.03 #defines the inner and outer radius of the corners of the arrow as a fraction from beam to top

        self.display_array = self.calculate_display_points

    def calculate_display_points(self):
        def circle(rad,theta):
            theta = np.deg2rad(theta)
            x = rad*np.cos(theta)
            y = rad*np.sin(theta)

            return x,y

        p = self.xlocation
        r = self.rad_scale*self.beam.ymax
        arw_cnr = self.arrow_corner_scale*self.beam.ymax

        if self.direction in self.negative_list:
            theta = np.linspace(-20,-340,101)
            theta_arw = theta[-1] + 20
        else:
            theta = np.linspace(-160,160,101)
            theta_arw = theta[-1] - 20

        circ_points = circle(r,theta)
        circ_x = circ_points[0]
        circ_y = circ_points[1]

        arw_o = r + arw_cnr
        arw_i = r - arw_cnr

        arw_o_points = circle(arw_o, theta_arw)
        arw_i_points = circle(arw_i, theta_arw)

        arw_x = np.array([arw_o_points[0], arw_i_points[0], circ_x[-1]])
        arw_y = np.array([arw_o_points[1], arw_i_points[1], circ_y[-1]])

        x = np.concatenate((circ_x, arw_x))
        y = np.concatenate((circ_y, arw_y))

        return np.vstack((x,y))

class Dist(Load):
    def __init__(self, parent, number, location1, location2, magnitude1, magnitude2, direction):
        super().__init__(parent, number, direction)

        self.location1 = location1
        self.location2 = location2
        self.magnitude1 = magnitude1
        self.magnitude2 = magnitude2
        self.label = f"w{self.number}"


        
"""
class Controller():
    def __init__(self, diagram):
        self.diagram = diagram
        self.list = []
        self.number = 1
    
    @classmethod
    def create(cls, xlocation):
        title = 
    
class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Beamer")

        # Size of the main window
        self.window_width = 700
        self.window_height = 500

        # Configure to put the window in the center of the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Escape key closes the window
        self.bind("<Escape>",lambda event=None: self.destroy())

        self.setting = Setting(self)

class Setting(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.grid(row=0,column=0,padx=5,pady=5)

        self.diagram = plt.figure(figsize=(3,3))
        plt.xlim(-1,11)
        plt.ylim(-1,1)

        beam = [0,10]
        plt.plot(beam, [0,0], color='k', linewidth=3)

        self.canvas = FigureCanvasTkAgg(self.diagram,master=self)
        self.canvas.get_tk_widget().grid(row=0,column=0)
        self.canvas.draw()


window = Root()
window.mainloop()
"""