import db as DB
import json
import processquery
from query import Query
from django.views.decorators.csrf import csrf_exempt

db = DB.DB()

FILE_QUERY = 'SELECT * FROM File WHERE username = ?'

QUERIES = {
    'get_all_author_uploads':
        Query('''
        SELECT submission_id, first_name, last_name, email, country, organization, webpage, person_num, corresponding
        FROM Author
        WHERE file_id = ?
        ''', [DB.AUTHOR_FILE_ID]),
    'get_all_submission_uploads':
        Query('''
        SELECT submission_id, track_id, track_name, title, authors, submitted, last_updated, form_fields, keywords, 
        decision, notified, reviews_sent, abstract
        FROM Submission
        WHERE file_id = ?
        ''', [DB.SUBMISSION_FILE_ID]),
    'get_all_review_uploads':
        Query('''
        SELECT review_id, submission_id, review_assignment_id, reviewer_name, field_id, review_comments, 
        evaluation_score, score, reviewer_first_name, reviewer_last_name, reviewer_email, reviewer_id, 
        submission_date, submission_time, recommendation
        FROM Review
        WHERE file_id = ?
        ''', [DB.REVIEW_FILE_ID]),
    'acceptance_by_author':
        Query('''
        SELECT A.first_name, A.last_name, COUNT(*), SUM(case decision when 'accept' then 1 else 0 end)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id
        WHERE A.file_id = ? AND S.file_id = ?
        GROUP BY A.person_num
        ORDER BY A.person_num ASC
        ''', [DB.AUTHOR_FILE_ID, DB.SUBMISSION_FILE_ID]),
    'acceptance_by_organization':
        Query('''
        SELECT A.organization, COUNT(*), SUM(case decision when 'accept' then 1 else 0 end)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id
        WHERE A.file_id = ? AND S.file_id = ?
        GROUP BY A.organization
        ORDER BY A.organization ASC
        ''', [DB.AUTHOR_FILE_ID, DB.SUBMISSION_FILE_ID]),
    'evaluation_score_by_organization':
        Query('''
        SELECT A.organization, AVG(R.score)
        FROM Author A 
        JOIN Review R ON A.submission_id = R.submission_id
        WHERE A.file_id = ? AND R.file_id = ?
        GROUP BY A.organization
        ORDER BY A.organization ASC
        ''', [DB.AUTHOR_FILE_ID, DB.REVIEW_FILE_ID]),
    'acceptance_rate_by_country':
        Query('''
        SELECT A.country, COUNT(*), SUM(case decision when 'accept' then 1 else 0 end)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id
        WHERE A.file_id = ? AND S.file_id  = ?
        GROUP BY A.country
        ORDER BY A.country ASC
        ''', [DB.AUTHOR_FILE_ID, DB.SUBMISSION_FILE_ID]),
    'evaluation_score_by_country':
        Query('''
        SELECT A.country, AVG(R.score)
        FROM Author A 
        JOIN Review R ON A.submission_id = R.submission_id
        WHERE A.file_id = ? AND R.file_id = ?
        GROUP BY A.country
        ORDER BY A.country ASC
        ''', [DB.AUTHOR_FILE_ID, DB.REVIEW_FILE_ID]),
    'keywords_by_organization':
        Query('''
        SELECT A.organization, S.keywords
        FROM Author A 
        JOIN Submission S ON A.submission_id = S.submission_id
        WHERE A.file_id = ? AND S.file_id = ?
        ''', [DB.AUTHOR_FILE_ID, DB.SUBMISSION_FILE_ID]),
    'keywords_by_country':
        Query('''
        SELECT A.country, S.keywords
        FROM Author A 
        JOIN Submission S ON A.submission_id = S.submission_id
        WHERE A.file_id = ? AND S.file_id = ?
        ''', [DB.AUTHOR_FILE_ID, DB.SUBMISSION_FILE_ID]),
    'keywords_by_track':
        Query('''
        SELECT S.track_name, S.keywords
        FROM Submission S
        WHERE S.decision = 'accept' AND S.file_id = ?
        ''', [DB.SUBMISSION_FILE_ID]),
    'search_paper':
        Query('''
        SELECT S.title, AVG(R.score)
        FROM Submission S 
        JOIN Review R ON S.submission_id = R.submission_id
        WHERE S.title LIKE ? AND R.file_id = ? AND S.file_id = ?
        GROUP BY S.title
        ''', [DB.REVIEW_FILE_ID, DB.SUBMISSION_FILE_ID])
}


@csrf_exempt
def handle_query(request):
    if 'username' not in request:
        return {
            'result': False,
            'message': 'Missing username'
        }
    if 'queryType' not in request or request['queryType'] not in QUERIES:
        return {
            'result': False,
            'message': 'Invalid query type'
        }
    username = request['username']
    files = db.execute_and_fetch_one(FILE_QUERY, (username,))
    if files is None:
        return {
            'result': False,
            'message': 'Invalid username'
        }

    query_type = request['queryType']
    params = []
    if 'params' in request:
        params = request['params']
    file_params = QUERIES[query_type].generate_params(files)
    if '' in file_params:
        return {
            'result': False,
            'message': 'Missing file'
        }
    result = db.execute_and_fetch(QUERIES[query_type].statement, params + file_params)
    if query_type in processquery.QUERY_POST_PROCESSORS:
        result = processquery.QUERY_POST_PROCESSORS[query_type](result)
    return {
        'result': True,
        'data': json.dumps(result)
    }
