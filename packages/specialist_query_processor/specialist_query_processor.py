from kearch_common.requester import KearchRequester
from kearch_common.data_format import get_payload

DATABASE_IP = '192.168.11.11'
DATABASE_PORT = 10080

REQUESTER_NAME = 'specialist_query_processor'
TFIDF_COEFFICIENT = 1.0


def calculate_score(queries, result):
    overlap_title = False
    for w in result['title_words']:
        if w in queries:
            overlap_title = True
    sum_tfidf = 0
    for w in queries:
        sum_tfidf = sum_tfidf + float(result['tfidf'][w])
    ret = 0
    if overlap_title:
        ret = 1
    ret = ret + TFIDF_COEFFICIENT * sum_tfidf
    return ret


test_results = {'data': [{'url': 'www.google.com', 'title_words': ['facebook', 'amazon'],
                          'summary': 'Hello world!', 'tfidf': {'google': 1.0, 'facebook': 2.0}}]}


def retrieve(queries, max_urls):
    database_requester = KearchRequester(
        DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)

    response = database_requester.request(
        path='/retrieve', method='GET', payload={'queries': queries, 'max_urls': max_urls})
    results = get_payload(response)
    # Debug Code: Uncomment a following line when you want this module standalone.
    # results = test_results

    ret = {'data': []}
    for r in results['data']:
        # If Flask cannnot convert data to correct format, I must convert them by hand.
        d = {'url': r['url'], 'title_words': r['title_words'],
             'summary': r['summary'], 'score': calculate_score(queries, r)}
        ret['data'].append(d)
    return ret
