import variables
import utils
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import constants

# Position of the celestial object Al = Altitude, Az = Azimuth
Al = 3.14/4
Az = 3.14/4

[l1, l2, time_for_each_moviment, steps, current_position] = constants.get_constants()

def main():   
    # Calculating Transformations for the robot
    robot  = variables.get_robot_variables()
    qs = symbols('q1:3')
    R10 = utils.rotate_matrix('z', qs[0])
    D10 = utils.position_matrix(robot["l1"])
    T10 = R10*D10
    pprint(T10)
    
    R21 = utils.rotate_matrix('y', -qs[1])
    D21 = utils.position_matrix(robot["l2"])
    T21 = R21*D21
    T20 = T10*T21

    R32 = utils.rotate_matrix('y', -(Al - qs[1]))
    D32 = utils.position_matrix([0, 0, 0, 1])
    T32 = R32*D32

    T30 = T20*T32
    # pprint(T30)

    # Calculating Transformations for the task
    Als = Symbol('Al')
    Azs = Symbol('Az')
    R50 = utils.rotate_matrix('z', Azs)
    D50 = utils.position_matrix([0, 0, 0, 1])
    T50 = R50*D50
    
    R65 = utils.rotate_matrix('y', -Als)
    D65 = utils.position_matrix([0, 0, 0, 1])
    T65 = R65*D65

    rs = Symbol('r')
    T76 = eye(4)*utils.position_matrix([rs, 0, 0, 1])

    T75 = T50*T65*T76

    # pprint(T75)

    # Calculating equation for q1 and q2
    q1s = Azs

    l1s = robot["l1"][2]
    l2s = robot["l2"][0]

    A = (l2s/cos(Als))**2
    B = l2s**2 + l1s**2
    C = 2*l1s*l2s
    D = -1 + B/A
    E = C/A

    q2s = asin((-E + sqrt(E**2 - 4*D))/2)
    # pprint(q2s)

    # loop start   
    T75_radius_adapted = T75.subs([(rs, get_radius_distance(T30))])
    # pprint(T75_radius_adapted)

    angles =  utils.get_parametrization(current_position, [Az, Al], time_for_each_moviment, steps)
    positions = []
    q = []
    pprint(angles)

    for next_intermediate_angle in angles:
        q1 = q1s.subs(Azs, next_intermediate_angle[0])
        q2 = q2s.subs([(l1s,l1), (l2s, l2), (Als, next_intermediate_angle[1])])

        q.append([q1, q2])
        positions.append(calculate_position(T75_radius_adapted, [(l1s,l1), (l2s, l2), (Als, next_intermediate_angle[1]), (Azs, next_intermediate_angle[0]), (qs[0], q1), (qs[1], q2)]))

    plot_chart(positions)

def plot_chart(coordinates):
    x = (list(map(lambda x: x[0], coordinates)))
    y = (list(map(lambda x: x[1], coordinates)))
    z = (list(map(lambda x: x[2], coordinates)))
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    limit = l1 + l2
    ax.set_xlim3d(0, limit)
    ax.set_ylim3d(0, limit)
    ax.set_zlim3d(0, limit)
    ax = set_quiver(ax)
    ax.plot(x, y, z, '.')
    ax.legend()
    plt.show()

def set_quiver(ax):
    x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
    u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
    ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black")
    return ax

def get_radius_distance(T):
    array = T[0:3,3]
    return sqrt(array[0]**2 + array[1]**2 + array[2]**2)

def calculate_position(T, subs):
    array = T[0:3,3].subs(subs)
    return [array[0], array[1], array[2]]
    
if __name__ == "__main__":
    main()