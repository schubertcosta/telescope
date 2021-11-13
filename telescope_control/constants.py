from sympy import *
from numpy import pi

l1 = 0.5
l2 = 0.8
time_for_each_moviment = 3
steps = 10
#zenith
q1_limit = [0.0, 2*pi]
# Limit pi/2 chose to keep always the value of Az = q1 true
q2_limit = [-pi/4, pi/2]
initial_position = [0.0, atan(l1/l2)]
max_tolerated_imaginary = 0.00001