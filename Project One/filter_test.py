from random import random
from time import time
from json import dumps

a = []
time_1 = time()
for i in range(10000):
    a.append({"ID": random(),
                "title": random(),
                "date": random(),
                "abstract": random(),
                "source_url": random(),
                "domain": random(),
                "full_text": random(),
                "category": random(),
                "author": random(),
                "thumbnail_url": random(),
                "dt_format": random()})
time_2 = time()
print("creation time", time_2 - time_1)

time_1 = time()
a.sort(key=lambda x: x["ID"])
time_2 = time()
print("sorting time", time_2 - time_1)

time_1 = time()
filtered = filter(lambda x: x['ID'] < .3, a)
time_2 = time()
print("filter time", time_2 - time_1)

time_1 = time()
listed = list(filtered)
time_2 = time()
print("listing time", time_2 - time_1)
print("list len", len(listed))

b = [{'a': random() * 100, 'b': random() * 100} for i in range(10)]
print("original", dumps(b, indent=4))
c = list(filter(lambda x: x['a'] < 50, b))
# print("orginal filter", dumps(list(c), indent=4))
for item in c:
    print("item:", item)
    item['b'] = 666
    item['c'] = 'new value'
print("new", dumps(b, indent=4))
print("new filter", dumps(list(c), indent=4))
