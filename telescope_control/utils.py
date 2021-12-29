from sympy import *
import numpy as np

def rotate_matrix(axis, q):
    switcher = {
        'x': Matrix([\
                [1, 0, 0, 0],
                [0, cos(q), -sin(q), 0],
                [0, sin(q), cos(q), 0],
                [0, 0, 0, 1]]),
        'y': Matrix([\
                [cos(q), 0, sin(q), 0],
                [0, 1, 0, 0],
                [-sin(q), 0, cos(q), 0],
                [0, 0, 0, 1]]),
        'z': Matrix([\
                [cos(q), -sin(q), 0, 0],
                [sin(q), cos(q), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    }
    return switcher.get(axis, "Invalid axis")        

def position_matrix(position):
    return Matrix(\
        [[1, 0, 0, 0],
        [0, 1, 0, 0], 
        [0, 0, 1, 0],
        position]).T

def get_parametrization(previous_position, next_position, time_for_each_moviment, steps):
    position = []
    d_position = []
    dd_position = []

    for t in np.linspace(0, time_for_each_moviment, num = steps):
        k0 = previous_position
        k1 = 0
        k2 = 3*np.subtract(next_position,previous_position)/time_for_each_moviment**2
        k3 = -2*np.subtract(next_position,previous_position)/time_for_each_moviment**3
        position.append(k0 + k1*t + k2*t**2 + k3*t**3)        
        d_position.append(k1 + 2*k2*t + 3*k3*t**2)
        dd_position.append(2*k2 + 6*k3*t)
    return position, d_position, dd_position

def calculate_energy(m, dPg, II, Pg, g):
    dPg_03_arr = np.array(dPg[0:3])
    dPg_36_arr = np.array(dPg[3:6])
    knetic_energy = 0.5*m*np.matmul(dPg_03_arr.T, dPg_03_arr) + 0.5*np.matmul(dPg_36_arr.T, np.matmul(II, dPg_36_arr))
    potential_energy = -m*np.matmul(np.array(g).T, np.array(Pg[0:3]))
    return knetic_energy - potential_energy

def gradient(expr, vector):
    grad = []
    for i in range(len(vector)):
        grad.append(diff(expr, vector[i]))
    return grad
