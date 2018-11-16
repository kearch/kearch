from kearch_common.requester import KearchRequester

SPECIALIST_GATEWAY_PORT = 32500

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 10080
REQUESTER_NAME = 'meta_gateway'

CONFIG_HOST_NAME = 'host_name'


def update_sp_servers():
    db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    config = db.request(path='/me/db/get_config_variables')
    me_host = config[CONFIG_HOST_NAME]

    sp_servers = db.request(path='/list_up_sp_servers')

    res = {}
    for sp_host in sp_servers.keys():
        kr = KearchRequester(sp_host, SPECIALIST_GATEWAY_PORT, REQUESTER_NAME)
        dump = kr.request(path='/sp/gateway/get_a_dump',
                          params={'me_host': me_host})
        db.request(path='/add_new_sp_server',
                   payload={'host': sp_host, 'summary': dump})
    return res


def main():
    result = update_sp_servers()
    print(result)


if __name__ == '__main__':
    main()
