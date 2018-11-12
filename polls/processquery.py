import operator
from collections import Counter
from utils import parseSubmissionTime

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

def process_all_authors(data):
    authorList, parsedResult = [], {}
    for authorInfo in data:
        # authorInfo = line.replace("\"", "").split(",")
        # print authorInfo
        authorList.append(
            {'name': authorInfo[1] + " " + authorInfo[2], 'country': authorInfo[4], 'affiliation': authorInfo[5]})

    authors = [ele['name'] for ele in authorList if
               ele]  # adding in the if ele in case of empty strings; same applies below
    topAuthors = Counter(authors).most_common(10)
    parsedResult['topAuthors'] = {'labels': [ele[0] for ele in topAuthors], 'data': [ele[1] for ele in topAuthors]}

    countries = [ele['country'] for ele in authorList if ele]
    topCountries = Counter(countries).most_common(10)
    parsedResult['topCountries'] = {'labels': [ele[0] for ele in topCountries],
                                    'data': [ele[1] for ele in topCountries]}

    affiliations = [ele['affiliation'] for ele in authorList if ele]
    topAffiliations = Counter(affiliations).most_common(10)
    parsedResult['topAffiliations'] = {'labels': [ele[0] for ele in topAffiliations],
                                       'data': [ele[1] for ele in topAffiliations]}

    return {'infoType': 'author', 'infoData': parsedResult}

