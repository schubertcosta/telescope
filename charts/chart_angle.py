import math
import matplotlib.pyplot as plt

class ChartAngle():
    def __init__(self, queue):
        plt.ion()
        self.current_queue = queue
        self.fig, self.axs = plt.subplots(2, figsize=(10,10))
        self.axs[0].title.set_text("q1 angle in degrees")
        self.axs[1].title.set_text("q2 angle in degrees")
        self.run_array_method(self.axs, "grid")
        self.run_array_method(self.axs, "autoscale")
        self.draw()
        self.set_loop()
    
    def run_array_method(self, array, method_name, params = None):
        for element in array:
            getattr(element, method_name)(params)

    def draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.set_loop()

    def on_running(self, coordinates):
        q1_array = [math.degrees(coordinate[0]) for coordinate in coordinates]
        q2_array = [math.degrees(coordinate[1]) for coordinate in coordinates]
        last_x = self.get_last_x_value(self.axs[0])
        x = [data for data in range(last_x, last_x + len(q1_array))]
        self.axs[0].plot(x, q1_array)
        self.axs[1].plot(x, q2_array)
        self.draw()           
    
    def get_last_x_value(self, axis):
        try:
            return max(axis.lines[-1].get_xdata())
        except:
            return 0

    def set_loop(self):
        if self.current_queue:
            while self.current_queue.empty():
                plt.pause(0.01)

    def plot_chart(self, coordinates, block = False):
        self.on_running(coordinates)
        if block:
            plt.show(block=True)