import requests
from bs4 import BeautifulSoup
import json

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('meta', class_='keywords')

with open("authors.json", "w+") as f:
    l = []

    for author in authors:
        data = {
            'name': author.text
        }
        l.append(data)
    
    json.dump(l, f, indent=4)

with open('quotes.json', "w+") as f:
    l = []

    for i in range(len(quotes)):
        data = {
            'tags': tags[i]['content'].split(','),
            "author": authors[i].text,
            'quote': str(quotes[i].text)[1:-1]
        }
        l.append(data)

    json.dump(l, f, indent=4)