import db as DB
import encryption as Encryption
import re
import time
from django.views.decorators.csrf import csrf_exempt

TOKEN_VALID_TIME = 60 * 60 * 2

db = DB.DB()

def handle_login(request):
    token, message = login(request['username'], request['password'])
    if token is None:
        return {
            'result': False,
            'message': message
        }
    return {
        'result': True,
        'token': token,
        'message': message
    }


def handle_register(request):
    token, message = register(request['username'], request['password'])
    if token is None:
        return {
            'result': False,
            'message': message
        }
    return {
        'result': True,
        'token': token,
        'message': message
    }


def is_valid_string(string):
    return re.match(r'[A-Za-z0-9@#$%^&+=]{5,12}', string)


def generate_token(username):
    token = Encryption.generate_token(Encryption.TOKEN_LENGTH)
    db.insert(DB.TOKENS_TABLE, (username, token, int(time.time()) + TOKEN_VALID_TIME))
    return token

def register(username, password):
    if not is_valid_string(username):
        return None, 'Invalid Username'
    if not is_valid_string(password):
        return None, 'Invalid Password'
    result = db.execute_and_fetch_one('SELECT * FROM ' + DB.USER_TABLE + ' WHERE username = ?', (username,))
    if result is not None:
        return None, 'User already exists'
    salt = Encryption.generate_token(Encryption.SALT_LENGTH)
    hashed_password = Encryption.hash(password, salt)
    db.insert(DB.USER_TABLE, (username, salt, hashed_password))

    return generate_token(username), 'Registration success'


def authenticate(username, password):
    result = db.execute_and_fetch_one('SELECT salt FROM ' + DB.USER_TABLE + ' WHERE username = ?', (username,))
    if result is None:
        return False
    salt = result[0]
    print(salt)
    hashed_password = Encryption.hash(password, salt)
    result = db.execute_and_fetch_one('SELECT * FROM ' + DB.USER_TABLE + ' WHERE username = ? AND password = ?', (username, hashed_password))
    return result is not None


def verify_token(token, username):
    result = db.execute_and_fetch_one('SELECT expiry FROM ' + DB.TOKENS_TABLE + ' WHERE token = ? AND username = ?', (token, username))
    return result is not None and result[0] >= int(time.time())


def login(username, password):
    if not authenticate(username, password):
        return None, 'Login failed'

    return generate_token(username), 'Login success'

'''
db.setup()
print(register('abcdef', 'abcdef'))
token = login('abcdef', 'abcde')
print(token)
token = login('abcdef', 'abcdef')
print(token)
print(verify_token('abcde', token))
'''