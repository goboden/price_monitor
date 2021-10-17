import secrets
import string
import hashlib
import binascii
from flask_login import UserMixin


users = []
users_db = {}
users_urls = {}


class User(UserMixin):
    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def __repr__(self):
        return f'id={self.id}, name={self.name}'


def get_user_by_password(password):
    if password == '1':
        user = User('1000', 'Authenticated User')
        users_db[user.id] = user
        return user
    elif password == '2':
        user = User('2000', 'New User 2000')
        users_db[user.id] = user
        return user
    return None


def get_user_by_id(user_id):
    user = users_db.get(user_id, None)
    return user


salt = 'DCNGgKtG7fY4Z8b9RjE8AXSnQn05k17p'


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


def generate_hash(password, salt):
    pass_b = password.encode('utf-8')
    salt_b = str.encode(salt)
    key = hashlib.pbkdf2_hmac('sha256', pass_b, salt_b, 1000000)
    hash = salt + binascii.hexlify(key).decode()
    return hash


def generate_password(telegram_id):
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for i in range(32))
    return new_password


if __name__ == '__main__':
    password = generate_password(1)
    print(password)

    hash1 = generate_hash(password, salt)
    print(f'hash1={hash1}')

    hash2 = generate_hash(password, salt)
    print(f'hash2={hash2}')

    hash3 = generate_hash(password, ('A' + salt)[:32])
    print(f'hash3={hash3}')

    print(hash1 == hash2)
    print(hash1 == hash3)

