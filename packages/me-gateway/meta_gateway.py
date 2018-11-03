from kearch_common.requester import KearchRequester

SPECIALIST_GATEWAY_PORT = 32500

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 10080
REQUESTER_NAME = 'meta_gateway'


def retrieve(sp_host, queries, max_urls):
    kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': queries, 'max_urls': max_urls})
    return results


def add_new_sp_server(sp_host, summary):
    kr = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    result = kr.request(path='/add_new_sp_server',
                        payload={'host': sp_host, 'summary': summary})
    return result


def fetch_a_dump(sp_host):
    kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    results = kr.request(path='/sp/gateway/get_a_dump', method='GET')
    return results
