import logging
import time
import sys
import numpy as np

from sympy.matrices.dense import eye
sys.path.insert(1, '../../../telescope')
import constants
import serial.tools.list_ports
import serial

    # while(1):
    #     # here we will get the data from the thread
    #     coordinates = []
    #     print("Enter the telescope rotation as [Az,Al]: ")
    #     coordinates.append(float(input()))
    #     coordinates.append(float(input()))
    #     motor_coordinates = convert_coordinates(coordinates)
    #     serial_port.write(motor_coordinates.encode())
class TelescopeConnect():    
    def __init__(self):
        ports = serial.tools.list_ports.comports()
        port_names = [port.name for port in ports]
        if(constants.telescope_COM_port not in port_names):
            logging.debug("%s port not found, exiting program..." % constants.telescope_COM_port)
            quit()

        try:
            self.serial_port = serial.Serial(port = constants.telescope_COM_port, baudrate=9600,
                                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        except:
            logging.debug("Error when connecting with serial port")
            quit()

        serialString = ""   
        connecting_attempts = 5

        while(serialString == ""):
            self.serial_port.write(b"IS_ALIVE\r")

            if(self.serial_port.in_waiting > 0):
                # Read data out of the buffer until a carraige return / new line is found
                serialString = self.serial_port.readline()

                # Print the contents of the serial data
                data_received = (serialString.decode('Ascii'))
                if(data_received == "YES"):
                    logging.debug("Telescope connected via Bluetooth!")
                    return
                
            if(connecting_attempts == 0):
                logging.debug("Failed to coonect with device")
                quit()
            else:
                logging.debug("Attempt %s to connect with bluetooth" % connecting_attempts)
                connecting_attempts -= 1
                time.sleep(2)

    def move_motors(self, target_coordinates):
        coordinates = target_coordinates[-1]
        motor_coordinates = self.convert_coordinates(coordinates)
        self.serial_port.write(motor_coordinates.encode())

    def convert_coordinates(self, coordinates):
        conversion_matrix = eye(2)*((constants.gear_radius[0]/constants.gear_radius[1])/constants.motor_step)
        motor_position = np.matmul(coordinates, conversion_matrix)
        return "%d,%d" % (motor_position[0], motor_position[1])    

if __name__ == '__main__':
    TelescopeConnect()