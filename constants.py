from sympy import *
from numpy import pi
from sympy.core.symbol import Symbol

l1 = 0.5
l2 = 0.8
time_for_each_moviment = 3
steps = 15
#zenith
q1_limit = [-2*pi, 2*pi]
q2_limit = [-pi/4, pi/2]
az_limit = [0, 2*pi]
al_limit = [0, 2*pi]
initial_position = [0.0, atan(l1/l2)]
initial_q_position = [0, 0]
max_tolerated_imaginary = 0.00001
# this key belongs to stellarium json response for the current location. If you change the language of stellarium you also need to change this variable here.
az_alt_key = "Az./Alt.:"
robot_structure = {
    "l1": [0, 0, Symbol('l1'), 1],
    "l2": [Symbol('l2'), 0, 0, 1]
}