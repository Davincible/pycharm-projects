from yahoo_finance import Share
from rtstock.stock import Stock
from googlefinance import getQuotes
import json

Stock_One = 'tsla'

# Get the Data from rtstock
rtstock_stock = Stock(Stock_One)
rtstock_latestprice = rtstock_stock.get_latest_price()
print("rtstock returns this value:", rtstock_latestprice)

# Get the stock Data from yahoo_finance VERY EXTENSIVE
yahooofinance_stock = Share(Stock_One)
yahooofinance_latestprice = yahooofinance_stock.get_price()
yahooofinance_tradetime = yahooofinance_stock.get_trade_datetime()
yahooofinance_anotherfunction = yahooofinance_stock.get_last_trade_with_time()
print('Yahoo finance retuns:', yahooofinance_latestprice, 'on the time:', yahooofinance_tradetime, 'AND IT RETURNS:',yahooofinance_anotherfunction)

# Get the stock Data from GoogleFinance WORKS REAL TIME, THE OTHERS DONT
# print('The Google Finance module returns:', json.dumps(getQuotes(Stock_One), indent=2))
