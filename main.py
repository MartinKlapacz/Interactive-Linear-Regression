
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from matplotlib.patches import Ellipse, Circle
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
regression_x = np.linspace(0, 10, 100)
cursor = Cursor(ax,horizOn=True,vertOn=True,color='green',linewidth=1.0)

class LinearRegression:
    def compute_alpha_and_beta(self, points):
        x_values = list(map(lambda point: point[0], points))
        y_values = list(map(lambda point: point[1], points))

        x_mean = np.mean(x_values)
        y_mean = np.mean(y_values)
        
        Sxy = np.sum(list(map(lambda point: (point[0] - x_mean) * (point[1] - y_mean), points)))
        Sxx = np.sum(list(map(lambda point: (point[0] - x_mean) * (point[0] - x_mean), points)))

        beta = Sxy / Sxx
        alpha = y_mean - beta * x_mean

        return alpha, beta

    def linear_regression(self, alpha, beta, x):
        return alpha + beta * x

class Index:
    def __init__(self):
        self.lin_reg = LinearRegression()
        self.points = []
        self.graph, = plt.plot([], [])

    def onclick(self, event):
        # save and draw new point
        circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
        ax.add_artist(circle)
        self.points.append((event.xdata, event.ydata))
        fig.canvas.draw()

        # regression curve
        if len(self.points) > 1:
            alpha, beta = self.lin_reg.compute_alpha_and_beta(points=self.points)
            self.graph.set_xdata(regression_x)
            self.graph.set_ydata(list(map(lambda x: self.lin_reg.linear_regression(alpha, beta, x), regression_x)))
        
    def clear(self, event):
        pass


callback = Index()
# add onClick event
cid = fig.canvas.mpl_connect('button_press_event', callback.onclick)
# both axes equally scaled
plt.gca().set_aspect('equal', adjustable='box')

plt.show()