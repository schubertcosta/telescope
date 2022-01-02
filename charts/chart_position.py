import numpy as np
from charts.chart_base import ChartBase
import constants
import matplotlib.pyplot as plt

class ChartPosition(ChartBase):
    def __init__(self, queue):
        plt.ion()
        module_lim = constants.l2*1.2
        self.current_queue = queue
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_xlim3d(-module_lim, module_lim)
        self.ax.set_ylim3d(-module_lim, module_lim)
        self.ax.set_zlim3d(0, module_lim + constants.l1)
        self.set_quiver()        
        telescope_size = ([[0, 0, t] for t in np.linspace(0, constants.l1, num=10)] + [[t, 0, constants.l1] for t in np.linspace(0, constants.l2,num=10)])
        self.on_running(telescope_size, "black")
        self.draw()
    
    def set_quiver(self):
        x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
        u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
        self.ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black") 

    def on_running(self, coordinates, override_color = None):
        color = np.random.rand(3,)
        for (x,y,z) in coordinates:
            self.ax.scatter(x, y, z, color= override_color if override_color != None else color)
            self.draw()   
        self.set_loop()  