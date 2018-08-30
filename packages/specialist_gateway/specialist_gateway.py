from kearch_common.requester import KearchRequester
from kearch_common.data_format import get_payload

import urllib
import requests

META_PORT = 10080

QUERY_PROCESSOR_IP = '192.168.11.05'
QUERY_PROCESSOR_PORT = 10080
REQUESTER_NAME = 'specialist_gateway'


def retrieve(queries, max_urls):
    kr = KearchRequester(QUERY_PROCESSOR_IP,
                         QUERY_PROCESSOR_PORT, REQUESTER_NAME)
    response = kr.request(path='/retrieve', method='GET',
                          payload={'queries': queries, 'max_urls': MAX_URLS})
    results = get_payload(response)
    return results


def send_DB_summary(ip_sp, ip_me, summary):
    url = urllib.parse.urljoin(
        '{}:{}'.format(ip_me, META_PORT), 'add_new_sp_server')
    d = dict()
    d['ip'] = ip_sp
    d['summary'] = summary
    resp = requests.request('POST', url, json=d)
