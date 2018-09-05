from kearch_common.requester import KearchRequester

SPECIALIST_GATEWAY_PORT = 10080

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 10080
REQUESTER_NAME = 'meta_gateway'


def retrieve(sp_host, queries, max_urls):
    kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': queries, 'max_urls': max_urls})
    return results


def add_new_sp_server(sp_host, summary):
    kr = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME)
    result = kr.request(path='/add_new_sp_server', method='POST',
                        payload={'host': sp_host, 'summary': summary})
    return result
