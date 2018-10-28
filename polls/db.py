import sqlite3

USER_TABLE = 'User'
TOKENS_TABLE = 'Tokens'
AUTHOR_TABLE = 'Author'
REVIEW_TABLE = 'Review'
SUBMISSION_TABLE = 'Submission'
STATE_TABLE = 'State'

class DB:

    def reset(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS ' + USER_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + TOKENS_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + AUTHOR_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + REVIEW_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + SUBMISSION_TABLE)
        c.execute('DROP TABLE IF EXISTS ' + STATE_TABLE)
        conn.commit()
        conn.close()
        self.setup()

    def setup(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + USER_TABLE + '(' +
                  'username text PRIMARY KEY, ' +
                  'salt text, ' +
                  'password text' +
                  ')')
        c.execute('CREATE TABLE IF NOT EXISTS ' + TOKENS_TABLE + '(' +
                  'username text, ' +
                  'token text, ' +
                  'expiry integer, ' +
                  'FOREIGN KEY(username) REFERENCES ' + USER_TABLE + '(username)' +
                  ')')
        c.execute('CREATE TABLE IF NOT EXISTS ' + AUTHOR_TABLE + '(' +
                  'file_id integer, ' +
                  'username text, ' +
                  'submission_id integer, first_name text, last_name text, email text, country text, organization text, webpage text, person_num integer, corresponding text,' +
                  'FOREIGN KEY(username) REFERENCES ' + USER_TABLE + '(username)' +
                  ')')
        c.execute('CREATE TABLE IF NOT EXISTS ' + REVIEW_TABLE + ' (' +
                  'file_id integer, ' +
                  'username text, ' +
                  'review_id integer, submission_id integer, review_assignment_id integer, reviewer_name text, field_id integer, review_comments text, evaluation_score text, score integer, reviewer_first_name text, reviewer_last_name text, reviewer_email text, reviewer_id text, submission_date text, submission_time text, recommendation text, ' +
                  'FOREIGN KEY(username) REFERENCES ' + USER_TABLE + '(username)' +
                  ')')
        c.execute('CREATE TABLE IF NOT EXISTS ' + SUBMISSION_TABLE + ' (' +
                  'file_id integer, ' +
                  'username text, ' +
                  'submission_id integer, track_id integer, track_name text, title text, authors text, submitted text, last_updated text, form_fields text, keywords text, decision text, notified text, reviews_sent text, abstract text, ' +
                  'FOREIGN KEY(username) REFERENCES ' + USER_TABLE + '(username)' +
                  ')')
        c.execute('CREATE TABLE IF NOT EXISTS ' + STATE_TABLE + ' (' +
                  'state_id integer PRIMARY KEY, ' +
                  'username text, ' +
                  'author_file_id integer, ' +
                  'review_file_id integer, ' +
                  'submission_file_id integer, ' +
                  'state_data text, ' +
                  'FOREIGN KEY(username) REFERENCES ' + USER_TABLE + '(username),' 
                  'FOREIGN KEY(author_file_id) REFERENCES ' + AUTHOR_TABLE + '(file_id),' +
                  'FOREIGN KEY(review_file_id) REFERENCES ' + REVIEW_TABLE + '(file_id),' +
                  'FOREIGN KEY(submission_file_id) REFERENCES ' + SUBMISSION_TABLE + '(file_id)' +
                  ')')
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

    def insert_many(self, table, prepended_columns, prepended_data, columns, data):
        conn = sqlite3.connect('data.db')
        conn.text_factory = str
        c = conn.cursor()
        prepended_column_names = '' if len(prepended_columns) == 0 else ','.join(prepended_columns) + ','
        column_names = ','.join(columns)
        param_placeholders = ','.join('?' * (len(prepended_data) + len(data[0])))
        for row in data:
            try:
                c.execute('INSERT INTO ' + table + ' (' + prepended_column_names + column_names + ') ' +
                          'VALUES (' + param_placeholders + ')', prepended_data + row)
            except Exception as e:
                print str(e)
                print "Could not insert " + str(row)
        conn.commit()
        conn.close()
