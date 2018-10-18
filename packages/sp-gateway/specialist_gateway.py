from kearch_common.requester import KearchRequester

META_GATEWAY_PORT = 32400

QUERY_PROCESSOR_HOST = 'sp-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080
REQUESTER_NAME = 'specialist_gateway'


def retrieve(queries, max_urls):
    kr = KearchRequester(QUERY_PROCESSOR_HOST,
                         QUERY_PROCESSOR_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': ' '.join(queries), 'max_urls': max_urls})
    return results


def send_DB_summary(sp_host, me_host, summary):
    d = dict()
    d['host'] = sp_host
    d['summary'] = summary

    kr = KearchRequester(me_host, META_GATEWAY_PORT, REQUESTER_NAME)
    result = kr.request(path='/add_new_sp_server', method='POST',
                        payload=d)
    return result
