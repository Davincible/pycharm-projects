import json

# with open('a_test_file.json', 'w') as file:
#     pass
sample = ['hello', 'this', 'is', 'a', 'list']
dict_ = {"Company": '?',
                   "HQ_location": '?',
                   "Full_Name": '?',
                   "Role": '?',
                   "Email": '?',
                   "Phone": '?',
                   "Company_Type": [],
                   "Listing": '?',
                   "TimeStamp": '?',
                   "Partnership_Type": {"in-licensing": False,
                                       "out-licensing": False,
                                       "distribution": False,
                                       "M&A": False,
                                       "financing": False},
                   "Drug_Data": {"in-licensing": [],
                                 "out-licensing": [],
                                 "distribution": [],
                                 "M&A": [],
                                 "financing": []}}

with open('a_test________.json', 'w') as file_:
    pass
    # file_.write(json.dumps(dict_))


with open('a_test________.json', 'r') as file:
    data = json.loads(file.read())
    print(data)
    if 'Company' in data:
        print(True)
    for item in data:
        print(item)


