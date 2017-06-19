from urllib.request import urlopen as op
import bs4 as bs

url = 'http://www.nu.nl'

with op(url) as connection:
    raw_data = connection.read()

soup = bs.BeautifulSoup(raw_data, 'lxml')

## use the nav element to navigate around the website.
## find a specific class with soup.find_all('<tag>', class_='<someclass>')
## hyperlinks are embodied by a tags

div = soup.find('div', class_='column first')
print(div.ul)

# with open("C:/Users/David.MIDDENAARDE/Documents/web-scraping_output.txt", 'w') as doc:
#     for paragraph in soup.find_all('div', class_='block headline'):
#         #pass
#         doc.write(paragraph.text)
#         print(paragraph)
#         print(paragraph.get('href'))
#         print(paragraph.a.get('href'))
#print(soup.get_text())
