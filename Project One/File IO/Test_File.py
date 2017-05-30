import pandas as pd

list_one = [ 'America', 'The Great Republic of Brouwer', 'India', 'Japan', 'Holy Land', 'China', 'HOOKED' ]
list_two = [ 'Guns', 'GAME', 'Tech support', 'Samurai', 'Tricking', 'Split eyes', 'Brothers']
list_three = list_one.copy()
list_four = [5,6,47,89,55,666,24]

series_test_01 = pd.Series(list_two, index=list_one)
print(series_test_01)

print('\n--------------------------------------------\n')

list_one.append('another Gathering')
list_two.append('hey')
series_test_02 = pd.Series(list_two, index=list_one)

print(pd.Series(list_four))

print('\n--------------------------------------------\n')

print(series_test_02)

