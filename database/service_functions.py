from hashlib import scrypt
from config import SECRET_KEY, LOG_FILENAME
import logging


def gen_password(password):
    return scrypt(password.encode(), salt=SECRET_KEY.encode(), n=8, r=256, p=4, dklen=64).hex()


def log_to_file(text):
    logger = logging.getLogger("Database module")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(text)
