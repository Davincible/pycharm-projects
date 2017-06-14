import numpy as np
from math import sqrt
import random

first_array = np.array([[1,2,3,4],[2,3,4,'suckadick',9]])
print(first_array)
print(first_array.shape)

second_array = np.arange(0,5)
print(second_array)
third_array = np.eye(5)
print(third_array)
fourth_array = np.diag(third_array)
print(fourth_array)
for item in fourth_array:
    print(item)

print(np.size(fourth_array))
fifth_array = np.array([4,5,6]*75)
print(fifth_array)
size = fifth_array.size
size = sqrt(size)
if size%1 == 0:
    size = int(size)
    fifth_array.resize(size, size)
    print(fifth_array)
else:
    print('Nope')

values = [i for i in range(1000) if (sqrt(i * 3) % 1) == 0]

print(values)

p = np.ones([2,3])
print(p)
print(np.vstack([p, 3*p]))

# for i in range(1000):
#     alpha = (sqrt((i * 3))%1) == 0
#     if alpha:
#         print(i)

list_01 = [1,2,3,4,5]
list_02 = [6,7,8,9,10]

array_01 = np.array([list_01, list_02])

diag_01 = np.diag(array_01)

print(diag_01)

print(len(array_01))
print(np.shape(array_01))
print(sum(array_01))
print(sum(list_01))
print('-------------')
print(array_01.argmax())
print(array_01.max())
print(array_01.argmin())
print('-----------------')
s = (np.arange(13) **2) #squared
print(s[-2:2:-1])
print(s[s > 80])


rand_dict = {i: 0 for i in range(101)}
print(rand_dict)
for count in range(1000):
    randomnumber = random.randint(0, 100)
    rand_dict[randomnumber] = rand_dict[randomnumber] + 1

print(rand_dict)