def process_all_submission(data):
    parsedResult = {}
    acceptedSubmission = [line for line in data if str(line[9]) == 'accept']
    rejectedSubmission = [line for line in data if str(line[9]) == 'reject']

    acceptanceRate = float(len(acceptedSubmission)) / len(data)

    submissionTimes = [parseSubmissionTime(str(ele[5])) for ele in data]
    lastEditTimes = [parseSubmissionTime(str(ele[6])) for ele in data]
    submissionTimes = Counter(submissionTimes)
    lastEditTimes = Counter(lastEditTimes)
    timeStamps = sorted([k for k in submissionTimes])
    lastEditStamps = sorted([k for k in lastEditTimes])
    submittedNumber = [0 for n in range(len(timeStamps))]
    lastEditNumber = [0 for n in range(len(lastEditStamps))]
    timeSeries = []
    lastEditSeries = []
    for index, timeStamp in enumerate(timeStamps):
        if index == 0:
            submittedNumber[index] = submissionTimes[timeStamp]
        else:
            submittedNumber[index] = submissionTimes[timeStamp] + submittedNumber[index - 1]

        timeSeries.append({'x': timeStamp, 'y': submittedNumber[index]})

    for index, lastEditStamp in enumerate(lastEditStamps):
        if index == 0:
            lastEditNumber[index] = lastEditTimes[lastEditStamp]
        else:
            lastEditNumber[index] = lastEditTimes[lastEditStamp] + lastEditNumber[index - 1]

        lastEditSeries.append({'x': lastEditStamp, 'y': lastEditNumber[index]})

    # timeSeries = {'time': timeStamps, 'number': submittedNumber}
    # lastEditSeries = {'time': lastEditStamps, 'number': lastEditNumber}

    acceptedKeywords = [ele[8].encode('utf-8').lower().replace("\r", "").split("\n") for ele in acceptedSubmission]
    acceptedKeywords = [ele for item in acceptedKeywords for ele in item]
    acceptedKeywordMap = {k: v for k, v in Counter(acceptedKeywords).iteritems()}
    acceptedKeywordList = [[ele[0], ele[1]] for ele in Counter(acceptedKeywords).most_common(20)]

    rejectedKeywords = [ele[8].encode('utf-8').lower().replace("\r", "").split("\n") for ele in rejectedSubmission]
    rejectedKeywords = [ele for item in rejectedKeywords for ele in item]
    rejectedKeywordMap = {k: v for k, v in Counter(rejectedKeywords).iteritems()}
    rejectedKeywordList = [[ele[0], ele[1]] for ele in Counter(rejectedKeywords).most_common(20)]

    allKeywords = [ele[8].encode('utf-8').lower().replace("\r", "").split("\n") for ele in data]
    allKeywords = [ele for item in allKeywords for ele in item]
    allKeywordMap = {k: v for k, v in Counter(allKeywords).iteritems()}
    allKeywordList = [[ele[0], ele[1]] for ele in Counter(allKeywords).most_common(20)]

    tracks = set([str(ele[2]) for ele in data])
    paperGroupsByTrack = {track: [line for line in data if str(line[2]) == track] for track in tracks}
    keywordsGroupByTrack = {}
    acceptanceRateByTrack = {}
    comparableAcceptanceRate = {}
    topAuthorsByTrack = {}

    # Obtained from the JCDL.org website: past conferences
    comparableAcceptanceRate['year'] = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    comparableAcceptanceRate['Full Papers'] = [0.29, 0.28, 0.27, 0.29, 0.29, 0.30, 0.29, 0.30]
    comparableAcceptanceRate['Short Papers'] = [0.29, 0.37, 0.31, 0.31, 0.32, 0.50, 0.35, 0.32]
    for track, papers in paperGroupsByTrack.iteritems():
        keywords = [ele[8].encode('utf-8').lower().replace("\r", "").split("\n") for ele in papers]
        keywords = [ele for item in keywords for ele in item]
        # keywordMap = {k : v for k, v in Counter(keywords).iteritems()}
        keywordMap = [[ele[0], ele[1]] for ele in Counter(keywords).most_common(20)]
        keywordsGroupByTrack[track] = keywordMap

        acceptedPapersPerTrack = [ele for ele in papers if str(ele[9]) == 'accept']
        acceptanceRateByTrack[track] = float(len(acceptedPapersPerTrack)) / len(papers)

        acceptedPapersThisTrack = [paper for paper in papers if str(paper[9]) == 'accept']
        acceptedAuthorsThisTrack = [ele[4].encode('utf-8').replace(" and ", ", ").split(", ") for ele in acceptedPapersThisTrack]
        acceptedAuthorsThisTrack = [ele for item in acceptedAuthorsThisTrack for ele in item]
        topAcceptedAuthorsThisTrack = Counter(acceptedAuthorsThisTrack).most_common(10)
        topAuthorsByTrack[track] = {'names': [ele[0] for ele in topAcceptedAuthorsThisTrack],
                                    'counts': [ele[1] for ele in topAcceptedAuthorsThisTrack]}

        if track == "Full Papers" or track == "Short Papers":
            comparableAcceptanceRate[track].append(float(len(acceptedPapersPerTrack)) / len(papers))

    acceptedAuthors = [ele[4].encode('utf-8').replace(" and ", ", ").split(", ") for ele in acceptedSubmission]
    acceptedAuthors = [ele for item in acceptedAuthors for ele in item]
    topAcceptedAuthors = Counter(acceptedAuthors).most_common(10)
    topAcceptedAuthorsMap = {'names': [ele[0] for ele in topAcceptedAuthors],
                             'counts': [ele[1] for ele in topAcceptedAuthors]}
    # topAcceptedAuthors = {ele[0] : ele[1] for ele in Counter(acceptedAuthors).most_common(10)}

    parsedResult['acceptanceRate'] = acceptanceRate
    parsedResult['overallKeywordMap'] = allKeywordMap
    parsedResult['overallKeywordList'] = allKeywordList
    parsedResult['acceptedKeywordMap'] = acceptedKeywordMap
    parsedResult['acceptedKeywordList'] = acceptedKeywordList
    parsedResult['rejectedKeywordMap'] = rejectedKeywordMap
    parsedResult['rejectedKeywordList'] = rejectedKeywordList
    parsedResult['keywordsByTrack'] = keywordsGroupByTrack
    parsedResult['acceptanceRateByTrack'] = acceptanceRateByTrack
    parsedResult['topAcceptedAuthors'] = topAcceptedAuthorsMap
    parsedResult['topAuthorsByTrack'] = topAuthorsByTrack
    parsedResult['timeSeries'] = timeSeries
    parsedResult['lastEditSeries'] = lastEditSeries
    parsedResult['comparableAcceptanceRate'] = comparableAcceptanceRate

    return {'infoType': 'submission', 'infoData': parsedResult}

