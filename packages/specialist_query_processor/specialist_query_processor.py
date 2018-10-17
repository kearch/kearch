from kearch_common.requester import KearchRequester
import sys

ELASTIC_HOST = 'sp-es.kearch.svc.cluster.local'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'sp'
ELASTIC_TYPE = 'webpage'

REQUESTER_NAME = 'specialist_query_processor'

test_results = {
    'data': [['www.google.com', 'google home', 'google is strong']]}


def retrieve(queries, max_urls):
    elastic_requester = KearchRequester(
        ELASTIC_HOST, ELASTIC_PORT, REQUESTER_NAME, conn_type='elastic')

    resp = elastic_requester.request(
        path='/' + ELASTIC_INDEX + '/' + ELASTIC_TYPE + '/_search?pretty',
        payload={'query': {'match': {'text': queries[0]}}},
        method='POST')

    print(resp['hits']['hits'], file=sys.stderr)
    results = {'data': []}
    for d in resp['hits']['hits']:
        results['data'].append(
            [d['_source']['url'], d['_source']['title'], d['_source']['text'][0:200]])

    # Debug : Uncomment a following line when you want this module standalone.
    # results = test_results

    return results
