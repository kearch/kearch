from kearch_common.requester import KearchRequester

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'specialist_query_processor'
TFIDF_COEFFICIENT = 1.0


def calculate_score(queries, result):
    overlap_title = False
    for w in result['title_words']:
        if w in queries:
            overlap_title = True
    sum_tfidf = 0
    for w in queries:
        sum_tfidf = sum_tfidf + float(getattr(result['tfidf'], w, 0))
    ret = 0
    if overlap_title:
        ret = 1
    ret = ret + TFIDF_COEFFICIENT * sum_tfidf
    return ret


test_results = {'data': [{'url': 'www.google.com', 'title_words': ['facebook', 'amazon'],
                          'summary': 'Hello world!', 'tfidf': {'google': 1.0, 'facebook': 2.0}}]}


def retrieve(queries, max_urls):
    database_requester = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')

    results = database_requester.request(
        path='/retrieve_webpages',
        params={'queries': queries, 'max_urls': max_urls})
    # Debug Code: Uncomment a following line when you want this module standalone.
    # results = test_results

    ret = {'data': []}
    for r in results['data']:
        # If Flask cannnot convert data to correct format, I must convert them by hand.
        d = {'url': r['url'],
             'title': r['title'],
             'title_words': r['title_words'],
             'summary': r['summary'],
             'score': calculate_score(queries, r)}
        ret['data'].append(d)
    return ret
