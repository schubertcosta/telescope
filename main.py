import variables
import utils
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import constants

# Position of the celestial object Al = Altitude, Az = Azimuth
Al = 3.14/4
Az = 3.14/4

[l1, l2, time_for_each_moviment, steps, previous_position, current_position] = constants.get_constants()

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

    # Calculating Transformations for the task
    Als = Symbol('Al')
    Azs = Symbol('Az')
    R50 = utils.rotate_matrix('z', Azs)
    D50 = utils.position_matrix([0, 0, 0, 1])
    T50 = R50*D50
    
    R65 = utils.rotate_matrix('y', -Als)
    D65 = utils.position_matrix([0, 0, 0, 1])
    T65 = R65*D65

    # rs = get_radius_distance(T30)
    rs = Symbol('r')
    T76 = eye(4)*utils.position_matrix([rs, 0, 0, 1])

    T75 = T50*T65*T76

    # pprint(T75)

    # Calculating equation for q1 and q2
    q1s = Azs

    l1s = robot["l1"][2]
    l2s = robot["l2"][0]

    A = (l2s/cos(Al))**2
    B = l2s**2 + l1s**2
    C = 2*l1s*l2s
    D = -1 + B/A
    E = C/A

    q2s = asin((-E + sqrt(E**2 - 4*D))/2)

    # loop start
    q1 = q1s.subs(Azs, Az)
    q2 = q2s.subs([(l1s,l1), (l2s, l2), (Als, Al)])
    T75_radius_adapted = T75.subs([(rs, get_radius_distance(T30))])
    next_position = calculate_position(T75_radius_adapted, [(l1s,l1), (l2s, l2), (Als, Al), (Azs, Az), (qs[1], q1), (qs[2], q2)])
    positions =  utils.get_parametrization(current_position, next_position, time_for_each_moviment, steps)
    q1_inter = []
    q2_inter = []

    for next_intermediate_position in positions:
        radius = sqrt(next_intermediate_position[0]**2 + next_intermediate_position[1]**2 + next_intermediate_position[2]**2)
        Al_inter = asin(next_intermediate_position[2]/radius)
        Az_inter = atan(next_intermediate_position[1]/next_intermediate_position[1])

        q1_inter.append(q1s.subs(Azs, Az_inter))
        q2_inter.append(q2s.subs([(l1s,l1), (l2s, l2), (Als, Al_inter)]))
    

    
    # https://stackoverflow.com/questions/38118598/3d-animation-using-matplotlib



    # x = l2*cos(q1)*cos(q2)
    # y = l2*sin(q1)*cos(q2)
    # z = l1 + l2*sin(q2)

    # coordinates = [x, y, z]

    # # pprint(coordinates)

    plot_chart(positions)

def plot_chart(coordinates):
    # plt.axes(projection='3d')

    # # Data for a three-dimensional line
    # r = np.linspace(0, 5, 500)
    # xline = r*np.cos(Al)*np.cos(Az)
    # yline = r*np.cos(Al)*np.sin(Az)
    # zline = r*np.sin(Al)
    # plt.plot(xline, yline, zline, color = "blue")
    pprint(coordinates)

    

    x,y,z = zip(coordinates)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(x, y, z, '.')
    ax.legend()
    plt.show()
    # plt.scatter(coordinates[:,0],coordinates[:,1], coordinates[:,2])

    # plt.show()

def get_radius_distance(T):
    array = T[0:3,3]
    return sqrt(array[0]**2 + array[1]**2 + array[2]**2)

def calculate_position(T, subs):
    array = T[0:3,3].subs(subs)
    return [array[0], array[1], array[2]]
    
if __name__ == "__main__":
    main()