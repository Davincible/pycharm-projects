import urllib3
import json
import time
from fake_useragent import UserAgent
from random import randint
import certifi
import datetime

def fetchPreMarket(url):
    wrong_request = b'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n[an error occurred while processing the directive]\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    Headers = {'User-Agent': None}
    header_list = ['firefox', 'internetexplorer', 'safari', 'chrome', 'opera']
    useragent = UserAgent()
    try:
        browser_index = randint(0, len(header_list) - 1)
        browser = header_list[browser_index]
        header_index = randint(0, len(useragent.data_browsers[browser]) - 1)
        Headers['User-Agent'] = useragent.data_browsers[browser][header_index]
    except IndexError:
        try:
            print("Index Error:", header_index)
        except UnboundLocalError:
            print("Index Error:", browser_index)

    link = url
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    try:
        print(time.time())
        start = time.time()
        connection = pm.request('GET', link, headers=Headers)
        raw_data = connection.data
        end = time.time()
        if raw_data == wrong_request:
            print("Please check your input url, invalid request")
            exit(1)
        print(raw_data)
        print('time passed:', end - start)
        try:
            data = json.loads(raw_data, encoding='UTF-8')
        except json.decoder.JSONDecodeError:
            data = json.loads(raw_data[3:])

        if isinstance(data, type(list())):
            info = data[0]
            for item in info:
                print(item, ' | ', time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(str(info[item])[:10]))) if str(item) == 'time' else info[item])
        elif isinstance(data, type(dict())):
            info = data
            for item in info:
                print(item, ' | ', datetime.datetime.fromtimestamp(info[item]).strftime('%c') if str(item) == 'time' else info[item], 'not time')
        else:
            info = data
            print(info)
        print('----------------------------------------------------------------')



    except KeyError:
        raise KeyError


url = 'https://finance.google.com/finance?infotype=infoquoteall&q=NASDAQ:MNKD'
url2 = 'https://finance.google.com/finance?q=MNKD&output=json'
url3 = 'https://api.iextrading.com/1.0/stock/mnkd/open-close'
url4 = 'https://api.iextrading.com/1.0/stock/mnkd/price'
url5 = 'https://api.iextrading.com/1.0/tops/last?symbols=mnkd'
url6 = 'https://api.iextrading.com/1.0/stock/mnkd/quote'
url7 = 'https://api.iextrading.com/1.0/stock/market/list/gainers'
url8 = 'https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,tsla&types=symbol,latestPrice,latestSource,latestUpdate,latestVolume,previousClose'
url9 = 'https://api.iextrading.com/1.0/stock/tsla/batch?types=symbol,latestPrice,latestSource,latestUpdate,latestVolume,previousClose'
url10 = 'https://api.iextrading.com/1.0/stock/market/batch?symbols=aapl,tsla&types=quote&filter=symbol,latestPrice,latestSource,latestUpdate,latestVolume,previousClose'

for i in range(100):
    # fetchPreMarket(url6)
    fetchPreMarket(url3)
    time.sleep(5)