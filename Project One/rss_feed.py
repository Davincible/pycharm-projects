import feedparser
import json

url = 'http://www.fiercepharma.com/rss/xml'

data = feedparser.parse(url)
#print(json.dumps(data, indent=4))
for article in data['entries']:
    print(article['title'])
