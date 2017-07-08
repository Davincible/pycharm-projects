import matplotlib.pyplot as plt


# here you just show the raw data of all the ages, does not give a good overview of the spread.
population_ages = [1,23,13,123,100,12,24,55,58,85,65,35,85,45,95,22,66,47,85,10,102,120,129,130]
ids = [x for x in range(len(population_ages))]

plt.bar(ids, population_ages, label='population ages', color='green')

plt.xlabel('x')
plt.ylabel('y')
plt.title('This is the graph title')
plt.legend()
plt.show()
