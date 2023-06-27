import os

import requests
from bs4 import BeautifulSoup


def file_maker(file_name, action, *index):
    if index:
        file_name = str(index[0]) + file_name

    try:
        if not os.path.isfile(file_name):
            file = open(file_name, action, encoding='utf-8')
            return file
    except:
        return None


def soup_maker(file_name, url):
    with open(file_name, 'a+', encoding='utf-8') as file:
        file.seek(0)
        if '$eof$' in file.read():
            return None
        else:
            if os.path.getsize(file_name) == 0:
                response = requests.get(url)
                html = response.text
                file.write(html)
            else:
                file.seek(0)
                html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    return soup


def delete_all_files():
    dir_name = "C:/Users/Zeinab/PycharmProjects/HackerNewsScraper"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".txt") or item.endswith('.csv'):
            os.remove(os.path.join(dir_name, item))
