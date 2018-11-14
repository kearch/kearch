from kearch_common.requester import KearchRequester

SPECIALIST_GATEWAY_PORT = 32500

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 10080
REQUESTER_NAME = 'meta_gateway'

CONFIG_CONNECTION_POLICY = 'connection_policy'
CONFIG_HOST_NAME = 'host_name'


def get_me_host():
    db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    config = db.request(path='/me/db/get_config_variables')
    me_host = config[CONFIG_HOST_NAME]
    return me_host


def retrieve(sp_host, queries, max_urls):
    kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    results = kr.request(path='/retrieve', method='GET',
                         params={'queries': queries, 'max_urls': max_urls})
    return results


def add_new_sp_server(sp_host, summary):
    kr = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    result = kr.request(path='/add_new_sp_server',
                        payload={'host': sp_host, 'summary': summary})
    kr.request('/me/db/approve_a_connection_request',
               payload={'in_or_out': 'out', 'sp_host': sp_host})
    return result


def fetch_a_dump(sp_host):
    me_host = get_me_host()

    gt_req = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    results = gt_req.request(path='/sp/gateway/get_a_dump',
                             params={'me_host': me_host}, method='GET')
    return results


def add_a_connection_request(sp_host):
    db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    config = db.request(path='/me/db/get_config_variables', method='GET')
    if config[CONFIG_CONNECTION_POLICY] == 'public':
        sp = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
        dump = sp.request(path='/sp/gateway/get_a_dump',
                          params={'me_host': config[CONFIG_HOST_NAME]})
        db.request(path='/me/db/add_a_connection_request',
                   payload={'in_or_out': 'in', 'sp_host': sp_host})
        db.request(path='/add_new_sp_server',
                   payload={'host': sp_host, 'summary': dump})
        db.request(path='/me/db/approve_a_connection_request',
                   payload={'in_or_out': 'in', 'sp_host': sp_host},
                   method='POST')

        return {'sp_host': sp_host}
    else:
        db.request(path='/me/db/add_a_connection_request',
                   payload={'in_or_out': 'in', 'sp_host': sp_host})
        return {'sp_host': sp_host}


def send_a_connection_request(sp_host):
    me_host = get_me_host()

    kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
    res = kr.request(path='/sp/gateway/add_a_connection_request',
                     method='POST', payload={'me_host': me_host})
    return res
