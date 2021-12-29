import numpy as np
from charts.chart_base import ChartBase
import constants
import matplotlib.pyplot as plt

class ChartPosition(ChartBase):
    def __init__(self, queue):
        plt.ion()
        self.current_queue = queue
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.set_xlim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_ylim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_zlim3d(0, constants.l1 + constants.l2)
        self.set_quiver()        
        self.draw()
        self.set_loop()
    
    def set_quiver(self):
        x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
        u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
        self.ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black") 

    def on_running(self, coordinates):
        color = np.random.rand(3,)
        for (x,y,z) in coordinates:
            self.ax.scatter(x, y, z, color=color)
            self.draw()   
        self.set_loop()  