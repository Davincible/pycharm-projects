import matplotlib.pyplot as plt


# here it is easy to spead the data set into groups aka bins, to get a proper overview of the data set.
# A histogram is a frequece distribution. 
population_ages = [1,23,13,123,100,12,24,55,58,85,65,35,85,45,95,22,66,47,85,10,102,120,129,130]
#ids = [x for x in range(len(population_ages))]

bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]

plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)


plt.xlabel('x')
plt.ylabel('y')
plt.title('This is the graph title')
plt.legend()
plt.show()
