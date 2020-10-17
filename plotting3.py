import random
from itertools import count

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(5,5))

x,y = [], []
index= count()
def animate(i):
    x.append(next(index))
    y.append(random.randint(2,20))
    plt.style.use("ggplot")
    plt.plot(x,y, color = 'red')

ani = FuncAnimation(fig, animate, interval=300)
plt.show()
