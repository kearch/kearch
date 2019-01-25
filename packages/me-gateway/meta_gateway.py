from kearch_common.requester import KearchRequester
import pytest

SPECIALIST_GATEWAY_PORT = 32500
SP_GATEWAY_BASEURL = '/v0/sp/gateway/'

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 10080

CONFIG_CONNECTION_POLICY = 'connection_policy'
CONFIG_HOST_NAME = 'host_name'


def get_me_host():
    db_req = KearchRequester(DATABASE_HOST, DATABASE_PORT,
                             conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    me_host = config[CONFIG_HOST_NAME]
    return me_host


def retrieve(sp_host, queries, max_urls):
    gw_req = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT)
    results = gw_req.request(path=SP_GATEWAY_BASEURL + 'retrieve',
                             method='GET',
                             params={'queries': queries, 'max_urls': max_urls})
    return results


@pytest.mark.minikube
def test_retrieve():
    # This test is assumed to run on minikube.
    for q in ['google', 'linux', 'linux kernel']:
        results = retrieve('192.168.99.100', q, 100)
        for r in results:
            assert('url' in r)
            assert('title' in r)
            assert('description' in r)
            assert('score' in r)


def add_new_sp_server(summary):
    db_req = KearchRequester(DATABASE_HOST, DATABASE_PORT,
                             conn_type='sql')
    result = db_req.request(path='/me/db/add_new_sp_server',
                            payload=summary)
    sp_host = summary['sp_host']
    db_req.request('/me/db/approve_a_connection_request',
                   payload={'in_or_out': 'out', 'sp_host': sp_host})
    return result


def delete_a_connection_request(sp_host):
    db_req = KearchRequester(DATABASE_HOST, DATABASE_PORT,
                             conn_type='sql')
    res = db_req.request(path='/me/db/delete_a_connection_request',
                         payload={'sp_host': sp_host})
    return res


def add_a_connection_request(sp_host, engine_name, scheme):
    db_req = KearchRequester(DATABASE_HOST, DATABASE_PORT,
                             conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables', method='GET')
    if config[CONFIG_CONNECTION_POLICY] == 'public':
        sp = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT)
        dump = sp.request(path=SP_GATEWAY_BASEURL + 'get_a_dump',
                          params={'me_host': config[CONFIG_HOST_NAME]})
        db_req.request(path='/me/db/add_a_connection_request',
                       payload={'in_or_out': 'in', 'sp_host': sp_host,
                                'engine_name': engine_name, 'scheme': scheme})
        db_req.request(path='/me/db/add_new_sp_server',
                       payload={'host': sp_host, 'summary': dump})
        db_req.request(path='/me/db/approve_a_connection_request',
                       payload={'in_or_out': 'in', 'sp_host': sp_host},
                       method='POST')

        return {'sp_host': sp_host}
    else:
        db_req.request(path='/me/db/add_a_connection_request',
                       payload={'in_or_out': 'in', 'sp_host': sp_host,
                                'engine_name': engine_name, 'scheme': scheme})
        return {'sp_host': sp_host}


def send_a_connection_request(sp_host):
    me_host = get_me_host()

    gw_req = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT)
    res = gw_req.request(path=SP_GATEWAY_BASEURL + 'add_a_connection_request',
                         method='POST', payload={'me_host': me_host})
    return res
