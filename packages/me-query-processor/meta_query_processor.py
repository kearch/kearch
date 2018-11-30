from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
EVALUATER_HOST = 'me-evaluater.kearch.svc.cluster.local'
EVALUATER_PORT = 10080
GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080
REQUESTER_NAME = 'meta_query_processor'
SP_HOST_RATIO = [8, 1, 1]


class MeQueryProcessorException(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)


def get_result_from_sp(sp_host, query, max_urls):
    g_req = KearchRequester(GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    r = g_req.request(
        path='/retrieve',
        params={'sp_host': sp_host, 'queries': query, 'max_urls': max_urls})
    res = list()
    for d in r['data']:
        d['sp_host'] = sp_host
        res.append(d)
    return res


def retrieve(query, max_urls, sp=None):
    if sp is None:
        e_req = KearchRequester(EVALUATER_HOST, EVALUATER_PORT, REQUESTER_NAME)
        sp_hosts = e_req.request(path='/me/evaluater/evaluate',
                                 params={'query': query})
        a = list(sp_hosts.items())
        a.sort(key=lambda x: x[1], reverse=True)
        n = min(len(SP_HOST_RATIO), len(a))
        res = list()
        for i in range(0, n):
            m = max_urls * SP_HOST_RATIO[i] / sum(SP_HOST_RATIO[:n])
            res.extend(get_result_from_sp(a[i][0], query, m))
        return {'data': res}
    else:
        res = get_result_from_sp(sp, query, max_urls)
        return {'data': res}
