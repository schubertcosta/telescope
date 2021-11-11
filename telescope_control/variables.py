from sympy.core.symbol import Symbol


def get_robot_variables():
    return {
        "l1": [0, 0, Symbol('l1'), 1],
        "l2": [Symbol('l2'), 0, 0, 1]
    }