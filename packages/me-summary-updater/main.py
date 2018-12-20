from kearch_common.requester import KearchRequester

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080
DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
REQUESTER_NAME = 'meta_gateway'


def update_sp_servers():
    db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                         conn_type='sql')
    sp_servers = db.request(path='/me/db/list_up_sp_servers')
    print(sp_servers.keys())

    for sp_host in sp_servers.keys():
        print('fetching summary from {} ...'.format(sp_host))
        kr = KearchRequester(GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
        dump = kr.request(path='/me/gateway/fetch_a_dump',
                          params={'sp_host': sp_host})

        print('saving summary from {} ...'.format(sp_host))
        me_db = KearchRequester(DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME,
                                conn_type='sql')
        me_db.request(path='/me/db/add_new_sp_server',
                      payload={'host': sp_host, 'summary': dump})


def main():
    update_sp_servers()


if __name__ == '__main__':
    main()