def process_all_review(data):
    parsedResult = {}
    evaluation = [str(line[6]).replace("\r", "") for line in data]
    submissionIDs = set([str(line[1]) for line in data])

    scoreList = []
    recommendList = []
    confidenceList = []

    submissionIDReviewMap = {}

    # Idea: from -3 to 3 (min to max scores possible), every 0.25 will be a gap
    scoreDistributionCounts = [0] * int((3 + 3) / 0.25)
    recommendDistributionCounts = [0] * int((1 - 0) / 0.1)

    scoreDistributionLabels = [" ~ "] * len(scoreDistributionCounts)
    recommendDistributionLabels = [" ~ "] * len(recommendDistributionCounts)

    for index, col in enumerate(scoreDistributionCounts):
        scoreDistributionLabels[index] = str(-3 + 0.25 * index) + " ~ " + str(-3 + 0.25 * index + 0.25)

    for index, col in enumerate(recommendDistributionCounts):
        recommendDistributionLabels[index] = str(0 + 0.1 * index) + " ~ " + str(0 + 0.1 * index + 0.1)

    for submissionID in submissionIDs:
        reviews = [str(line[6]).replace("\r", "") for line in data if str(line[1]) == submissionID]
        # print reviews
        confidences = [float(review.split("\n")[1].split(": ")[1]) for review in reviews]
        scores = [float(review.split("\n")[0].split(": ")[1]) for review in reviews]

        confidenceList.append(sum(confidences) / len(confidences))
        # recommends = [1.0 for review in reviews if review.split("\n")[2].split(": ")[1] == "yes" else 0.0]
        try:
            recommends = map(lambda review: 1.0 if review.split("\n")[2].split(": ")[1] == "yes" else 0.0, reviews)
        except:
            recommends = [0.0 for n in range(len(reviews))]
        weightedScore = sum(x * y for x, y in zip(scores, confidences)) / sum(confidences)
        weightedRecommend = sum(x * y for x, y in zip(recommends, confidences)) / sum(confidences)

        scoreColumn = min(int((weightedScore + 3) / 0.25), 23)
        recommendColumn = min(int((weightedRecommend) / 0.1), 9)
        scoreDistributionCounts[scoreColumn] += 1
        recommendDistributionCounts[recommendColumn] += 1
        submissionIDReviewMap[submissionID] = {'score': weightedScore, 'recommend': weightedRecommend}
        scoreList.append(weightedScore)
        recommendList.append(weightedRecommend)

    parsedResult['IDReviewMap'] = submissionIDReviewMap
    parsedResult['scoreList'] = scoreList
    parsedResult['meanScore'] = sum(scoreList) / len(scoreList)
    parsedResult['meanRecommend'] = sum(recommendList) / len(recommendList)
    parsedResult['meanConfidence'] = sum(confidenceList) / len(confidenceList)
    parsedResult['recommendList'] = recommendList
    parsedResult['scoreDistribution'] = {'labels': scoreDistributionLabels, 'counts': scoreDistributionCounts}
    parsedResult['recommendDistribution'] = {'labels': recommendDistributionLabels,
                                             'counts': recommendDistributionCounts}

    return {'infoType': 'review', 'infoData': parsedResult}


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
    'get_all_author_uploads': process_all_authors,
    'get_all_submission_uploads': process_all_submission,
    'get_all_review_uploads': process_all_review,
}
