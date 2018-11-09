from django.views.decorators.csrf import csrf_exempt
import db as DB
import storage as Storage

db = DB.DB()

FILE_QUERY = 'SELECT author_file_id, review_file_id, submission_file_id FROM File WHERE username = ?'

STATE_SELECT = '''
SELECT author_file_id, review_file_id, submission_file_id, state_data
FROM State
WHERE state_id = ?
'''

ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def encode_state(state_int):
    state_str = ''
    while state_int > len(ALPHABETS):
        state_str += ALPHABETS[state_int % len(ALPHABETS)]
        state_int = state_int // len(ALPHABETS)
    state_str += ALPHABETS[state_int % len(ALPHABETS)]
    return state_str

def decode_state(state_str):
    state_int = 0
    for char in state_str[::-1]:
        state_int *= len(ALPHABETS)
        state_int += ALPHABETS.find(char)
    return state_int

@csrf_exempt
def handle_savestate(request):
    if 'username' not in request:
        return {
            'result': False,
            'message': 'Missing username'
        }
    state_id = db.generate_id()
    username = request['username']

    files = db.execute_and_fetch_one(FILE_QUERY, (username,))
    if files is None:
        return {
            'result': False,
            'message': 'Invalid username'
        }

    author_file_id = files[0]
    review_file_id = files[1]
    submission_file_id = files[2]
    state_data = request['stateData'] if 'stateData' in request else ''
    db.insert('State', (state_id, username, author_file_id, submission_file_id, review_file_id, state_data))
    return {
        'result': True,
        'stateId': encode_state(state_id)
    }

@csrf_exempt
def handle_loadstate(request):
    if 'stateId' not in request:
        return {
            'result': False,
            'message': 'Missing state id'
        }
    if 'username' not in request:
        return {
            'result': False,
            'message': 'Missing username'
        }
    username = request['username']
    result = db.execute_and_fetch_one(STATE_SELECT, (decode_state(request['stateId']),))
    if result is None:
        return {
            'result': False,
            'message': 'Cannot find state id'
        }
    Storage.update_file_data(username, Storage.AUTHOR_TABLE, result[0])
    Storage.update_file_data(username, Storage.REVIEW_TABLE, result[1])
    Storage.update_file_data(username, Storage.SUBMISSION_TABLE, result[2])
    return {
        'result': True,
        'data': result[3]
    }