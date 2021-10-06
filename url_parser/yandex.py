import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'Accept':
        '''text/html,
            application/xhtml+xml,
            application/xml;q=0.9,
            image/webp,image/apng,
            */*;q=0.8,application/signed-exchange;v=b3;q=0.9''',
        'Accept-Language':
        'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection':
        'keep-alive',
        'Host':
        'market.yandex.ru',
        'Sec-Fetch-Dest':
        'document',
        'Sec-Fetch-Mode':
        'navigate',
        'Sec-Fetch-Site':
        'none',
        'Sec-Fetch-User':
        '?1',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        '''Mozilla/5.0 (X11; Linux x86_64)
           AppleWebKit/537.36 (KHTML, like Gecko)
           Chrome/83.0.4103.61 Safari/537.36
        ''',
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        return False


def get_price(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        price_div = soup.find('div', class_='_3NaXx _3kWlK')
        return price_div
    return 0
