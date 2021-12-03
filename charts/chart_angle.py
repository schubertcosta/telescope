import math
import matplotlib.pyplot as plt

class ChartAngle():
    def __init__(self):
        plt.ion()
        self.fig, self.axs = plt.subplots(2)
        self.fig.suptitle("q1 and q2 (telescope) in degrees")
        self.draw()
    
    def draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def on_running(self, coordinates):
        q1_array = [math.degrees(coordinate[0]) for coordinate in coordinates]
        q2_array = [math.degrees(coordinate[1]) for coordinate in coordinates]
        x = [data for data in range(len(q1_array))]
        plt.pause(0.3)
        self.axs[0].plot(x, q1_array)
        self.axs[1].plot(x, q2_array)
        self.draw()                   

    def plot_chart(self, coordinates, block = False):
        self.on_running(coordinates)
        if block:
            plt.show(block=True)