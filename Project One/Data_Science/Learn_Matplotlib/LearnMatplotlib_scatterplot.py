import matplotlib.pyplot as plt


# A scatter plot is used to give an overview of the relations between different variables.

x = [1,2,3,4,5,6,7,8]
y = [5,2,4,2,1,4,5,2]

plt.scatter(x,y, label="A  scatter plot", color='blue', marker='x', s=30)

plt.xlabel('x')
plt.ylabel('y')
plt.title('This is the graph title')
plt.legend()
plt.show()