from kearch_common.requester import KearchRequester
import sys

ELASTIC_HOST = 'sp-es.kearch.svc.cluster.local'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'sp'
ELASTIC_TYPE = 'webpage'


def retrieve(queries, max_urls):
    elastic_requester = KearchRequester(
        ELASTIC_HOST, ELASTIC_PORT, conn_type='elastic')

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
    results = []
    for d in hits:
        results.append(
            {'url': d['_source']['url'],
             'title': d['_source']['title'],
             'description': d['_source']['text'][0:200],
             'score': d['_score']})

    return results


def test_retrieve():
    for q in ['google', 'linux', 'linux kernel']:
        results = retrieve(q, 100)
        for r in results:
            assert('url' in r)
            assert('title' in r)
            assert('description' in r)
            assert('score' in r)
