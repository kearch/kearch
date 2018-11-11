import sys
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
REQUESTER_NAME = 'meta_query_processor'

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080


# When you change DEBUG_UNIT_TEST true, this program run unit test.
DEBUG_UNIT_TEST = False


class MeQueryProcessorException(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)


def get_sp_host_from_database(queries):
    if DEBUG_UNIT_TEST:
        ret = dict()
        for q in queries:
            d = dict()
            d['10.229.55.117'] = 167
            d['14.229.55.117'] = 127
            ret[q] = d
        return ret
    else:
        database_requester = KearchRequester(
            DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type="sql")
        ret = database_requester.request(
            path='/retrieve_sp_servers', params={'queries': queries})
        return ret


def get_result_from_sp(sp_host, queries, max_urls):
    ret = dict()
    if DEBUG_UNIT_TEST:
        ret['data'] = [{'url': 'www.google.com', 'title_words': [
            'google', 'usa'], 'title': 'google_in_usa', 'summary':'google is strong', 'score':11.0}]
    else:
        sp_requester = KearchRequester(
            GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
        ret = sp_requester.request(
            path='/retrieve',
            params={'sp_host': sp_host, 'queries': ' '.join(queries), 'max_urls': max_urls})
    ret['sp_host'] = sp_host
    return ret


def retrieve(queries, max_urls, sp=None):
    if sp is None:
        sp_data = get_sp_host_from_database(queries)
        host_to_score = dict()
        for d in sp_data.values():
            for host, freq in d.items():
                if host in host_to_score:
                    host_to_score[host] += freq
                else:
                    host_to_score[host] = freq
        if len(host_to_score) == 0:
            sys.stderr.write("No specialist server in this meta database.\n")
            return {
                'data': [],
                'sp_host': ''
            }

        host_to_score_list = list(host_to_score.items())
        host_to_score_list.sort(key=lambda x: x[1], reverse=True)
        best_host = host_to_score_list[0][0]
    else:
        best_host = sp
    res = get_result_from_sp(best_host, queries, max_urls)
    return res
