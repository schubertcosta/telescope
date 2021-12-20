import matplotlib.pyplot as plt

class ChartBase():    
    def run_array_method(self, array, method_name, params = None):
        for element in array:
            getattr(element, method_name)(params)

    def draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def on_running(self, coordinates):
        raise NotImplementedError("Please Implement this method")   
    
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