from kearch_common.requester import KearchRequester
import sys

ELASTIC_HOST = 'sp-es.kearch.svc.cluster.local'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'sp'
ELASTIC_TYPE = 'webpage'

REQUESTER_NAME = 'specialist_query_processor'


def retrieve(queries, max_urls):
    elastic_requester = KearchRequester(
        ELASTIC_HOST, ELASTIC_PORT, REQUESTER_NAME, conn_type='elastic')

    query = ' '.join(queries)
    payload = {'query': {'multi_match': {'query': query,
                                         'type': 'phrase',
                                         'fields': ['title', 'text']}}}
    resp = elastic_requester.request(
        path='/' + ELASTIC_INDEX + '/' + ELASTIC_TYPE + '/_search?pretty',
        payload=payload, method='POST')

    hits = []
    if 'hits' in resp and 'hits' in resp['hits']:
        hits = resp['hits']['hits']

    print(hits, file=sys.stderr)
    results = {'data': []}
    for d in hits:
        results['data'].append(
            {'url': d['_source']['url'],
             'title': d['_source']['title'],
             'summary': d['_source']['text'][0:200],
             'score': d['_score']})

    return results
