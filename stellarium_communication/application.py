from charts.chart_angle import ChartAngle
from charts.chart_position import ChartPosition
from telescope_control.calculate_parameters import calculate_parameters
from telescope_server import Telescope_Server
from queue import Queue
from threading import Thread
import logging
import time
import stellarium_api
import coords
import matplotlib.pyplot as plt
from freecad.pieces_control import FreeCadAnimation

def stellarium_api_communication(queue):
    chart = ChartPosition()
    chart_angles = ChartAngle()
    freecad = FreeCadAnimation()
    while True:
        queue.get()   

        (azs, als) = stellarium_api.get_current_position_focus()
        (az, al) = coords.degStr_2_rad(azs), coords.degStr_2_rad(als)

        [positions, angles] = calculate_parameters(az, al)
        chart.plot_chart(positions)
        chart_angles.plot_chart(angles)
        freecad.set_position(angles)

        if queue:
            while queue.empty():
                plt.pause(0.01)

        queue.task_done()

def stellarium_telescope_server(queue):
    test = Telescope_Server(queue)
    test.run()

class Application():
    queue = Queue()     
    stellarium_api_thread = Thread(target=stellarium_api_communication, args=(queue,))
    stellarium_api_thread.daemon = True
    stellarium_api_thread.start()
    stellarium_thread = Thread(target=stellarium_telescope_server, args=(queue,))
    stellarium_thread.daemon = True
    stellarium_thread.start()    
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.debug("\nBye!")

# Run Threads
if __name__ == '__main__':
    Application()