from urllib.request import urlopen as op
import urllib

url = 'http://www.nu.nl'
url2 = 'http://pythonprogramming.net'

values =    {'s': 'basic',
             'submit': 'search'}

connection = op(url)
raw_data = connection.read()
connection.close()

data = urllib.parse.urlencode(values)
print('before utf-8 encoding: ', data)
data = data.encode('utf-8')
print('data after utf-8 encoding: ', data)
request = urllib.request.Request(url2, data)

resp = urllib.request.urlopen(request)
print(resp.read())
resp.close()

print('------------')
another = op(url2, data)
print(another.read())