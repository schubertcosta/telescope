
from sympy import *
import sys
sys.path.insert(1, '../telescope')
sys.path.insert(1, '../charts')
sys.path.insert(1, './telescope_control')
import utils
import constants
# import numpy as np
# from numpy import pi
# from sympy.vector import gradient

# # Calculating Transformations for the robot
robot  = constants.robot_structure
# Azs = Symbol('Az')

qs = symbols('q1:3')
# dqs = Matrix(symbols('dq1:3'))
# R10 = utils.rotate_matrix('z', qs[0])
# D10 = utils.position_matrix(robot["l1"])
# T10 = R10*D10

# # # Calculating equation for q1 and q2
# l1s = robot["l1"][2]

# q1s = [Azs]

# # Cinematic and Dinamic parameters
# Pg10 = T10*constants.Pg11
# JL10 = Pg10[0:3,0].jacobian([qs[0]])
# JA10 = T10[0:3,2]
# dPg10 = Matrix([JL10, JA10])*dqs[0]

# II10 = T10[0:3,0:3]*constants.II11*(T10[0:3,0:3].T)

# JLA = Matrix(BlockMatrix([[JL10], [JA10]]))

# # pprint(JLA)
# dJL = (JL10[0:3,0].jacobian([qs[0]]))*dqs[0]
# dJA = (JA10[0:3,0].jacobian([qs[0]]))*dqs[0]
# dJLA = Matrix(BlockMatrix([[dJL], [dJA]]))


# # # Calculating system energy
# # Pg = [Pg10, Pg20]
# # dPg = [dPg10, dPg20]

# # pprint([constants.mass_matrix[0], dPg10, II10, Pg10, constants.g0])

# L = 0
# L += utils.calculate_energy(constants.mass_matrix[0], dPg10, II10, Pg10, constants.g0)
# dLdqp = utils.gradient(L, [dqs[0]])
# dLdq = utils.gradient(L, [qs[0]])

# dEddqp = 0.5*dqs[0]

# t = symbols('t')
# q_L = Function(qs[0])(t)
# dq_L = diff(q_L, t)
# ddq_L = diff(dq_L, t)
# ddLdqpdt = diff(Matrix(dLdqp).subs([(qs[0], q_L),(dqs[0], dq_L)]), t)

# # pprint(ddLdqpdt.subs([(ddq_L, 1)]))
# # quit()
# # That is the telescope last position
# last_position = constants.initial_position
# last_q_position = constants.initial_q_position
# last_xyz_position = constants.initial_xyz_position

# def calculate_parameters(az):

#     [stellarium_angles, d_stellarium_angles, dd_stellarium_angles] =  utils.get_fifth_order_parametrization(0, az, constants.time_for_each_moviment, constants.steps)
# #     positions = []
#     q, dq, ddq, torque = [[],[],[], []]

#     for index, next_intermediate_angle in enumerate(stellarium_angles):
#         q1 = next_intermediate_angle
#         q.append(q1)
        
#         ## Calculating velocity
#         V_ref_0 = [0, 0, d_stellarium_angles[index][0]]
#         V = np.array([0.0, 0.0, 0.0, V_ref_0[0], V_ref_0[1], V_ref_0[2]])
#         JLAnum = np.array(JLA.subs([(l1s, constants.l1), (qs[0], q1)]))
#         dqnum = np.matmul((JLAnum.T), V)
#         dq.append(dqnum)
        
#         # # Calculating acceleration
#         # A_ref_0 = [0, 0, dd_stellarium_angles[index][0]]
#         # A = np.array([0.0, 0.0, 0.0, A_ref_0[0], A_ref_0[1], A_ref_0[2]])
#         # dJLAnum = dJLA
#         # ddq_dem = np.subtract(A, np.matmul(dJLAnum, dqnum))
#         # ddqnum = np.matmul((JLAnum.T), ddq_dem)
#         # ddq.append(ddqnum)

#         # # Calculating torques
#         # T1 = ddLdqpdt.subs([(ddq_L, ddqnum[0])])
#         T2 = -Matrix(dLdq).subs([(qs[0], q1), (dqs[0], dqnum[0])])
#         # T3 = Matrix([dEddqp]).subs([(dqs[0], dqnum[0])])

#         pprint(T2)
#         # TN =      
#         # torque.append(TN)

# #         T2 = -Matrix(dLdq).subs([(l1s, constants.l1), (qs[0], q1), (dqs[0], dqnum[0])])
# #         pprint(T2[0])
    
#     # pprint(ddq)
#     quit()
# #     return [[stellarium_angles, d_stellarium_angles, dd_stellarium_angles], [q, dq, ddq, torque], positions]

# def verify_route(angle, range):
#     if angle >= range[0] and angle <= range[1]:
#         return True
#     return False

# def get_faster_route(angles, last_position):
#     min = 2*pi
#     shortest_angle = last_position
#     for current_angle in angles:
#         if abs(current_angle-last_position) <= min:
#             min = abs(current_angle-last_position)
#             shortest_angle = current_angle
#     return shortest_angle

# def get_best_q(qs_array, sub_params, range, q_number, last_position):
#     q_array = [qs.subs(sub_params) for qs in qs_array]
#     q_candidate_array = []

#     for q in q_array:
#         if im(q) >= constants.max_tolerated_imaginary:
#             print("q%d contains a complex number, q%d = %s" % (q_number, q_number, q))
#             continue

#         if im(q):
#             q = re(q)
        
#         if q >= range[0] and q <= range[1]:
#             q_candidate_array.append(q)
    
#     if len(q_candidate_array) == 0:
#         print("All candidates for q%d are out of range" % (q_number))
#         raise ValueError("Error - q%d out of range. q_array -> %s" % (q_number, q_array))

#     return get_faster_route(q_candidate_array, last_position) 

# if __name__ == '__main__':
#     calculate_parameters(2*pi)


Als = Symbol('Al')


R21 = utils.rotate_matrix('y', -qs[1])
D21 = utils.position_matrix(robot["l2"])
T21 = R21*D21

# Calculating rotation in y axis
R32 = utils.rotate_matrix('y', -(Als - qs[1]))
D32 = utils.position_matrix([0, 0, 0, 1])
T32 = R32*D32

T31 = T21*T32




pprint(T31.subs([(Als, qs[1])]))

pprint(T21)


doc = App.open("C:\\telescope\\CAD\\v1\\mounting.FCStd")
doc.base.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(-30,0,0), App.Vector(0,0,0))




serialString = ""                           # Used to hold data coming over UART
    # # Wait until there is data waiting in the serial buffer
    # if(serialPort.in_waiting > 0):

    #     # Read data out of the buffer until a carraige return / new line is found
    #     serialString = serialPort.readline()

    #     # Print the contents of the serial data
    #     print(serialString.decode('Ascii'))

    #     # Tell the device connected over the serial port that we recevied the data!
    #     # The b at the beginning is used to indicate bytes!
    #     serialPort.write(b"Thank you for sending data \r\n")


     char* cstr = new char[data_received.length() +1]; 
      strcpy(cstr, data_received.c_str()); 