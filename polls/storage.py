import db as db
import time

AUTHOR_TABLE = db.AUTHOR_TABLE
REVIEW_TABLE = db.REVIEW_TABLE
SUBMISSION_TABLE = db.SUBMISSION_TABLE


def save_data(username, type, columns, data):
    d = db.DB()
    d.setup()
    file_id = d.generate_id()
    d.insert_many(type, ['file_id', 'username'], [file_id, username], columns, data)
    return file_id