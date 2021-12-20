import math
import matplotlib.pyplot as plt

from charts.chart_base import ChartBase

class ChartAngle(ChartBase):
    def __init__(self, queue):
        plt.ion()
        self.current_queue = queue
        self.fig, self.axs = plt.subplots(2, figsize=(10,10))
        self.axs[0].title.set_text("q1 angle in degrees")
        self.axs[1].title.set_text("q2 angle in degrees")
        self.run_array_method(self.axs, "grid")
        self.run_array_method(self.axs, "autoscale")
        self.draw()

    def on_running(self, coordinates):
        q1_array = [math.degrees(coordinate[0]) for coordinate in coordinates]
        q2_array = [math.degrees(coordinate[1]) for coordinate in coordinates]
        last_x = self.get_last_x_value(self.axs[0])
        x = [data for data in range(last_x, last_x + len(q1_array))]
        self.axs[0].plot(x, q1_array)
        self.axs[1].plot(x, q2_array)
        self.draw() 