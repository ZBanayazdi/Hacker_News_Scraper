import os
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

articles = []

def file_maker(page, *indx):
    if indx:
        file_name = page + '_page' + str(indx[0]) + '.txt'
    else:
        file_name = page + '_page.txt'

    try:
        with open(file_name, 'x', encoding='utf-8'):
            pass
    except:
        pass
    return file_name


def soup_maker(fn, url):
    with open(fn, 'r+', encoding='utf-8') as file:
        if os.path.getsize(fn) == 0:
            html = requests.get(url).text
            file.write(html)
        else:
            html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def main_page_scraper():
    main_file_name = file_maker('main')
    main_soup = soup_maker(main_file_name, 'https://news.ycombinator.com/')
    comment_url = []

    for item in main_soup.find_all('tr', class_='athing'):
        item_rank = item.find('span', class_='rank')
        item_rank = item_rank.get_text().replace('.', '') if item_rank else None

        item_span = item.find('span', class_='titleline')
        item_a = item_span.find('a') if item_span else None
        item_link = item_a.get('href') if item_a else None
        item_text = item_a.get_text(strip=True) if item_a else None

        next_row = item.find_next_sibling('tr')
        item_score = next_row.find('span', class_='score') if next_row else None
        item_score = item_score.get_text(strip=True) if item_score else '0 points'

        item_comments = next_row.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)')) if next_row else None
        item_comments_text = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comments'

        if item_comments:
            href = item_comments.get('href')
            comment_full_url = urljoin('https://news.ycombinator.com/', href)
            comment_url.append(comment_full_url)

        articles.append({'rank': item_rank,
                         'link': item_link,
                         'title': item_text,
                         'score': item_score,
                         'comments': item_comments_text})

    return comment_url, articles


def comment_page_scraper(fn, url):
    html_soup = soup_maker(fn, url)

    
    
comments_url, articles = main_page_scraper()

for article in articles:
    for key, val in article.items():
        if key == 'rank':
            print('#' + str(val) + ':')
        if key != 'rank':
            print(key, ':', val)
    print('\n********************\n')
    
for index, url in enumerate(comments_url):
    fn = file_maker('comment', index)
    comment_page_scraper(fn, url)
