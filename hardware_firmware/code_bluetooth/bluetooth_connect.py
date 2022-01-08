import time
import sys

from sympy.matrices.dense import eye
sys.path.insert(1, '../../../telescope')
import constants
import serial.tools.list_ports
import serial

def main():
    ports = serial.tools.list_ports.comports()
    port_names = [port.name for port in ports]
    if(constants.telescope_COM_port not in port_names):
        print("%s port not found, exiting program..." % constants.telescope_COM_port)
        quit()

    try:
        serial_port = serial.Serial(port = constants.telescope_COM_port, baudrate=9600,
                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    except:
        print("Error when connecting with serial port")
        quit()

    check_connection(serial_port)

    while(1):
        # here we will get the data from the thread
        coordinates = input("Enter the motor position as [Az,Al]: ")
        motor_coordinates = convert_coordinates(coordinates)
        serial_port.write(motor_coordinates.encode())

def convert_coordinates(coordinates):
    return coordinates*(eye(2)*(constants.gear_radius[0]/constants.gear_radius[1])/constants.motor_step)

def check_connection(serial_port):
    serialString = ""   
    connecting_attempts = 5

    while(serialString == ""):
        serial_port.write(b"IS_ALIVE\r")

        if(serial_port.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serial_port.readline()

            # Print the contents of the serial data
            data_received = (serialString.decode('Ascii'))
            if(data_received == "YES"):
                return
            
        if(connecting_attempts == 0):
            print("Failed to coonect with device")
            quit()
        else:
            connecting_attempts -= 1
            time.sleep(1)

if __name__ == '__main__':
    main()