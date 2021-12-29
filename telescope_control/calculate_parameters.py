import utils
from sympy import *
import sys
sys.path.insert(1, '../telescope')
sys.path.insert(1, '../charts')
import constants
import numpy as np
from numpy import pi
# import autograd.numpy as np
# import autograd.numpy as anp
# from autograd import grad, jacobian

# Calculating Transformations for the robot
robot  = constants.robot_structure
Als = Symbol('Al')
Azs = Symbol('Az')

qs = symbols('q1:3')
dqs = Matrix(symbols('dq1:3'))
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

# Cinematic and Dinamic parameters
Pg10 = T10*constants.Pg11
JL10 = Pg10[0:3,0].jacobian(qs)
JA10 = Matrix(BlockMatrix([T10[0:3,3], Matrix(np.zeros((3,1)))]))
dPg10 = Matrix([JL10, JA10])*dqs
II10 = T10[0:3,0:3]*constants.II11*(T10[0:3,0:3].T)

Pg20 = T20*constants.Pg22
JL20 = Pg20[0:3,0].jacobian(qs)
JA20 = Matrix(BlockMatrix([T10[0:3,3], T20[0:3,3]]))
dPg20 = Matrix([JL20, JA20])*dqs
II20 = T20[0:3,0:3]*constants.II22*(T20[0:3,0:3].T)

JLA = Matrix(BlockMatrix([[JL20], [JA20]]))

dJL = Matrix(BlockMatrix([(JL20[0:3,0].jacobian(qs))*dqs, (JL20[0:3,1].jacobian(qs))*dqs]))
dJA = Matrix(BlockMatrix([(JA20[0:3,0].jacobian(qs))*dqs, (JA20[0:3,1].jacobian(qs))*dqs]))
dJLA = Matrix(BlockMatrix([[dJL], [dJA]]))

# Calculating system energy
Pg = Matrix(BlockMatrix([Pg10, Pg20]))
dPg = Matrix(BlockMatrix([dPg10, dPg20]))

L = 0
for i in range(2):
    L += utils.calculate_energy(constants.mass_matrix[i], dPg[:,i], constants.II[0], Pg[:,i], constants.g0)

dLdqp = utils.gradient(L, dqs)
dLdq = utils.gradient(L, qs)

dEddqp = np.matmul(constants.mi, dqs)

# syms q1(t) q2(t) q3(t) q4(t) q5(t) q6(t)
# q_L = [q1(t) q2(t) q3(t) q4(t) q5(t) q6(t)]';
# dq_L = diff(q_L,t);
# ddq_L = diff(dq_L,t);

# ddLdqpdt = diff(subs(dLdqp,[q dq'],[q_L' dq_L']),t);

quit()
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
    q, dq, ddq = [[],[],[]]

    for index, next_intermediate_angle in enumerate(stellarium_angles):
        q1 = get_best_q(q1s, [(Azs, next_intermediate_angle[0])], constants.q1_limit, 1, last_q_position[0])
        q2 = get_best_q(q2s, [(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1])], constants.q2_limit, 2, last_q_position[1])

        last_q_position = [q1, q2]
        q.append(last_q_position)
        last_position = next_intermediate_angle

        T75num = T75_radius_adapted[0:3,0:3].subs([(l1s, constants.l1), (l2s, constants.l2), (Als, next_intermediate_angle[1]), (Azs, next_intermediate_angle[0]), (qs[0], q1), (qs[1], q2)])
        last_xyz_position = T75num[0:3,2]
        positions.append(last_xyz_position)

        ## Calculating velocity
        V_ref_0 = np.matmul(np.array(T75num),[d_stellarium_angles[index][0], d_stellarium_angles[index][1], 0])
        V = np.array([0.0, 0.0, 0.0, V_ref_0[0], V_ref_0[1], V_ref_0[2]])
        JLAnum = np.array(JLA.subs([(l1s, constants.l1), (l2s, constants.l2), (qs[0], q1), (qs[1], q2)]))
        dqnum = np.matmul((JLAnum.T), V)
        dq.append(dqnum)
        
        # Calculating acceleration
        A_ref_0 = np.matmul(np.array(T75num),[dd_stellarium_angles[index][0], dd_stellarium_angles[index][1], 0])
        A = np.array([0.0, 0.0, 0.0, A_ref_0[0], A_ref_0[1], A_ref_0[2]])
        dJLAnum = np.array(JLA.subs([(l1s, constants.l1), (l2s, constants.l2), (qs[0], q1), (qs[1], q2), (dqs[0], dqnum[0]), (dqs[1], dqnum[1])]))
        ddq_jacobian_dem = np.matmul(dJLAnum, dqnum)
        ddq_dem = np.subtract(A, ddq_jacobian_dem)
        ddqnum = np.matmul((dJLAnum.T), ddq_dem)
        ddq.append(ddqnum)

        # Calculating torques
        T1, T2, T3 = [[], [], []]

        # for p in range(2):
        #     T1[p] = 
        #     T2[p] = 
        #     T3[p] = 

        # %Calculando os torques
        # for p = 1:length(q)
        #     T1(p) = double(subs(ddLdqpdt(p),[q_L' dq_L' ddq_L'],[matrizPosicaoJuntas(i,:) matrizVelocidadeJuntas(i,:) matrizAceleracaoJuntas(i,:)]));
        #     T2(p) = -double(subs(dLdq(p),[q dq'],[matrizPosicaoJuntas(i,:) matrizVelocidadeJuntas(i,:)]));
        #     T3(p) = double(subs(dEddqp(p),[q dq'],[matrizPosicaoJuntas(i,:) matrizVelocidadeJuntas(i,:)]));
        # end
        # torque(i,:) = T1+T2+T3
    return [[stellarium_angles, d_stellarium_angles, dd_stellarium_angles], [q, dq, ddq], positions]

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