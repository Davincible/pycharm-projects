from fake_useragent import UserAgent

ua = UserAgent()
print(ua.data.keys())
for item in dir(ua):
    if item[0] is not '_':

        if callable(getattr(ua, item)):
            print('CALLABLE:', item, end=', ')
        else:
            print(item, end=', ')
print()
print(len(ua.data_randomize), ua.data_randomize)
print(ua.data_browsers.keys())
for key in ua.data_browsers.keys():
    print(key, 'has %d items' % len(ua.data_browsers[key]))
print(ua.data_browsers.get(2))
