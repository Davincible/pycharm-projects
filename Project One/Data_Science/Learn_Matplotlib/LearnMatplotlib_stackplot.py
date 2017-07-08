import matplotlib.pyplot as plt

# Stack plots are used when two or more data sets are going to be shown on the same set of axes,
# or you want to break down one data set by their components. And we're interested in the sums.

days = [1,2,3,4,5]

sleeping = [7,8,6,11,7]
eating = [2,3,4,3,2]
working = [7,8,7,2,2]
playing = [8,5,7,8,13]

# Labels, you can't define then directly (maybe in this version you can, haven't checked)
plt.plot([],[],color='m', label='Sleeping', linewidth=3.5)
plt.plot([],[],color='c', label='Eating', linewidth=3.5)
plt.plot([],[],color='r', label='Working', linewidth=3.5)
plt.plot([],[],color='g', label='Playing', linewidth=3.5)

plt.stackplot(days, sleeping,eating,working,playing, colors=['m', 'c', 'r', 'g'])

plt.xlabel('x')
plt.ylabel('y')
plt.title('This is the graph title')
plt.legend()
plt.show()