from random import randint

store1 = {'store1': (randint(1,1000) for x in range(10))}
store2 = {'store2': (randint(1,1000) for x in range(10))}
store3 = [randint(1,1000) for x in range(10)]

new = map(min, store1, store2)
type(new)
for item in new:
    print(item)

min_store1 = min(store1)
min_store2 = min(store2)
min_store3 = min(store3)

min_dict = {'store1': min(store1), 'store2': min(store2), 'store3': min(store3)}

best = min(min_dict)
print(best)
