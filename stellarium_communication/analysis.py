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

class Analysis():
    def __init__(self):
        self.queue = Queue()         
        stellarium_thread = Thread(target=self.stellarium_telescope_server)
        stellarium_thread.daemon = True
        stellarium_thread.start()    
        stellarium_api_thread = Thread(target=self.stellarium_api_communication)
        stellarium_api_thread.daemon = True
        stellarium_api_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("\nBye!")

    def stellarium_api_communication(self):
        chart_angle = ChartAngle(self.queue, ["Telescope angles - q1/q2", "Telescope velocity - dq1/dq2", "Telescope aceleration - ddq1/ddq2", "Torque"])
        chart_stellarium = ChartAngle(self.queue, ["Stellarium angles - Al/Az", "Stellarium velocity - Al/Az", "Stellarium aceleration - Al/Az", ""])
        chart_position = ChartPosition(self.queue)
        while True:
            self.queue.get()   

            (azs, als) = stellarium_api.get_current_position_focus()
            (az, al) = coords.degStr_2_rad(azs), coords.degStr_2_rad(als)
            
            [stelarium_coordinates, telescope_coordinates, positions] = calculate_parameters(az, al)

            chart_angle.plot_chart(telescope_coordinates)
            chart_stellarium.plot_chart(stelarium_coordinates)
            chart_position.plot_chart(positions)

            self.queue.task_done()

    def stellarium_telescope_server(self):
        test = Telescope_Server(self.queue)
        test.run()   
   
# Run Threads
if __name__ == '__main__':
    Analysis()