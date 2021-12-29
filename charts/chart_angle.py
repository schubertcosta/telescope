import math
import matplotlib.pyplot as plt
from charts.chart_base import ChartBase

class ChartAngle(ChartBase):
    def __init__(self, queue, title):
        plt.ion()
        self.current_queue = queue
        self.fig, self.axs = plt.subplots(3, figsize=(10,10))
        self.axs[0].title.set_text(title[0])
        self.axs[1].title.set_text(title[1])
        self.axs[2].title.set_text(title[2])
        self.run_array_method(self.axs, "grid")
        self.run_array_method(self.axs, "autoscale")
        self.draw()

    def on_running(self, coordinates_array):
        for index, coordinates in enumerate(coordinates_array):
            q1_array = [math.degrees(coordinate[0]) for coordinate in coordinates]
            q2_array = [math.degrees(coordinate[1]) for coordinate in coordinates]
            last_x = self.get_last_x_value(self.axs[0])
            x = [data for data in range(last_x, last_x + len(q1_array))]
            self.axs[index].plot(x, q1_array, c="red", label="1")
            self.axs[index].plot(x, q2_array, c="blue", label="2")
            self.draw() 