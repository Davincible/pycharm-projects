##  get the accurate time stamps from the article pages
##  Search the whole data base for interests
## nu.nl/tag/<interest>
from urllib.request import urlopen as op
import bs4 as bs
from unidecode import unidecode
import re

#url = 'http://www.nu.nl'
url = 'http://www.businesswire.com/portal/site/home/news/'
website = 'http://www.businesswire.com'

with op(url) as connection:
    raw_data = connection.read()

soup = bs.BeautifulSoup(raw_data, 'lxml')
articles = []

## data is wrapped in li tags, and then packed in a ul tag
interests = ['trump', "assassin's creed", 'cia', 'eu', 'cameraman', 'amsterdam', 'italië']


index = 0
for article_list in soup.find_all('ul'):
    for article in article_list.find_all('li'):
        articles.append({})
        try:
            link = article.a.get('href')
            if link[0] == '/':
                articles[index]['href'] = "{}{}".format(website, link)
            else:
                articles[index]['href'] = link
            articles[index]['timestamp'] = article.find('span', class_='timestamp').text
            articles[index]['timestamp'] = unidecode(articles[index]['timestamp'])
            articles[index]['section'] = article.find('span', class_='section').text
            articles[index]['title'] = article.find('title').text
        except AttributeError:
            pass

        index +=1


    # try:
    #     print(element['title'])
    # except KeyError:
    #     pass
for interest in interests:
    regex = r'(?i)(\b{}\b)'.format(interest)
    regex_compiled = re.compile(regex)

    for element in articles:
        try:
            if regex_compiled.findall(element['title']):
                print("Dit artikel is van interesse:", element)
                print("Door de interesse:", interest, "\n")
        except KeyError:
            pass

print("De hele lijst:", articles)
print("Heeft een lengte van:", len(articles))
with open('C:/Users/David.MIDDENAARDE/Documents/general_NewsTracker_Output.txt', 'w') as output_document:
    for item in articles:
        output_document.write(str(item) + '\n')