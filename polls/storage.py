import db as db

AUTHOR_TABLE = db.AUTHOR_TABLE
REVIEW_TABLE = db.REVIEW_TABLE
SUBMISSION_TABLE = db.SUBMISSION_TABLE

def saveData(type, columns, data):
    d = db.DB()
    d.setup()
    d.insert_many(type, columns, data)