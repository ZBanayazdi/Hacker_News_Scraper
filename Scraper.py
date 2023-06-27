import os
import re
from urllib.parse import urljoin

import File
import Save

MAIN_FILE_NAME = 'main.txt'


def main_page_scraper(main_page_url):
    main_soup = File.soup_maker(MAIN_FILE_NAME, main_page_url)
    if main_soup:
        for item in main_soup.find_all('tr', class_='athing'):
            item_rank = item.find('span', class_='rank')
            item_rank = item_rank.get_text().replace('.', '') if item_rank else None

            item_span = item.find('span', class_='titleline')
            item_a = item_span.find('a') if item_span else None
            item_link = item_a.get('href') if item_a else None
            item_link = urljoin(main_page_url, item_link)
            item_text = item_a.get_text(strip=True) if item_a else None

            next_row = item.find_next_sibling('tr')
            item_score = next_row.find('span', class_='score') if next_row else None
            item_score = item_score.get_text(strip=True) if item_score else '0 points'

            item_comments = next_row.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)')) if next_row else None
            item_comments_text = item_comments.get_text(strip=True).replace('\xa0',
                                                                            ' ') if item_comments else '0 comments'

            if item_comments:
                href = item_comments.get('href')
                comment_full_url = urljoin(main_page_url, href)
                Save.save_to_file(Save.COMMENT_URLS_FILE, comment_full_url)
            Save.save_to_file(Save.ARTICLE_FILE, {'rank': item_rank,
                                                  'link': item_link,
                                                  'title': item_text,
                                                  'score': item_score,
                                                  'comments': item_comments_text})
        Save.save_to_file(Save.COMMENT_URLS_FILE, '$eof$')
        Save.save_to_file(Save.ARTICLE_FILE, {'rank': '$eof$',
                                              'link': '$eof$',
                                              'title': '$eof$',
                                              'score': '$eof$',
                                              'comments': '$eof$'})


def comment_page_scraper(file_name, url):
    comment_soup = File.soup_maker(file_name, url)
    for fatitem in comment_soup.find_all('table', class_='fatitem'):
        fatitem_title = fatitem.find('span', class_='titleline')
        fatitem_title = fatitem_title.find('a') if fatitem_title else None
        fatitem_title = fatitem_title.get_text() if fatitem_title else None

        title = fatitem.find('span', class_='titleline')
        fatitem_reference = title.find('span', class_='sitestr') if title else None
        fatitem_reference = fatitem_reference.find_parent('a') if fatitem_reference else None
        fatitem_reference = 'https://' + fatitem_reference.get_text() if fatitem_reference else None

        fatitem_score = fatitem.find('span', class_='score') if fatitem else None
        fatitem_score = fatitem_score.get_text() if fatitem_score else None

        fatitem_user = fatitem.find('a', class_='hnuser') if fatitem else None
        fatitem_user = fatitem_user.get_text() if fatitem_user else None

        fatitem_age = fatitem.select('span.age>a')[0].get_text() if fatitem else None

        fatitem_comment_numbers = fatitem.select('span~a') if fatitem else None
        fatitem_comment_numbers = fatitem_comment_numbers[-1].get_text(strip=True).replace('\xa0',
                                                                                           ' ') if fatitem_comment_numbers else None
        Save.save_to_file(Save.COMMENTS_FILE, {'title': fatitem_title,
                                               'reference': fatitem_reference,
                                               'score': fatitem_score,
                                               'user': fatitem_user,
                                               'age': fatitem_age,
                                               'comment_numbers': fatitem_comment_numbers})


def comments_page_scraper(file_name):
    with open(file_name, 'r', encoding='utf-8')as comment_urls_file:
        comment_urls = comment_urls_file.readlines()
        for index, url in enumerate(comment_urls):
            if '$eof$' not in url:
                file_path = f'{index}comment.txt'
                if os.path.isfile(file_path):
                    file = open(file_path, 'a+')
                else:
                    file = File.file_maker('comment.txt', 'a+', index)
                comment_page_scraper(file.name, url)
                file.close()
        Save.save_to_file(Save.COMMENTS_FILE, {'title': '$eof$',
                                               'reference': '$eof$',
                                               'score': '$eof$',
                                               'user': '$eof$',
                                               'age': '$eof$',
                                               'comment_numbers': '$eof$'})
