import time
import datetime
import numpy as np
import pandas as pd

def calctime(a = float):
    time_a = time.time()
    time.sleep(a)
    time_b = time.time()
    timepassed = time_b - time_a
    calculated = timepassed - a
    print(datetime.datetime.fromtimestamp(time_a))
    return timepassed, calculated

print(calctime(0.1))

#dt = datetime.datetime.date()
#print(dt)
print('----------------------------\n')
time_now = time.time()
time_later = datetime.timedelta(days=100)
date_now = datetime.datetime.fromtimestamp(time_now)
print("The date right now is: ", date_now)
print("the date in 100 days will be: ",date_now + time_later)
print('----------------------------\n')

store1 = [10.00, 11.00, 12.34, 2.34, 5.23]
store2 = [9.00, 11.10, 12.34, 2.01, 1.56, 88]
cheapest = map(max, store1, store2)
for item in cheapest:
    print(item)

def printend(a):
    print("We're done here", a)

print('----------------------------\n')

# list_one = [None for element in range(100)]
# print(list_one)
# print(len(list_one))
# list_one = ['One' for i in range(len(list_one))]
# print(list_one)
# print(len(list_one))

end = printend("I'm outta here")
end

a = np.eye(6)
b = pd.DataFrame(a)
print("a id:", b)

column_list = ['one', 'two', 'three', 'four', 'five', 'six']

print(b.rename(columns=dict(zip([i for i in range(6)], column_list))))

for i in range(2):
    b = b.reset_index()
    print(b)
