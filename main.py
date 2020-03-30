
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from matplotlib.patches import Ellipse, Circle


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
regression_x = np.linspace(0, 10, 100)

points = []

cursor = Cursor(ax,
    horizOn=True,
    vertOn=True,
    color='green',
    linewidth=1.0)

def compute_alpha_beta(points):
    x_values = list(map(lambda point: point[0], points))
    y_values = list(map(lambda point: point[1], points))

    x_mean = np.mean(x_values)
    y_mean = np.mean(y_values)
    
    Sxy = np.sum(list(map(lambda point: (point[0] - x_mean) * (point[1] - y_mean), points)))
    Sxx = np.sum(list(map(lambda point: (point[0] - x_mean) * (point[0] - x_mean), points)))

    beta = Sxy / Sxx
    alpha = y_mean - beta * x_mean

    return alpha, beta

def linear_regression(alpha, beta, x):
    return alpha + beta * x


def onclick(event):
    circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
    ax.add_artist(circle)
    points.append((event.xdata, event.ydata))

    if len(points) > 1:
        alpha, beta = compute_alpha_beta(points=points)
        line = plt.plot(regression_x, list(map(lambda x: linear_regression(alpha, beta, x), regression_x)), linestyle='-')    
    fig.canvas.draw()


cid = fig.canvas.mpl_connect('button_press_event', onclick)

# both axes equally scaled
plt.gca().set_aspect('equal', adjustable='box')

plt.show()

