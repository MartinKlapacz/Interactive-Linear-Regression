
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from matplotlib.patches import Ellipse, Circle


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

points = []

def onclick(event):
    circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
    ax.add_artist(circle)
    points.append(((event.xdata, event.ydata)))
    fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
# both axes equally scaled
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

