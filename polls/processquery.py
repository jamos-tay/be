import operator

def process_acceptance_by_author(data):
    # [A.first_name, A.last_name, COUNT(*), COUNT(decision)]
    result = []
    for row in data:
        result.append([row[0] + ' ' + row[1], (row[3] / float(row[2])) if row[2] > 0 else 0])

    result = sorted(result, key=operator.itemgetter(1), reverse=True)[:10]

    return {"counts": map(lambda row: row[1], result), "names": map(lambda row: row[0], result)}


def process_acceptance_rate_by_country(data):
    # [A.country, COUNT(*), COUNT(decision)]
    result = []
    for row in data:
        result.append([row[0], (row[2] / float(row[1])) if row[1] > 0 else 0])

    result = sorted(result, key=operator.itemgetter(1), reverse=True)[:10]
    return {"counts": map(lambda row: row[1], result), "names": map(lambda row: row[0], result)}

def process_acceptance_by_organization(data):
    # [A.organization, COUNT(*), COUNT(decision)]
    result = []
    for row in data:
        result.append([row[0], (row[2] / float(row[1])) if row[1] > 0 else 0])

    result = sorted(result, key=operator.itemgetter(1), reverse=True)[:10]
    return {"counts": map(lambda row: row[1], result), "names": map(lambda row: row[0], result)}

def process_evaluation_score_by_organization(data):
    # [A.organization, AVG(R.score)]
    result = data

    result = sorted(result, key=operator.itemgetter(1), reverse=True)[:10]
    return {"counts": map(lambda row: row[1], result), "names": map(lambda row: row[0], result)}

def process_evaluation_score_by_country(data):
    # [A.country, AVG(R.score)]
    result = data

    result = sorted(result, key=operator.itemgetter(1), reverse=True)[:10]
    return {"counts": map(lambda row: row[1], result), "names": map(lambda row: row[0], result)}


def flatten(data):
    flattened = []
    for keyword in data:
        flattened.append([keyword, data[keyword]])
    return flattened

def process_keywords_by_organization(data):
    # [A.organization, S.keywords]
    result = {}
    for row in data:
        if row[0] not in result:
            result[row[0]] = {}
        keywords = row[1].split('\n')
        for keyword in keywords:
            if keyword not in result[row[0]]:
                result[row[0]][keyword] = 0
            result[row[0]][keyword] += 1

    for key in result:
        result[key] = flatten(result[key])
    return result

def process_keywords_by_country(data):
    # [A.country, S.keywords]
    result = {}
    for row in data:
        if row[0] not in result:
            result[row[0]] = {}
        keywords = row[1].split('\n')
        for keyword in keywords:
            if keyword not in result[row[0]]:
                result[row[0]][keyword] = 0
            result[row[0]][keyword] += 1

    for key in result:
        result[key] = flatten(result[key])
    return result

def process_keywords_by_track(data):
    # [S.track_name, S.keywords]
    result = {}
    for row in data:
        if row[0] not in result:
            result[row[0]] = {}
        keywords = row[1].split('\n')
        for keyword in keywords:
            if keyword not in result[row[0]]:
                result[row[0]][keyword] = 0
            result[row[0]][keyword] += 1

    for key in result:
        result[key] = flatten(result[key])
    return result

def process_search_paper(data):
    return data

QUERY_POST_PROCESSORS = {
    'acceptance_by_author': process_acceptance_by_author,
    'acceptance_by_organization': process_acceptance_by_organization,
    'evaluation_score_by_organization': process_evaluation_score_by_organization,
    'acceptance_rate_by_country': process_acceptance_rate_by_country,
    'evaluation_score_by_country': process_evaluation_score_by_country,
    'keywords_by_organization': process_keywords_by_organization,
    'keywords_by_country': process_keywords_by_country,
    'search_paper': process_search_paper,
    'keywords_by_track':  process_keywords_by_track,
}
