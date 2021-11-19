import numpy as np
import constants
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class ChartUpdate():
    def on_launch(self):
        plt.ion()
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)
        self.ax.set_xlim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_ylim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_zlim3d(0, constants.l1 + constants.l2)
        self.set_quiver()
        
        self.draw()
    
    def draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def on_running(self, coordinates):
        color = np.random.rand(3,)
        for (x,y,z) in coordinates:
            plt.pause(0.3)
            self.ax.scatter(x, y, z, color=color)
            self.draw()        
        
    def set_quiver(self):
        x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
        u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
        self.ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black")        

    def plot_chart(self, coordinates, queue, block = False):
        self.on_running(coordinates)
        if queue:
            while queue.empty():
                plt.pause(0.01)
        elif block:
            plt.show(block=True)