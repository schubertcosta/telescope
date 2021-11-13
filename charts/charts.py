import numpy as np
import constants
import matplotlib.pyplot as plt


plt.ion()
class ChartUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def on_launch(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.lines, = self.ax.plot([], [], [], '.')
        self.ax.set_xlim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_ylim3d(-constants.l2*1.2, constants.l2*1.2)
        self.ax.set_zlim3d(0, constants.l1 + constants.l2)
        self.ax = self.set_quiver()
        self.x, self.y, self.z = [[],[],[]]

    def on_running(self, coordinates):
        x = (list(map(lambda x: x[0], coordinates)))
        y = (list(map(lambda y: y[1], coordinates)))
        z = (list(map(lambda z: z[2], coordinates)))

        self.x += x
        self.y += y
        self.z += z
        
        self.lines.set_data_3d(self.x,self.y,self.z)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_quiver(self):
        x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
        u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
        self.ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black")

    def plot_chart(self, coordinates):
        import time
        self.on_running(coordinates)
        time.sleep(1)