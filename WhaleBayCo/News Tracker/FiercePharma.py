import urllib3
import bs4 as bs
from fake_useragent import UserAgent
import certifi
from random import randint


class news_page():

    def __init__(self, url=None):
        self.url = url
        self.useragent = UserAgent()
        self.header_list = ['firefox', 'internetexplorer', 'safari', 'chrome', 'opera']
        self.Headers = {'User-Agent': self.useragent.data_browsers[self.header_list[randint(0, 4)]][randint(0, 49)]}

    def retrieve_page(self):
        """retreive the html page"""

