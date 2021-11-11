import numpy as np
import constants
import matplotlib.pyplot as plt

def plot_chart(coordinates):
    x = (list(map(lambda x: x[0], coordinates)))
    y = (list(map(lambda y: y[1], coordinates)))
    z = (list(map(lambda z: z[2], coordinates)))
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-constants.l2*1.2, constants.l2*1.2)
    ax.set_ylim3d(-constants.l2*1.2, constants.l2*1.2)
    ax.set_zlim3d(0, constants.l1 + constants.l2)
    ax = set_quiver(ax)
    ax.plot(x, y, z, '.')
    plt.title("Position of the tip of the telescope", loc="center")
    plt.show()

def set_quiver(ax):
    x, y, z = np.array([[0,0,0],[0,0,0],[0,0,0]])
    u, v, w = np.array([[1,0,0],[0,1,0],[0,0,1]])
    ax.quiver(x,y,z,u,v,w,arrow_length_ratio=0.1, color="black")
    return ax

# how to implement live chart plot
# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib
#     import matplotlib.pyplot as plt
# import numpy

# hl, = plt.plot([], [])

# def update_line(hl, new_data):
#     hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
#     hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
#     plt.draw()