import requests
import re
from bs4 import BeautifulSoup

articles = []
url = 'https://news.ycombinator.com/'

r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')

for item in html_soup.find_all('tr', class_='athing'):
    item_rank = item.find('span', class_='rank')
    item_rank = item_rank.get_text().replace('.','') if item_rank else None
    item_span = item.find('span', class_='titleline')
    item_a = item_span.find('a')
    item_link = item_a.get('href') if item_a else None
    item_text = item_a.get_text(strip=True) if item_a else None
    next_row = item.find_next_sibling('tr')
    item_score = next_row.find('span', class_='score')
    item_score = item_score.get_text(strip=True) if item_score else '0 points'
    item_comments = next_row.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)'))
    item_comments = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comments'
    articles.append({'rank': item_rank,
                     'link': item_link,
                     'title': item_text,
                     'score': item_score,
                     'comments': item_comments})

for article in articles:
    for key, val in article.items():
        if key=='rank':
            print('#'+str(val)+':')
        if key != 'rank':
            print(key, ':', val)
    print('\n********************\n')
