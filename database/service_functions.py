from hashlib import scrypt
from config import SECRET_KEY, LOG_FILENAME
import logging
from random import shuffle, choice


def gen_password_hash(password, salt=SECRET_KEY):
    return scrypt(password.encode(), salt=salt.encode(), n=8, r=256, p=4, dklen=64).hex()


def log_to_file(text):
    logger = logging.getLogger("Database module")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(text)


def password_generator(password_length=15):
    alphabet = list('1234567890+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    shuffle(alphabet)
    password = ''.join([choice(alphabet) for x in range(password_length)])
    return password
