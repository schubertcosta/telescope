import utils
from sympy import *
import sys
sys.path.insert(1, '../telescope')
sys.path.insert(1, '../charts')
import constants
from numpy import pi

# Calculating Transformations for the robot
robot  = constants.robot_structure
Als = Symbol('Al')
Azs = Symbol('Az')

qs = symbols('q1:3')
R10 = utils.rotate_matrix('z', qs[0])
D10 = utils.position_matrix(robot["l1"])
T10 = R10*D10

R21 = utils.rotate_matrix('y', -qs[1])
D21 = utils.position_matrix(robot["l2"])
T21 = R21*D21
T20 = T10*T21

# Calculating rotation in y axis
R32 = utils.rotate_matrix('y', -(Als - qs[1]))
D32 = utils.position_matrix([0, 0, 0, 1])
T32 = R32*D32

T30 = T20*T32

# Calculating Transformations for the task
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

l1s = robot["l1"][2]
l2s = robot["l2"][0]

q1s = [Azs]

A = (l2s/cos(Als))**2
B = l2s**2 + l1s**2
C = 2*l1s*l2s
D = -1 + B/A
E = C/A

q2s = [asin((-E + sqrt(E**2 - 4*D))/2),  asin((-E - sqrt(E**2 - 4*D))/2)]

# That is the telescope last position
last_position = constants.initial_position
last_q_position = constants.initial_q_position
last_xyz_position = constants.initial_xyz_position

def calculate_parameters(az, al):
    global last_position
    global last_q_position
    global last_xyz_position

    if not (verify_route(az, constants.az_limit) and verify_route(al, constants.al_limit)):
        return [last_xyz_position]
    (az, al) = [get_faster_route([az, az-2*pi], last_position[0]), get_faster_route([al, al-2*pi] if al >= 0 else [al, al+2*pi], last_position[1])]    

    # loop start   
    T75_radius_adapted = T75.subs([(rs, T30[0:3,3].norm())])

    [stellarium_angles, d_stellarium_angles, dd_stellarium_angles] =  utils.get_parametrization(last_position, [az, al], constants.time_for_each_moviment, constants.steps)
    positions = []
    q = []

    for next_intermediate_angle in stellarium_angles:
        q1 = get_best_q(q1s, [(Azs, next_intermediate_angle[0])], constants.q1_limit, 1, last_q_position[0])
        q2 = get_best_q(q2s, [(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1])], constants.q2_limit, 2, last_q_position[1])

        last_q_position = [q1, q2]
        q.append(last_q_position)
        last_position = next_intermediate_angle

        R75 = T75_radius_adapted[0:3,3].subs([(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1]), (Azs, next_intermediate_angle[0]), (qs[0], q1), (qs[1], q2)])
        last_xyz_position = R75
        positions.append(R75)
    
    return [[stellarium_angles, d_stellarium_angles, dd_stellarium_angles], [q, [[0.0,0.0]], [[0.0,0.0]]], positions]

def verify_route(angle, range):
    if angle >= range[0] and angle <= range[1]:
        return True
    return False

def get_faster_route(angles, last_position):
    min = 2*pi
    shortest_angle = last_position
    for current_angle in angles:
        if abs(current_angle-last_position) <= min:
            min = abs(current_angle-last_position)
            shortest_angle = current_angle
    return shortest_angle

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
        raise ValueError("Error - q%d out of range. q_array -> %s" % (q_number, q_array))

    return get_faster_route(q_candidate_array, last_position)