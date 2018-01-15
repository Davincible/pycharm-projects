import pandas as pd
from os import walk
from xmljson import badgerfish as bf
from xmljson import yahoo as yh
from xml.etree.ElementTree import fromstring, parse
from json import dumps, loads

firstdata_filelist = list(walk('data_01'))[0][2]

first_file = firstdata_filelist[0]
with open('data_01/{}'.format(first_file)) as file_xml:
    first_file_data = file_xml.read()
parsed_data = bf.data(fromstring(first_file_data))
yahoo_data = dumps(yh.data(fromstring(first_file_data)))
first_file_json = dumps(parsed_data, indent=4)

# print(dict(parsed_data))

# keys = list(dict(parsed_data).keys())
firstdata_dict = dict(parsed_data)
firstdata_series = pd.read_json(yahoo_data)
firstdata_series.to_excel('first_data.xlsx')
print(firstdata_series)
# print(dict(parse('data_01/{}'.format(first_file))))
# while keys:
#     for key in keys:
#