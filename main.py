
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from matplotlib.patches import Ellipse, Circle
import numpy as np


fig = plt.figure()

ax1 = fig.add_subplot(1, 2, 1)
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])
ax1.set_title("regression curve")
plt.gca().set_aspect('equal', adjustable='box')


ax2 = fig.add_subplot(1, 2, 2)
ax2.set_xlim([0, 60])
ax2.set_ylim([0, 100])
ax2.set_title("error curve")
ax2.set_xlabel("number of points")
plt.gca().set_aspect('equal', adjustable='box')



regression_x = np.linspace(0, 10, 100)
cursor = Cursor(ax1,horizOn=True,vertOn=True,color='green',linewidth=1.0)

class LinearRegression:

    def __init__(self):
        self.alpha = 0
        self.beta = 0
        self.points = []

    def compute_alpha_and_beta(self, points):
        self.points = points
        self.x_values = list(map(lambda point: point[0], points))
        self.y_values = list(map(lambda point: point[1], points))

        self.x_mean = np.mean(self.x_values)
        self.y_mean = np.mean(self.y_values)
        
        Sxy = np.sum(list(map(lambda point: (point[0] - self.x_mean) * (point[1] - self.y_mean), points)))
        Sxx = np.sum(list(map(lambda point: (point[0] - self.x_mean) * (point[0] - self.x_mean), points)))

        self.beta = Sxy / Sxx
        self.alpha = self.y_mean - self.beta * self.x_mean

    def linear_regression(self, x):
        return self.alpha + self.beta * x

    def get_squared_error(self):
        return np.sum(list(map(lambda point: (point[1] - self.linear_regression(point[0]))**2, self.points))) 

    def get_absolute_error(self):
        return np.sum(list(map(lambda point: np.abs(point[1] - self.linear_regression(point[0])), self.points))) 


class Index:
    def __init__(self):
        self.lin_reg = LinearRegression()
        self.points = []
        self.regression_curve, = ax1.plot([], [], 'b-')
        self.error_y = [0]
        self.error_graph,  = ax2.plot(self.error_y, [0], 'r-')

    def onclick(self, event):
        if event.xdata is None or event.ydata is None or not ax1 is event.inaxes:
            return 
        # save and draw new point
        circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
        ax1.add_artist(circle)
        self.points.append((event.xdata, event.ydata))
        fig.canvas.draw()

        # regression curve
        if len(self.points) > 1:
            self.lin_reg.compute_alpha_and_beta(points=self.points)

            self.regression_curve.set_xdata(regression_x)
            self.regression_curve.set_ydata(list(map(lambda x: self.lin_reg.linear_regression(x), regression_x)))

            # maybe this should be better solved
            self.error_graph.set_xdata(list(range(len(self.points))))
            self.error_y.append(self.lin_reg.get_squared_error())
            self.error_graph.set_ydata(self.error_y)
            print(event.inaxes)
            print(ax1)
            print(event.inaxes is ax1)
        
    def clear(self, event):
        pass


callback = Index()
# add onClick event
cid = fig.canvas.mpl_connect('button_press_event', callback.onclick)

plt.show()