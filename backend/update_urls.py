from database.get_from_db import get_urls_from_db
from url_parser import parse
from time import sleep

def update_urls():
    urls = get_urls_from_db()
    for url in urls:
        print(url)
        html = parse(url[0])
        print(html.price)
        sleep(10)


if __name__ == '__main__':
    update_urls()
