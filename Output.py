import csv
from prettytable import PrettyTable

def pretty_printer(file_name):
    data = []
    with open(file_name, 'r', encoding='utf-8')as file:
        reader = csv.reader(file)
        for row in reader:
            if any(row):
                data.append(row)
    while not data[-1]:
        data.pop()
    table = PrettyTable()
    table.field_names = data[0]  # استفاده از اولین ردیف برای تعیین نام ستون‌ها
    for row in data[1:]:  # شروع از دومین ردیف برای اضافه کردن محتویات جدول
        table.add_row(row)
    print(table)


def comment_url_print():
    print('----------\nCOMMENT_URLS:\n')
    file_name = 'comment_urls.csv'
    with open(file_name, 'r', encoding='utf-8')as comment_urls_file:
        print(comment_urls_file.read())


def comments_print():
    print('----------\nCOMMENTS:')
    file_name = 'comments.csv'
    pretty_printer(file_name)


def article_print():
    print('----------\nARTICLE:')
    file_name = 'article.csv'
    pretty_printer(file_name)


def print_output():
    article_print()
    comment_url_print()
    comments_print()
