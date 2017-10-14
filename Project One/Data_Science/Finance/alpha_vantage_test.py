from alpha_vantage.timeseries import TimeSeries
from time import time

api_key = '1R4FFRPW6IJZZPL8'
ticker = 'mnkd'
interval = '1min'
total_list = []
ts = TimeSeries(key=api_key, output_format='pandas')
ta = TimeSeries(key=api_key)

startstart = time()
for i in range(100):
    start = time()
    data, meta_data = ts.get_intraday(symbol=ticker, interval=interval, outputsize='full')
    end = time()
    total_list.append(end - start)
    print('finished iteration %d of pandas' % i)
    print(data)
total = 0
for item in total_list:
    total += item
total /= len(total_list)

total_list_ = []
for x in range(100):
    start_ = time()
    data_, meta_data_ = ts.get_intraday(symbol=ticker, interval=interval)
    end_ = time()
    total_list_.append(end_ - start_)
    print('finished iteration %d of json' % x)
total_ = 0
for item in total_list_:
    total_ += item
total_ /= len(total_list_)
endend = time()

print('average for pandas:', total, 'max:', max(total_list), 'min:', min(total_list))
print('average for json', total_, 'max:', max(total_list_), 'min:', min(total_list_))
print('total time:', endend - startstart)