from sympy import *
def get_constants():
    l1 = 0.5
    l2 = 0.8
    time_for_each_moviment = 3
    steps = 10
    #zenith
    current_position = [0, atan(l1/l2)]
    return [l1, l2, time_for_each_moviment, steps, current_position]