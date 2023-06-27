import File
import Output
import Scraper

MAIN_PAGE_URL = 'https://news.ycombinator.com/'
COMMENT_URLS = 'comment_urls.csv'

new_project = input("delete previous files and run project with new files?\n y/n?\n")
if new_project == 'y':
    File.delete_all_files()
Scraper.main_page_scraper(MAIN_PAGE_URL)
Scraper.comments_page_scraper(COMMENT_URLS)
Output.print_output()
