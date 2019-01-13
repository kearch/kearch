from kearch_common.requester import KearchRequester
from concurrent.futures import ThreadPoolExecutor

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
EVALUATER_HOST = 'me-evaluater.kearch.svc.cluster.local'
EVALUATER_PORT = 10080
GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080
ME_GATEWAY_BASEURL = '/v0/me/gateway/'
SP_HOST_RATIO = [8, 1, 1]
NUM_THREAD = 10


class MeQueryProcessorException(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)


def get_result_from_sp(sp_host, query, max_urls):
    gw_req = KearchRequester(GATEWAY_HOST, GATEWAY_PORT)
    r = gw_req.request(
        path=ME_GATEWAY_BASEURL + 'retrieve',
        params={'sp_host': sp_host, 'queries': query, 'max_urls': max_urls})
    res = list()
    for d in r['data']:
        d['sp_host'] = sp_host
        res.append(d)
    return res


def get_result_from_sp_tuple(t):
    return get_result_from_sp(t[0], t[1], t[2])


def retrieve(query, max_urls, sp=None):
    if sp is None:
        e_req = KearchRequester(EVALUATER_HOST, EVALUATER_PORT)
        sp_hosts = e_req.request(path='/me/evaluater/evaluate',
                                 params={'query': query})
        a = list(sp_hosts.items())
        a.sort(key=lambda x: x[1], reverse=True)
        n = min(len(SP_HOST_RATIO), len(a))

        args = list()
        for i in range(0, n):
            m = max_urls * SP_HOST_RATIO[i] / sum(SP_HOST_RATIO[:n])
            args.append((a[i][0], query, m))
        res = list()
        with ThreadPoolExecutor(max_workers=NUM_THREAD) as executor:
            r = list(executor.map(get_result_from_sp_tuple, args))
            for a in r:
                res.extend(a)

        return {'data': res}
    else:
        res = get_result_from_sp(sp, query, max_urls)
        return {'data': res}
