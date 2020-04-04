
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
ax2.text(2, 95, 'squared',color="red")
ax2.text(2, 90, 'absolute',color="green")
plt.gca().set_aspect('equal', adjustable='box')



regression_x = np.linspace(0, 10, 100)

class LinearRegression:
    def __init__(self):
        self.alpha = 0
        self.beta = 0
        self.points = []

    def linear_regression(self, x):
        # compute alpha and beta
        self.x_values = list(map(lambda point: point[0], self.points))
        self.y_values = list(map(lambda point: point[1], self.points))

        self.x_mean = np.mean(self.x_values)
        self.y_mean = np.mean(self.y_values)
        
        Sxy = np.sum(list(map(lambda point: (point[0] - self.x_mean) * (point[1] - self.y_mean), self.points)))
        Sxx = np.sum(list(map(lambda point: (point[0] - self.x_mean) * (point[0] - self.x_mean), self.points)))

        self.beta = Sxy / Sxx
        self.alpha = self.y_mean - self.beta * self.x_mean

        # apply regression function to x using computed alpha and beta
        return self.alpha + self.beta * x

    def get_squared_error(self):
        return np.sum(list(map(lambda point: (point[1] - self.linear_regression(point[0]))**2, self.points))) 

    def get_absolute_error(self):
        return np.sum(list(map(lambda point: np.abs(point[1] - self.linear_regression(point[0])), self.points))) 


class Index:
    def __init__(self):
        self.lin_reg = LinearRegression()
        self.regression_curve, = ax1.plot([], [], 'b-')

        self.squared_error_y = [0]
        self.squared_error_graph,  = ax2.plot(self.squared_error_y, [0], 'r-')

        self.absolute_error_y = [0]
        self.absolute_error_graph,  = ax2.plot(self.absolute_error_y, [0], 'g-')


    def onclick(self, event):
        if event.xdata is None or event.ydata is None or not ax1 is event.inaxes:
            return 
        # save and draw new point
        circle = plt.Circle((event.xdata, event.ydata), 0.1,  color='b')
        ax1.add_artist(circle)
        self.lin_reg.points.append((event.xdata, event.ydata))
        fig.canvas.draw()

        # plot graphs
        if len(self.lin_reg.points) > 1:
            # upadte regression curve
            self.regression_curve.set_xdata(regression_x)
            self.regression_curve.set_ydata(list(map(lambda x: self.lin_reg.linear_regression(x), regression_x)))

            # update squared error graph
            self.squared_error_graph.set_xdata(list(range(len(self.lin_reg.points))))
            self.squared_error_y.append(self.lin_reg.get_squared_error())
            self.squared_error_graph.set_ydata(self.squared_error_y)

            # update absolute error graph
            self.absolute_error_graph.set_xdata(list(range(len(self.lin_reg.points))))
            self.absolute_error_y.append(self.lin_reg.get_absolute_error())
            self.absolute_error_graph.set_ydata(self.absolute_error_y)

        
    def clear(self, event):
        # remove points
        self.lin_reg.points.clear()

        # remove artists
        ax1.artists = []        

        # reset regression curve
        self.regression_curve.set_xdata([])
        self.regression_curve.set_ydata([])

        # reset error graphs
        self.squared_error_y = [0]
        self.squared_error_graph.set_xdata([0])
        self.squared_error_graph.set_ydata([0])
        self.absolute_error_y = [0]
        self.absolute_error_graph.set_xdata([0])
        self.absolute_error_graph.set_ydata([0])



callback = Index()

# add onClick event
cid = fig.canvas.mpl_connect('button_press_event', callback.onclick)

# button widget
clear_button_sizes = plt.axes([0.05, 0.90, 0.1, 0.075])
clear_button = Button(clear_button_sizes, "clear")
clear_button.on_clicked(callback.clear)

plt.show()