"""""
example file how FuncAnimation works
"""

from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
import time

x_data, y_data, z_data = [], [], []

figure, ax = pyplot.subplots()
line1, = pyplot.plot(x_data, y_data,'r--o')
line2, = pyplot.plot(x_data, z_data,'b*--')

def update(frame):
    x_data.append(datetime.now())
    y_data.append(randrange(0, 100))
    z_data.append(randrange(0, 100))
    line1.set_data(x_data, y_data)
    line2.set_data(x_data, z_data)
    pyplot.style.use("ggplot")
    # pyplot.plot(x_data, y_data, color = 'red')
    # pyplot.plot(x_data, z_data, color = 'yellow')
    pyplot.plot(x_data, y_data,'r--o')
    pyplot.plot(x_data, z_data, 'b*--')
    figure.gca().relim()
    figure.gca().autoscale_view()
    return [line1, line2]


animation = FuncAnimation(figure, update, interval=1000)

pyplot.show()
