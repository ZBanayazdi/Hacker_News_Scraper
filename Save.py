import csv
import os

ARTICLE_FILE = 'article.csv'
COMMENT_URLS_FILE = 'comment_urls.csv'
COMMENTS_FILE = 'comments.csv'


def save_to_file(file_name, row):
    with open(file_name, 'a+', encoding='utf-8', newline='')as file:
        file.seek(0)
        if '$eof$' in file.read():
            return
        else:
            writer = csv.writer(file, delimiter=',')
            if file_name == ARTICLE_FILE or file_name == COMMENTS_FILE:
                keys = list(row.keys())
                values = list(row.values())
                if os.path.getsize(file_name) == 0:
                    writer.writerow(keys)  # header
                writer.writerow(values)
            if file_name == COMMENT_URLS_FILE:
                writer = csv.writer(file)
                writer.writerow([row])
