from urllib.request import urlopen as op
import bs4 as bs

url = 'http://www.nu.nl'

with op(url) as connection:
    raw_data = connection.read()

soup = bs.BeautifulSoup(raw_data, 'lxml')
for paragraph in soup.find_all('span'):
    pass
    # print(paragraph.text)
print(soup.get_text())
