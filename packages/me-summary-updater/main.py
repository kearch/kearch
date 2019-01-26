from kearch_common.requester import KearchRequester

SP_GATEWAY_PORT = 32500
DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
CONFIG_HOST_NAME = 'host_name'


def update_sp_servers():
    db_req = KearchRequester(DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    me_host = config[CONFIG_HOST_NAME]
    sp_servers = db_req.request(path='/me/db/list_up_sp_servers')
    print(sp_servers.keys())

    for sp_host in sp_servers.keys():
        print('fetching summary from {} ...'.format(sp_host))
        kr = KearchRequester(sp_host, SP_GATEWAY_PORT)
        dump = kr.request(path='/v0/sp/gateway/get_a_dump',
                          params={'me_host': me_host})

        print('saving summary from {} ...'.format(sp_host))
        me_db = KearchRequester(DATABASE_HOST, DATABASE_PORT,
                                conn_type='sql')
        me_db.request(path='/me/db/add_new_sp_server',
                      payload={'host': sp_host, 'summary': dump})


def test_update_sp_servers():
    update_sp_servers()


def main():
    update_sp_servers()


if __name__ == '__main__':
    main()
