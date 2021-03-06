import variables
import utils
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import constants

# Position of the celestial object Al = Altitude, Az = Azimuth
Al = 3.14/4
Az = 3.14/4

[l1, l2, time_for_each_moviment, steps, previous_position] = constants.get_constants()

# #Zenith
# first_position=[0,0]
# next_position=[Az, Al]


def main():   
    # Calculating Transformations for the robot
    robot  = variables.get_robot_variables()
    qs = symbols('q0:3')
    R10 = utils.rotate_matrix('z', qs[1])
    D10 = utils.position_matrix(robot["l1"])
    T10 = R10*D10
    
    R21 = utils.rotate_matrix('y', -qs[2])
    D21 = utils.position_matrix(robot["l2"])
    T21 = R21*D21

    R32 = utils.rotate_matrix('y', -(Al - qs[2]))
    D32 = utils.position_matrix([0, 0, 0, 1])
    T32 = R32*D32

    T30 = T10*T21*T32
    # pprint(T30)

    # Calculating Transformations for the task
    Als = Symbol('Al')
    Azs = Symbol('Az')
    rs = Symbol('r')
    R50 = utils.rotate_matrix('z', Azs)
    D50 = utils.position_matrix([0, 0, 0, 1])
    T50 = R50*D50
    
    R65 = utils.rotate_matrix('y', -Als)
    D65 = utils.position_matrix([0, 0, 0, 1])
    T65 = R65*D65

    T76 = eye(4)*utils.position_matrix([rs, 0, 0, 1])

    T75 = T50*T65*T76
    # pprint(T75)

    # # Calculating equation for q1 and q2
    # q1s = Azs

    # l1s = robot["l1"][2]
    # l2s = robot["l2"][0]

    # A = (l2s/cos(Al))**2
    # B = l2s**2 + l1s**2
    # C = 2*l1s*l2s
    # D = -1 + B/A
    # E = C/A

    # q2s = asin((-E + sqrt(E**2 - 4*D))/2)

    # q1 = q1s.subs(Azs, Az)
    # # pprint(q1)
    # q2 = q2s.subs([(l1s,l1), (l2s, l2), (Als, Al)])
    # # pprint(q2)


    current_position = [0,0,0]
    next_position = [0.3,0.5,1]
    # loop start
    position =  utils.get_parametrization(current_position, next_position, time_for_each_moviment, steps)
    for i in position:
        T03 = 

    
    # https://stackoverflow.com/questions/38118598/3d-animation-using-matplotlib



    # x = l2*cos(q1)*cos(q2)
    # y = l2*sin(q1)*cos(q2)
    # z = l1 + l2*sin(q2)

    # coordinates = [x, y, z]

    # # pprint(coordinates)

    # plot_chart(coordinates)

# def plot_chart(coordinates):
#     plt.axes(projection='3d')

#     # Data for a three-dimensional line
#     r = np.linspace(0, 5, 500)
#     xline = r*np.cos(Al)*np.cos(Az)
#     yline = r*np.cos(Al)*np.sin(Az)
#     zline = r*np.sin(Al)
#     plt.plot(xline, yline, zline, color = "blue")

#     plt.plot([coordinates[0]],[coordinates[1]],[coordinates[2]], marker='o', markersize=3, color="red")

#     plt.show()

def calculate_position(T, az, al):
    pprint(T(:,4))

if __name__ == "__main__":
    main()