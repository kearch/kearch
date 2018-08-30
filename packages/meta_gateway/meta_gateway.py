from kearch_common.requester import KearchRequester
from kearch_common.data_format import get_payload

import urllib
import requests

SPECIALIST_GATEWAY_PORT = 10080

DATABASE_IP = '192.168.11.05'
DATABASE_PORT = 10080
REQUESTER_NAME = 'meta_gateway'

def retrieve(ip_sp, queries, max_urls):
    kr = KearchRequester(ip_sp, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    response = kr.request(path='/retrieve', method='GET', payload={'queries': queries, 'max_urls': MAX_URLS})
    results = get_payload(response)
    return results


def add_new_sp_server(ip_sp, summary):
    kr = KearchRequester(DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)
    kr.request(path='/add_new_sp_server', method='POST', payload={'ip':ip_sp,'summary':summary})
