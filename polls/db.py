import sqlite3

USER_TABLE = 'User'
TOKENS_TABLE = 'Tokens'
AUTHOR_TABLE = 'Author'
REVIEW_TABLE = 'Review'
SUBMISSION_TABLE = 'Submission'

class DB:

    def reset(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS ' + USER_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + TOKENS_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + AUTHOR_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + REVIEW_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + SUBMISSION_TABLE)
        conn.commit()
        conn.close()
        self.setup()

    def setup(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + USER_TABLE + ' (username text PRIMARY KEY, salt integer, password text)')
        c.execute('CREATE TABLE IF NOT EXISTS ' + TOKENS_TABLE + ' (username text, token text, expiry integer)')
        c.execute('CREATE TABLE IF NOT EXISTS ' + AUTHOR_TABLE + ' (submission_id integer, first_name text, last_name text, email text, country text, organization text, webpage text, person_num integer, corresponding text)')
        c.execute('CREATE TABLE IF NOT EXISTS ' + REVIEW_TABLE + ' (review_id integer, submission_id integer, review_assignment_id integer, reviewer_name text, field_id integer, review_comments text, evaluation_score text, score integer, reviewer_first_name text, reviewer_last_name text, reviewer_email text, reviewer_id text, submission_date text, submission_time text, recommendation text)')
        c.execute('CREATE TABLE IF NOT EXISTS ' + SUBMISSION_TABLE + ' (submission_id integer, track_id integer, track_name text, title text, authors text, submitted text, last_updated text, form_fields text, keywords text, decision text, notified text, reviews_sent text, abstract text)')
        conn.commit()
        conn.close()

    def execute_and_fetch_one(self, statement, params):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(statement, params)
        result =  c.fetchone()
        return result

    def insert(self, table, params):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO ' + table + ' VALUES (' + ','.join('?' * len(params)) + ')', params)
        conn.commit()
        conn.close()

    def insert_many(self, table, columns, data):
        conn = sqlite3.connect('data.db')
        conn.text_factory = str
        c = conn.cursor()
        column_names = ','.join(columns)
        param_placeholders = ','.join('?' * len(data[0]))
        for row in data:
            try:
                c.execute('INSERT INTO ' + table + ' (' + column_names + ') VALUES (' + param_placeholders + ')', tuple(row))
            except Exception as e:
                pass
                # print str(e)
                # print "Could not insert " + str(row)
        conn.commit()
        conn.close()