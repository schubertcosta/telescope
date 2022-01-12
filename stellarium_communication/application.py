from hardware_firmware.code_bluetooth.bluetooth_connect import TelescopeConnect
from telescope_control.calculate_parameters import calculate_parameters
from telescope_server import Telescope_Server
from queue import Queue
from threading import Thread
import logging
import time
import stellarium_api
import coords
# from freecad.freecad_animation import FreeCadAnimation

class Application():
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
        # freecad = FreeCadAnimation()
        # telescope_connection = TelescopeConnect()

        while True:
            self.queue.get()   

            (azs, als) = stellarium_api.get_current_position_focus()
            (az, al) = coords.degStr_2_rad(azs), coords.degStr_2_rad(als)

            [stelarium_coordinates, telescope_coordinates, positions] = calculate_parameters(az, al, True)

            # telescope_connection.move_motors(telescope_coordinates[0])
            # freecad.set_position(telescope_coordinates[0])

            # if self.queue:
            #     while self.queue.empty():
            #         freecad.free_gui()

            self.queue.task_done()

    def stellarium_telescope_server(self):
        stellarium_server = Telescope_Server(self.queue)
        stellarium_server.run()

# Run Threads
if __name__ == '__main__':
    Application()