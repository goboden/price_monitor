users = []
users_urls = {}


class UserExistsError(Exception):
    pass


class URLExistsError(Exception):
    pass


def add_user(user_name, telegram_id, chat_id):
    print(f'{user_name} ({telegram_id}) from {chat_id}')
    if telegram_id not in users:
        users.append(telegram_id)
    else:
        raise UserExistsError


def add_url(telegram_id, url, price):
    print(f'{telegram_id}, {url}, {price}')
    user_urls = users_urls[telegram_id] if telegram_id in users_urls else []
    if url not in user_urls:
        user_urls.append(url)
        users_urls[telegram_id] = user_urls
    else:
        raise URLExistsError
