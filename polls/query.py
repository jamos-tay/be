import db

FILE_PARAM_POSITION_MAP = {
    db.AUTHOR_FILE_ID : 1,
    db.REVIEW_FILE_ID : 2,
    db.SUBMISSION_FILE_ID : 3
}

class Query():
    statement = ''
    files = []

    def __init__(self, statement, files):
        self.statement = statement
        self.files = list(map(lambda file: FILE_PARAM_POSITION_MAP[file], files))

    def generate_params(self, params):
        return list(map(lambda file: params[file], self.files))