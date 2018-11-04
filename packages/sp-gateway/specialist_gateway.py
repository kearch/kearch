from kearch_common.requester import KearchRequester

META_GATEWAY_PORT = 32400

QUERY_PROCESSOR_HOST = 'sp-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'specialist_gateway'


def retrieve(queries, max_urls):
    kr = KearchRequester(QUERY_PROCESSOR_HOST,
                         QUERY_PROCESSOR_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': ' '.join(queries),
                                 'max_urls': max_urls})
    return results


def send_DB_summary(sp_host, me_host, summary):
    d = dict()
    d['host'] = sp_host
    d['summary'] = summary

    kr = KearchRequester(me_host, META_GATEWAY_PORT, REQUESTER_NAME)
    result = kr.request(path='/add_new_sp_server', method='POST',
                        payload=d)
    return result


def get_a_dump(me_host):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    reqs = db_req.request(path='/sp/db/get_connection_requests')
    if me_host in reqs['out'] and not reqs['out'][me_host]:
        db_req.request(path='/sp/db/approve_a_connection_request',
                       params={'me_host': me_host})
        dump = db_req.request(path='/dump_database')
    return dump
