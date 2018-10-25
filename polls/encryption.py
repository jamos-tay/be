import hashlib
import random

SALT_LENGTH = 16
TOKEN_LENGTH = 16


def generate_token(length):
    return ''.join(chr(random.randint(32,126)) for i in range(length))


def hash(password, salt):
    salted_password = (password + salt).encode('utf-8')
    return hashlib.sha256(salted_password).hexdigest()
