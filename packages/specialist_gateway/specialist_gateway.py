import urllib

from kearch_common.data_format import get_payload
from kearch_common.requester import KearchRequester

META_PORT = 10080

QUERY_PROCESSOR_HOST = 'sp-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080
REQUESTER_NAME = 'specialist_gateway'


def retrieve(queries, max_urls):
    kr = KearchRequester(QUERY_PROCESSOR_HOST,
                         QUERY_PROCESSOR_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': ' '.join(queries), 'max_urls': max_urls})
    return results


def send_DB_summary(host_sp, host_me, summary):
    d = dict()
    d['host'] = host_sp
    d['summary'] = summary

    kr = KearchRequester(host_me, META_PORT, REQUESTER_NAME)
    result = kr.request(path='/add_new_sp_server', method='POST',
                        payload=d)
    return result
