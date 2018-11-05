from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'me_admin'


def get_requests():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    requests = db_req.request(path='/me/db/get_connection_requests')
    return requests


def get_config():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    return config


def update_config(update):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/me/db/set_config_variables',
                   payload=update, method='POST')
    config = get_config()
    return config
