from kearch_common.requester import KearchRequester

META_GATEWAY_PORT = 32400

QUERY_PROCESSOR_HOST = 'sp-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'specialist_gateway'

CONFIG_CONNECTION_POLICY = 'connection_policy'
CONFIG_HOST_NAME = 'host_name'
CONFIG_ENGINE_NAME = 'engine_name'


def is_connected(me_host):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    reqs = db_req.request(path='/sp/db/get_connection_requests')
    if (me_host in reqs['out'] and reqs['out'][me_host]) or \
            (me_host in reqs['in'] and reqs['in'][me_host]):
        # already approved
        return True
    return False


def retrieve(queries, max_urls):
    kr = KearchRequester(QUERY_PROCESSOR_HOST,
                         QUERY_PROCESSOR_PORT, REQUESTER_NAME)
    results = kr.request(path='/sp/query-processor/retrieve', method='GET',
                         params={'queries': ' '.join(queries),
                                 'max_urls': max_urls})
    return results


def send_a_dump(sp_host, me_host, summary):
    d = dict()
    d['host'] = sp_host
    d['summary'] = summary

    kr = KearchRequester(me_host, META_GATEWAY_PORT, REQUESTER_NAME)
    result = kr.request(path='/me/gateway/add_new_sp_server', method='POST',
                        payload=d)
    return result


def add_a_connection_request(scheme, me_host):
    db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    config = db.request(path='/sp/db/get_config_variables', method='GET')
    if config[CONFIG_CONNECTION_POLICY] == 'public':
        sp_host = config[CONFIG_HOST_NAME]
        dump = db.request(path='/sp/db/dump_database', method='GET')
        res = send_a_dump(sp_host, me_host, dump)
        return res
    else:
        res = db.request(path='/sp/db/add_a_connection_request',
                         payload={'in_or_out': 'in', 'scheme': scheme,
                                  'me_host': me_host})
        return res


def get_a_dump(me_host):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    reqs = db_req.request(path='/sp/db/get_connection_requests')
    should_approve = me_host in reqs['out'] and not reqs['out'][me_host]

    dump = {}
    if should_approve or is_connected(me_host):
        dump = db_req.request(path='/sp/db/dump_database')
    if should_approve:
        db_req.request(path='/sp/db/approve_a_connection_request',
                       payload={'me_host': me_host, 'in_or_out': 'out'})
    return dump
