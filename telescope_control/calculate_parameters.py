import variables
import utils
from sympy import *
import constants
import charts
import numpy as np

# Position of the celestial object Al = Altitude, Az = Azimuth
# Al = 3.14/4
# Az = 3.14/4

def calculate_parameters(Az, Al):   
    # Calculating Transformations for the robot
    robot  = variables.get_robot_variables()
    qs = symbols('q1:3')
    R10 = utils.rotate_matrix('z', qs[0])
    D10 = utils.position_matrix(robot["l1"])
    T10 = R10*D10
    
    R21 = utils.rotate_matrix('y', -qs[1])
    D21 = utils.position_matrix(robot["l2"])
    T21 = R21*D21
    T20 = T10*T21

    R32 = utils.rotate_matrix('y', -(Al - qs[1]))
    D32 = utils.position_matrix([0, 0, 0, 1])
    T32 = R32*D32

    T30 = T20*T32

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

    # Calculating equation for q1 and q2
    q1s = Azs

    l1s = robot["l1"][2]
    l2s = robot["l2"][0]

    A = (l2s/cos(Als))**2
    B = l2s**2 + l1s**2
    C = 2*l1s*l2s
    D = -1 + B/A
    E = C/A

    q2s = [asin((-E + sqrt(E**2 - 4*D))/2),  asin((-E - sqrt(E**2 - 4*D))/2)]

    # loop start   
    T75_radius_adapted = T75.subs([(rs, T30[0:3,3].norm())])

    angles =  utils.get_parametrization(constants.current_position, [Az, Al], constants.time_for_each_moviment, constants.steps)
    positions = []
    q = []

    for index, next_intermediate_angle in enumerate(angles):
        q1 = get_best_q1(q1s, [(Azs, next_intermediate_angle[0])])
        q2 = get_best_q2(q2s, [(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1])], constants.current_position[1] if index == 0 else angles[index-1][1])
        new_position = [q1, q2]
        q.append(new_position)
        constants.current_position = new_position

        R75 = T75_radius_adapted[0:3,3].subs([(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1]), (Azs, next_intermediate_angle[0]), (qs[0], q1), (qs[1], q2)])
        positions.append(R75)

    charts.plot_chart(positions)

def get_best_q1(q1s, sub_params):
    range = constants.q1_limit
    q1 = q1s.subs(sub_params)

    if im(q1) >= constants.max_tolerated_imaginary:
        print("q1 contains a complex number, q1 = ", q1)
        exit()
    
    if im(q1):
        q1 = re(q1)

    if q1 >= range[0] and q1 <= range[1]:
        return q1    

    print("Value of q1 out of range --> q1 = ", q1)
    exit()


def get_best_q2(q2s, sub_params, previous_q2):
    range = constants.q2_limit
    q2_1 = q2s[0].subs(sub_params)
    q2_2 = q2s[1].subs(sub_params)
    q2 = 0

    if im(q2_1) >= constants.max_tolerated_imaginary or im(q2_2) >= constants.max_tolerated_imaginary:
        print("q2 contains a complex number, q2 =", q2)
        exit()

    if abs(q2_1-previous_q2) >= abs(q2_2-previous_q2):
        q2 = q2_2
    q2 = q2_1
    if im(q2):
        q2 = re(q2)

    if q2 >= range[0] and q2 <= range[1]:
        return q2   

    print("Value of q2 out of range --> q2 = ", q2)
    exit()
    
if __name__ == "__main__":
    calculate_parameters()