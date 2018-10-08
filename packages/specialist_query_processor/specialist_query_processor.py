from kearch_common.requester import KearchRequester

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'specialist_query_processor'
TFIDF_COEFFICIENT = 1.0


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

    return results
