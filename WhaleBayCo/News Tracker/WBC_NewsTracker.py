import urllib3
import bs4 as bs
from fake_useragent import UserAgent
import certifi
import logging
from random import randrange, random
from urllib.parse import urlparse
import re
import json
from datetime import datetime

# fiercepharma also has a keyword section : https://www.fiercepharma.com/keyword/

#  create logger
logger = logging.getLogger('news_scraper.main')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.warning("test warning")
class article_scraper():
    """class to scrape articles and check for interests"""
    soup = None
    interests = []
    articles = []
    interesting_articles = []
    header_threshold = 0
    article_template = {"ID": None,
                        "title": None,
                        "date": None,
                        "epoch": None,
                        "abstract": None,
                        "source_url": None,
                        "domain": None,
                        "full_text": '',
                        "category": None,
                        "author": None,
                        "thumbnail_url": None,
                        "dt_format": None,
                        "interests": [],
                        "of_interest": False}

    def __init__(self, interests=None):
        self.useragent = UserAgent()
        self.header_list = list(self.useragent.data_browsers.keys())
        self.Headers = {}
        self.switch_headers()
        self.pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self._get_interests(interests)

    def switch_headers(self):
        try:
            if self.header_threshold and random() < self.header_threshold:
                user_agent_index = randrange(len(self.header_list))
                browser_data_index = randrange(len(self.useragent.data_browsers[self.header_list[user_agent_index]]))
                self.Headers = {'User-Agent': self.useragent.data_browsers[self.header_list[user_agent_index]][browser_data_index]}
            else:
                self.header_threshold = random()
        except Exception as e:
            print(len(self.header_list), len(self.useragent.data_browsers[self.header_list[user_agent_index]]))
            raise e

    def _get_interests(self, interests):
        if isinstance(interests, type(list())):
            self.interests = interests.copy()
            return
        elif isinstance(interests, type(str())):
            try:
                with open(interests, 'r', encoding='utf-8') as interests_file:
                    for line in interests_file.readlines():
                        self.interests.append(line.strip())
            except FileNotFoundError:
                logger.warning(":cls: {} :meth: _get_interest, file could not be found: {}".format(
                    self.__class__.__name__, interests))
            except Exception as e:
                logger.warning(
                    ":cls: {} :meth: _get_interest, error occured while processing interests: {}, with error {}".format(
                        self.__class__.__name__, interests, e))
            return
        elif not interests:
            logger.info("no interests specified")
            return
        else:
            logger.warning(":cls: {} :meth: _get_interests: :param: interests neither type string nor list".format(
                self.__class__.__name__))
            return

    def scrape_articles(self, url):
        title_matches = []
        self.switch_headers()

        if not url:
            logger.error(":cls: {} :meth: check_for_articles, :param: url not specified")
            return "URLNotSpecified"

        domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        page = self.retrieve_page(url)
        if not page:
            return "NoPageFound"

        articles, oldest_article = self.extract_articles(page, domain)
        if not articles:
            return "NoArticlesFound"
        logger.info(":cls: {} :meth: scrape articles Found {} articles on {}".format(self.__class__, len(articles), url))

        try:
            articles = self.check_interests(articles, url)
        except TypeError as e:
            return "CheckInterestError"

        return {"articles": articles, "oldest_article": oldest_article}

    def extract_articles(self, page, domain):
        if 'fiercepharma' in domain or 'fiercebiotech' in domain:
            articles, oldest_article = self.extract_fiercepharma(page, domain)
            if not articles:
                logger.error("Error in :meth: extract_articles: :meth: extract_fiercepharma returned none")
                return
        else:
            logger.warning(":cls: {} :meth: extract_articles, cannot extract articles from domain '{}'".format(self.__class__.__name__, domain))
            articles, oldest_article = None, None

        return articles, oldest_article

    def retrieve_page(self, url=None):
        """retreive the html page"""
        if not url:
            logger.warning(":cls: {} :meth: retrieve_page, no url specified".format(self.__class__.__name__))
            return
        try:
            conn = self.pool_manager.request('GET', url, headers=self.Headers)
            raw_data = conn.data

        except Exception as e:
            logger.warning(":cls: {} :meth: retrieve_page, error retrieving page: {}".format(self.__class__.__name__, e))
            return
        try:
            soup = bs.BeautifulSoup(raw_data, 'lxml')
        except Exception as e:
            logger.warning(":cls: {} :meth: retrieve_page, parsing data with beautifulsoup: {}".format(
                self.__class__.__name__, e))
            return

        logger.info(":meth: retrieve_page: retrieved data from page {} in :cls: {}".format(url, self.__class__.__name__))
        return soup

    def extract_fiercepharma(self, soup, domain):
        if not domain:
            logger.error(":cls: {} :meth: extract_fiercepharma, Error: :param: parent_website not specified".format(
                self.__class__.__name__))
            return
        if not soup:
            logger.error(":cls: {} :meth: extract_fiercepharma, Error: :param: soup not specified".format(
                self.__class__.__name__))
            return
        try:
            main_content = soup.find(id='content')
            article_list = []
            oldest_article = None
            for card in main_content.find_all('div', class_='card'):
                # get the properties from the main article card
                try:
                    article_data = self.article_template.copy()
                    article_data['thumbnail_url'] = self.string_formater(card.find('img')['src'])
                    try:
                        article_data['category'] = self.string_formater(card.find('div', class_='taxonomy').a.text)
                    except AttributeError:
                        pass
                    article_data['source_url'] = self.string_formater("{}{}".format(domain, card.find('h2', class_='list-title').a['href']))
                    article_data['title'] = self.string_formater(card.find('h2', class_='list-title').a.text)
                    article_data['author'] = self.string_formater(card.find('div', class_='byline').span.a.text)
                    article_data['date'] = self.string_formater(card.find('div', class_='byline').find('time').text)
                    article_data['dt_format'] = "%b %d, %Y %I:%M%p"
                    article_data['domain'] = domain
                    article_data['abstract'] = self.string_formater(card.find('div', class_='views-field-field-introduction-teaser').text)
                except Exception as e:
                    print(article_data)
                    raise e

                # remember date of oldest article collected
                article_date = datetime.strptime(article_data['date'], article_data['dt_format'])
                article_data['epoch'] = int(article_date.timetuple())
                if not oldest_article:
                    oldest_article = article_date
                else:
                    if article_date < oldest_article:
                        oldest_article = article_date

                # get the full text
                main_article_body = self.retrieve_page(article_data['source_url'])
                try:
                    for p in main_article_body.find('div', property="schema:articleBody").find_all('p'):
                        article_data['full_text'] += self.string_formater(p.text)
                except AttributeError:
                    #  sponsored articles don't have the 'schema:articleBody' in the div tag
                    for p in main_article_body.find('div', class_="node__content").find_all('p'):
                        article_data['full_text'] += self.string_formater(p.text)

                #  get category from the main page, because otherwise sponsored articles will not be categorized
                text_elements = main_article_body.find('div', class_="taxonomy-primary").findAll(text=True)
                text_elements.sort()
                article_data['category'] = self.string_formater(text_elements[-1])

                # store article data in list
                article_list.append(article_data.copy())

            if article_list:
                oldest_article = oldest_article.strftime(article_list[0]['dt_format'])
        except Exception as e:
            logger.warning(":cls: {} :meth: extract_fiercepharma, error while processing data: {}".format(
                self.__class__.__name__, e))
            return

        if not article_list:
            logger.warning(":cls: {} :meth: extract_fiercepharma, no articles found in page")

        if not oldest_article:
            logger.warning(":cls: {} :meth: extract_fiercepharma, :var: oldest_article not set")

        return article_list, oldest_article

    @staticmethod
    def string_formater(string):
        return str(string, ).strip().replace('\xa0', ' ')

    def check_interests(self, articles, url):
        """check if any of the articles pulled are of interest, if so append them to a list"""
        # get processed articles as param and only return the end result
        if not self.interests:
            logger.warning(":cls: {} :meth: check_interests, no interests specified, not checking for matches")

        try:
            found_atleast_one = False
            for article in articles:
                for interest in self.interests:
                    article['interests'].append(interest)
                    compiled_re = re.compile(r'(?i)(\b{}\b)'.format(interest))

                    #  check if the keyword is present in the article
                    if compiled_re.findall(article['title']) or compiled_re.findall(article['full_text']):
                        found_atleast_one = True
                        article[interest] = True
                        article['of_interest'] = True
                    else:
                        article[interest] = False

            if found_atleast_one:
                logger.info(":meth: check_interests: Found {} interesting articles in url {}".format(len(self.interesting_articles), url))
            else:
                logger.info(":meth: check_interests: Found no interesting articles in url {}".format(url))
        except Exception as e:
            logger.warning(":cls: {} :meth: check_interests, error while checking for interesting articles: {}".format(
                self.__class__.__name__, e))

        return articles

def scrape_process(url, interests=None):
    bot = article_scraper(interests=interests)
    try:
        articles = bot.scrape_articles(url)
    except TypeError as e:
        return None
    return articles

if __name__ == '__main__':
    print(scrape_process('https://www.fiercepharma.com/pharma/m-a'))
