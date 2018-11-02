from django.views.decorators.csrf import csrf_exempt
import db as DB

db = DB.DB()

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
    author_file_id = request['authorFileId'] if 'authorFileId' in request else ''
    submission_file_id = request['submissionFileId'] if 'submissionFileId' in request else ''
    review_file_id = request['reviewFileId'] if 'reviewFileId' in request else ''
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
    result = db.execute_and_fetch_one(STATE_SELECT, (decode_state(request['stateId']),))
    if len(result) == 0:
        return {
            'result': False,
            'message': 'Cannot find state id'
        }
    return {
        'result': True,
        'data': result
    }