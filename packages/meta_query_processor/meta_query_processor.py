from kearch_common.requester import KearchRequester

DATABASE_IP = '192.168.11.10'
DATABASE_PORT = '10080'
REQUESTER_NAME = 'meta_query_processor'

COMMUNICATOR_IP = '192.168.11.11'
COMMUNICATOR_PORT = '10080'


# When you change DEBUG_UNIT_TEST true, this program run unit test.
DEBUG_UNIT_TEST = False


class MeQueryProcessorException(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)


def get_sp_ip_from_database(queries, max_urls):
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
            DATABASE_IP, DATABASE_PORT, REQUESTER_NAME)
        ret = database_requester.request(
            path='/retrieve', params={'queries': queries, max_urls: max_urls})
        return ret


def get_result_from_sp(sp_ip, queries, max_urls):
    if DEBUG_UNIT_TEST:
        ret = dict()
        ret['data'] = [{'url': 'www.google.com', 'title_words': [
            'google', 'usa'], 'title': 'google_in_usa', 'summary':'google is strong', 'score':11.0}]
        return ret
    else:
        sp_requester = KearchRequester(
            COMMUNICATOR_IP, COMMUNICATOR_PORT, REQUESTER_NAME)
        ret = sp_requester.request(
            path='/retrieve', params={'sp_ip': sp_ip, 'queries': queries, max_urls: max_urls})
        return ret


def retrieve(queries, max_urls):
    sp_data = get_sp_ip_from_database(queries, max_urls)
    ip_to_score = dict()
    for d in sp_data.values():
        for ip, freq in d.items():
            if ip in ip_to_score:
                ip_to_score[ip] += freq
            else:
                ip_to_score[ip] = freq
    if len(ip_to_score) == 0:
        raise MeQueryProcessorException(
            'No specialist server in this meta database.')

    ip_to_score_list = list(ip_to_score.items())
    ip_to_score_list.sort(key=lambda x: x[1], reverse=True)
    best_ip = ip_to_score_list[0][0]
    res = get_result_from_sp(best_ip, queries, max_urls)
    return res
