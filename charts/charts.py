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



        # x = np.linspace(0, 2 * np.pi, 400)
        # y = np.sin(x ** 2)
        # self.figs, self.axs = plt.subplots(2, 2)
        # self.axs[0, 0].plot(x, y)
        # self.axs[0, 0].set_title("main")
        # self.axs[1, 0].plot(x, y**2)
        # self.axs[1, 0].set_title("shares x with main")
        # self.axs[1, 0].sharex(self.axs[0, 0])
        # self.axs[0, 1].plot(x + 1, y + 1)
        # self.axs[0, 1].set_title("unrelated")
        # self.axs[1, 1].plot(x + 2, y + 2)
        # self.axs[1, 1].set_title("also unrelated")
        # self.figs.tight_layout()
    
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