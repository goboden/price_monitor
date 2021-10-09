from hashlib import scrypt
from config import SECRET_KEY


def gen_password(password):
    return scrypt(password.encode(), salt=SECRET_KEY.encode(), n=8, r=256, p=4, dklen=64).hex()

