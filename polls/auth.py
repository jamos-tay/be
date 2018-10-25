import db as DB
import encryption as Encryption
import re
import time

TOKEN_VALID_TIME = 60 * 60 * 2

db = DB.DB()


def is_valid_string(string):
    return re.match(r'[A-Za-z0-9@#$%^&+=]{5,12}', string)


def register(username, password):
    if not is_valid_string(username) or not is_valid_string(password):
        return False
    result = db.execute_and_fetch_one('SELECT * FROM ' + DB.USER_TABLE + ' WHERE username = ?', (username,))
    if result is not None:
        return False
    salt = Encryption.generate_token(Encryption.SALT_LENGTH)
    hashed_password = Encryption.hash(password, salt)
    db.insert(DB.USER_TABLE, (username, salt, hashed_password))
    return True


def authenticate(username, password):
    result = db.execute_and_fetch_one('SELECT salt FROM ' + DB.USER_TABLE + ' WHERE username = ?', (username,))
    if result is None:
        return False
    salt = result[0]
    print(salt)
    hashed_password = Encryption.hash(password, salt)
    result = db.execute_and_fetch_one('SELECT * FROM ' + DB.USER_TABLE + ' WHERE username = ? AND password = ?', (username, hashed_password))
    return result is not None


def verify_token(username, token):
    result = db.execute_and_fetch_one('SELECT expiry FROM ' + DB.TOKENS_TABLE + ' WHERE username = ? AND token = ?', (username, token))
    return result is not None and result[0] >= int(time.time())


def login(username, password):
    if not authenticate(username, password):
        return None

    token = Encryption.generate_token(Encryption.TOKEN_LENGTH)
    db.insert(DB.TOKENS_TABLE, (username, token, int(time.time()) + TOKEN_VALID_TIME))
    return token

db.setup()
print(register('abcdef', 'abcdef'))
token = login('abcdef', 'abcde')
print(token)
token = login('abcdef', 'abcdef')
print(token)
print(verify_token('abcde', token))