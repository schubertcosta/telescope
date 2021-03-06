from sympy import *
from numpy import pi
from sympy.core.symbol import Symbol

l1 = 0.5
l2 = 0.8
time_for_each_moviment = 3
steps = 15
q1_limit = [-2*pi, 2*pi]
q2_limit = [-pi/4, pi/2]
az_limit = [0, 2*pi]
al_limit = [0, pi]
initial_position = [0.0, atan(l1/l2)]
initial_q_position = [0, 0]
initial_xyz_position = [l2, 0, l1]
max_tolerated_imaginary = 0.00001
# this key belongs to stellarium json response for the current location. If you change the language of stellarium you also need to change this variable here.
az_alt_key = "Az./Alt.:"
robot_structure = {
    "l1": [0, 0, Symbol('l1'), 1],
    "l2": [Symbol('l2'), 0, 0, 1]
}
freecad_mounting = "G:\\Meu Drive\\Projetos\\Telescopio\\CAD\\First version1\\monting.FCStd"
freecad_path = 'C:/Program Files/FreeCAD 0.19/bin/' # path to your FreeCAD.so or FreeCAD.dll file
stelarium_uri = "http://localhost:8090/api/"

# Parameters relate with the center of mass of the telescope
# we are using PLA
g0 = [0, 0, -9.80665]
mi = 0.5*eye(2); # friction steel x PLA
mass_matrix = [4.33506, 2.41293]

Pg11 = Matrix([0, 0, -0.17468, 1])
II11 = Matrix([[0.19413, 0, 0], [0, 0.016470, 0], [0, 0, 0.05770]])

Pg22 = Matrix([-0.06774, 0, 0, 1])
II22 = Matrix([[0.01757, 0, 0], [0, 0.06109, 0], [0, 0, 0.06803]])

II = [II11, II22]