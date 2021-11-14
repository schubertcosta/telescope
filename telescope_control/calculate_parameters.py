import utils
from sympy import *
import constants
from numpy import pi

# Calculating Transformations for the robot
robot  = constants.robot_structure
qs = symbols('q1:3')
R10 = utils.rotate_matrix('z', qs[0])
D10 = utils.position_matrix(robot["l1"])
T10 = R10*D10

R21 = utils.rotate_matrix('y', -qs[1])
D21 = utils.position_matrix(robot["l2"])
T21 = R21*D21
T20 = T10*T21

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
q1s = [Azs]

l1s = robot["l1"][2]
l2s = robot["l2"][0]

A = (l2s/cos(Als))**2
B = l2s**2 + l1s**2
C = 2*l1s*l2s
D = -1 + B/A
E = C/A

q2s = [asin((-E + sqrt(E**2 - 4*D))/2),  asin((-E - sqrt(E**2 - 4*D))/2)]

# That is the telescope last position
last_position = constants.initial_position

def calculate_parameters(az, al):
    global last_position

    # (az, al) = normalize_coordinates(az, al, last_position)

    # Calculating rotation in y axis
    R32 = utils.rotate_matrix('y', -(al - qs[1]))
    D32 = utils.position_matrix([0, 0, 0, 1])
    T32 = R32*D32

    T30 = T20*T32
    # loop start   
    T75_radius_adapted = T75.subs([(rs, T30[0:3,3].norm())])

    angles =  utils.get_parametrization(last_position, [az, al], constants.time_for_each_moviment, constants.steps)
    positions = []
    q = []

    for index, next_intermediate_angle in enumerate(angles):
        q1 = get_best_q(q1s, [(Azs, next_intermediate_angle[0])], constants.q1_limit, 1, last_position[0] if index == 0 else angles[index-1][0])
        q2 = get_best_q(q2s, [(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1])], constants.q2_limit, 2, last_position[1] if index == 0 else angles[index-1][1])

        q.append([q1, q2])
        last_position = next_intermediate_angle

        R75 = T75_radius_adapted[0:3,3].subs([(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1]), (Azs, next_intermediate_angle[0]), (qs[0], q1), (qs[1], q2)])
        positions.append(R75)
        
    return positions

def normalize_coordinates(az, al, last_position):
    az_data = [az, -2*pi + az]
    q1_list = []
    az_new = az
    al_new = al

    for az_current in az_data:
        try:
            q1_list.append(get_best_q(q1s, [(Azs, az_current)], constants.q1_limit, 1))
        except Exception as error:
            print('Caught this error: ' + repr(error))
            continue
    
    if len(q1_list) == 0:
        print("There is no q1 valid, please review the code or the telescope limits")
        exit()
    else:
        # just because q1=az
        max = 2*pi
        for q in q1_list:
            if abs(q-last_position[0]) < max:
                az_new = q

    return az_new, al_new


def get_best_q(qs_array, sub_params, range, q_number, last_position):
    q_array = [qs.subs(sub_params) for qs in qs_array]
    q_candidate_array = []

    for q in q_array:
        if im(q) >= constants.max_tolerated_imaginary:
            print("q%d contains a complex number, q%d = %s" % (q_number, q_number, q))
            continue

        if im(q):
            q = re(q)
            
        if q >= range[0] and q <= range[1]:
            q_candidate_array.append(q)
    
    if len(q_candidate_array) == 0:
        print("All candidates for q%d are out of range" % (q_number))
        raise ValueError("Error - q%d out of range" % (q_number))
    
    min = 2*pi
    best_q = q_candidate_array[0]
    for q in q_candidate_array:
        if abs(q-last_position) < min:
            best_q = q
    return best_q


# def get_best_q2(q2s, sub_params, previous_q2):
#     range = constants.q2_limit
#     q2_1 = q2s[0].subs(sub_params)
#     q2_2 = q2s[1].subs(sub_params)
#     q2 = 0

#     if im(q2_1) >= constants.max_tolerated_imaginary or im(q2_2) >= constants.max_tolerated_imaginary:
#         print("q2 contains a complex number, q2 =", q2)
#         exit()

#     if abs(q2_1-previous_q2) >= abs(q2_2-previous_q2):
#         q2 = q2_2
#     q2 = q2_1
#     if im(q2):
#         q2 = re(q2)

#     if q2 >= range[0] and q2 <= range[1]:
#         return q2   

#     print("Value of q2 out of range --> q2 = ", q2)
#     exit()
    
if __name__ == "__main__":
    calculate_parameters(3.14,3.14/4)