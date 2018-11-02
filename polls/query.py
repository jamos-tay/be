import db as DB
import json
from django.views.decorators.csrf import csrf_exempt

db = DB.DB()

QUERIES = {
    'acceptance_by_author' :
        '''
        SELECT A.person_num, A.first_name, A.last_name, COUNT(*), COUNT(decision)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id AND S.decision = 'accept'
        GROUP BY A.person_num
        ORDER BY A.person_num ASC
        ''',
    'acceptance_by_organization':
        '''
        SELECT A.organization, COUNT(*), COUNT(decision)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id AND S.decision = 'accept'
        GROUP BY A.organization
        ORDER BY A.organization ASC
        ''',
    'evaluation_score_by_organization':
        '''
        SELECT A.organization, AVG(R.score)
        FROM Author A 
        JOIN Review R ON A.submission_id = R.submission_id
        GROUP BY A.organization
        ORDER BY A.organization ASC
        ''',
    'keywords_by_organization':
        '''
        SELECT DISTINCT A.organization, S.keywords
        FROM Author A 
        JOIN Submission S ON A.submission_id = S.submission_id
        ''',
    'acceptance_rate_by_country':
        '''
        SELECT A.country, COUNT(*), COUNT(decision)
        FROM Author A 
        LEFT JOIN Submission S ON A.submission_id = S.submission_id AND S.decision = 'accept'
        GROUP BY A.country
        ORDER BY A.country ASC
        ''',
    'evaluation_score_by_country':
        '''
        SELECT A.country, AVG(R.score)
        FROM Author A 
        JOIN Review R ON A.submission_id = R.submission_id
        GROUP BY A.country
        ORDER BY A.country ASC
        ''',
    'search_paper':
        '''
        SELECT S.title, AVG(R.score)
        FROM Submission S 
        JOIN Review R ON S.submission_id = R.submission_id
		WHERE S.title LIKE ?
		GROUP BY S.title
        '''
}

@csrf_exempt
def handle_query(request):
    if 'queryType' not in request or request['queryType'] not in QUERIES:
        return {
            'result': False,
            'message': 'Invalid query type'
        }
    query_type = request['queryType']
    params = []
    if 'params' in request:
        params = request['params']
    result = db.execute_and_fetch(QUERIES[query_type], params)
    return {
        'result': True,
        'data': json.dumps(result)
    }
