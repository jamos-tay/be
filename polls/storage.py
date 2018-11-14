import db as db
import time

AUTHOR_TABLE = db.AUTHOR_TABLE
REVIEW_TABLE = db.REVIEW_TABLE
SUBMISSION_TABLE = db.SUBMISSION_TABLE

d = db.DB()
d.setup()

def save_data(username, type, columns, data):
    file_id = d.generate_id()
    num_failed, num_success = d.insert_many(type, ['file_id', 'username'], [file_id, username], columns, data)
    if num_success > 0:
        update_file_data(username, type, file_id)
    return num_failed, num_success

def update_file_data(username, type, file_id):
    d.insert('File', (username, '', '', ''), True)
    d.execute('UPDATE File SET ' + db.ID_MAP[type] + ' = ? WHERE username = ?', (file_id, username,))
