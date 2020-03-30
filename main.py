
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from matplotlib.patches import Ellipse, Circle


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

points = []
regression_x = np.arange(0, 10, 0.1)

def compute_alpha_beta(points):
    x_values = list(map(lambda point: point[0], points))
    y_values = list(map(lambda point: point[1], points))

    x_mean = np.mean(x_values)
    y_mean = np.mean(y_values)

    alpha = np.sum(list(map(lambda point: (point[0] - x_mean) * (point[1] - y_mean), points))) / np.sum(list(map(lambda point: (point[0] - x_mean)**2, points)))
    beta = y_mean - alpha * x_mean
    return alpha, beta

def linear_regression(alpha, beta, x):
    return alpha + beta * x


def onclick(event):
    circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
    ax.add_artist(circle)
    points.append([event.xdata, event.ydata])

    if len(points) > 1:
        alpha, beta = compute_alpha_beta(points=points)
        regression_curve = list(map(lambda x: (x, linear_regression(alpha, beta, x)), regression_x))
        print(points)
        plt.plot(regression_curve)
    
    fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
# both axes equally scaled
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

