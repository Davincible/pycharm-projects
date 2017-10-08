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
        self.TickerSymbols = pd.DataFrame(columns=['ticker', 'company'])
        self.FDA_Calendar = pd.DataFrame(columns=['ticker', 'drug', 'indication', 'news-date', 'news-note', 'news-url'])
        self.start_date = None
        self.end_date = None
        self.events_this_week = None
        self.events_next_week = None

    def pull_data(self):
        """ pull the html of the url """

        #  read the webpage
        pm = urllib3.PoolManager()
        try:
            connection = pm.request('GET', self.url, headers=self.Headers)
        except:
            print("Failed to connect.")

        self.raw_data = connection.data

        #  parse the html
        self.soup = bs.BeautifulSoup(self.raw_data, 'lxml')
        print('Message: page successfully downloaded')

    def read_table(self):
        """ filter out the table from the html """

        #  find the table in the html, then create a list with the html of every single row
        raw_table = self.soup.find('div', class_='table-wrap')
        raw_item_list = raw_table.find_all('tr')

        #  filter the data from every single row and append it to the dataframe
        for row in raw_item_list:
            data_dict = {}
            if not row.find_all('th', class_='thead-th sort'):
                data_dict['ticker'] = row.find('a', class_='ticker').text
                data_dict['drug'] = row.find('strong', class_='drug').text
                data_dict['indication'] = row.find('div', class_='indication').text
                data_dict['news-date'] = row.find('time', class_='catalyst-date').text
                data_dict['news-note'] = row.find('div', class_='catalyst-note').text
                data_dict['news-url'] = row.find_all('td')[-1].find('a').get('href')
                self.FDA_Calendar = self.FDA_Calendar.append(data_dict, ignore_index=True)
        print("Message: Table succesfully imported")

    def next_weeks_calendar(self, print_=False):
        self.start_date = '10/09/2017'
        self.end_date = '10/15/2017'
        mask = (self.FDA_Calendar['news-date'] >= self.start_date) & (self.FDA_Calendar['news-date'] <= self.end_date)
        self.events_next_week = self.FDA_Calendar.loc[mask]
        if print_:
            print(self.FDA_Calendar.loc[mask])

    def export_events_next_week(self):
        file_name = 'Events in the week of {}.xlsx'.format(self.start_date)
        file_name = file_name.replace('/', '-')
        self.events_next_week.to_excel(file_name)
        print("Message: successfully saved events next week as xlsx")

    def export_calander_to_xlsx(self):
        file_name = 'FDA Calendar - {}.xlsx'.format(self.start_date)
        file_name = file_name.replace('/', '-')
        self.FDA_Calendar.to_excel(file_name)
        print("Message: successfully saved calendar as xlsx")

    def read_tickerlist(self):
        """  filter out the tickers from the html """

        # find the small and modal ticker list in the parsed html
        raw_tickerlist_small = self.soup.find('datalist', class_='datalist', id='tickers-list--small')
        raw_tickerlist_modal = self.soup.find('datalist', class_='datalist', id='tickers-list--modal')

        # filter out the value var from the option tag and store it in a dataframe
        raw_lines = [item.get('value') for item in raw_tickerlist_small.find_all('option')]
        info_dict = {}
        for row in raw_lines:
            info = [str(x.text) for x in bs.BeautifulSoup(row, 'lxml').find_all('span')]
            info_dict['ticker'] = info[0]
            info_dict['company'] = info[1]
            self.TickerSymbols = self.TickerSymbols.append(info_dict, ignore_index=True)
        print("Message: ticker list succesfully imported")

    def export_tickerlist_to_xlsx(self):
        self.FDA_Calendar.to_excel('Ticker List.xlsx')
        print("Message: successfully saved ticker list as xlsx")

if __name__ == '__main__':
    FDA_Calendar = FDA_CalendarClass()
    FDA_Calendar.pull_data()
    FDA_Calendar.read_table()
    FDA_Calendar.next_weeks_calendar()
    FDA_Calendar.read_tickerlist()
    FDA_Calendar.export_calander_to_xlsx()
    FDA_Calendar.export_tickerlist_to_xlsx()
    FDA_Calendar.export_events_next_week()
