from urllib.request import urlopen as op
import bs4 as bs
from unidecode import unidecode

url = 'http://www.nu.nl'

with op(url) as connection:
    raw_data = connection.read()

soup = bs.BeautifulSoup(raw_data, 'lxml')
articles = []

## data is wrapped in li tags, and then packed in a ul tag
div = soup.find('div', class_='column first')
article_list = div.ul

index = 0
for article in div.find_all('li'):
    articles.append({})
    try:
        articles[index]['href'] = "http://www.nl{}".format(article.a.get('href'))
        articles[index]['timestamp'] = article.find('span', class_='timestamp').text
        articles[index]['timestamp'] = unidecode(articles[index]['timestamp'])
        articles[index]['section'] = article.find('span', class_='section').text
        articles[index]['title'] = article.find('span', class_='title').text
    except AttributeError:
        pass
    index +=1

print(articles)
print(len(articles))