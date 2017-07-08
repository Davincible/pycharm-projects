import matplotlib.pyplot as plt

# Where stackplots show how variables over time,
# a pie chart shows the distribution of the variables in one moment of time.

days = [1,2,3,4,5]

sleeping = [7,8,6,11,7]
eating = [2,3,4,3,2]
working = [7,8,7,2,2]
playing = [8,5,7,8,13]

slices = [7,2,2,13]
activities = ['sleeping', 'eating', 'working', 'playing']
cols = ['c', 'm', 'r', 'b']

plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=90,
        explode=(0.1,0.35,0.1,0.1),  # let the elements explode away from the center of the pie
        shadow=True,                 # set a light shadow
        autopct='%1.1f%%'            # calculate the percentage of each element
        )

# plt.xlabel('x')
# plt.ylabel('y')
plt.title('This is the graph title')
# plt.legend()
plt.show()