def get_constants():
    l1 = 0.5
    l2 = 0.8
    time_for_each_moviment = 3
    steps = 10
    previous_position = [l2, 0, l1]
    #zenith
    current_position = [0,0,0]
    return [l1, l2, time_for_each_moviment, steps, previous_position, current_position]