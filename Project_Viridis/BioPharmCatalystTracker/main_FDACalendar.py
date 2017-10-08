import urllib3
import bs4 as bs
import pandas as pd
from unidecode import unidecode

#  soup.find_all().get('value')
#  soup.table

class FDA_CalendarClass():
    def __init__(self, *args, **kwargs):
        self.url = 'https://www.biopharmcatalyst.com/calendars/fda-calendar'
        self.raw_data = None
        self.soup = None
        self.Headers = {}
        self.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def pull_data(self):

        #  read the webpage
        pm = urllib3.PoolManager()
        # with pm.request('GET', self.url, headers=self.Headers) as connection:
        #     self.raw_data = connection.data
        connection = pm.request('GET', self.url, headers=self.Headers)
        self.raw_data = connection.data

        #  parse the html
        self.soup = bs.BeautifulSoup(self.raw_data, 'lxml')

    def read_table(self):

        #  filter out the table from the html
        raw_table = self.soup.find('div', class_='table-wrap')

    def read_tickerlist(self):

        #  filter out the tickers from the html
        raw_tickerlist_small = self.soup.find('datalist', class_='datalist', id='tickers-list--small')
        raw_tickerlist_modal = self.soup.find('datalist', class_='datalist', id='tickers-list--modal')

        raw_line = raw_tickerlist_small.find('option').get('value')
        print(raw_line)
        print(bs.BeautifulSoup(raw_line, 'lxml').find_all('span'))
        # print(raw_tickerlist_small)

    def try_pandas(self):
        dfs = pd.read_html(self.url)
        for df in dfs:
            print(df.head(), '\n')

if __name__ == '__main__':
    FDA_Calendar = FDA_CalendarClass()
    FDA_Calendar.pull_data()
    FDA_CalendarClass.read_tickerlist(FDA_Calendar)

    # FDA_Calendar.try_pandas()