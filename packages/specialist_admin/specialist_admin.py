from kearch_common.requester import KearchRequester

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'sp-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'specialist_admin'


def send_db_summary(me_host, sp_host):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    summary = db_req.request(path='/dump_database')
    pld = {'sp_host': sp_host, 'me_host': me_host, 'summary': summary}

    gw_req = KearchRequester(
        GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    ret = gw_req.request(path='/send_DB_summary', payload=pld, method='POST')
    return ret


# inputs is just text contains URLs separated by newline.
def init_crawl_urls(form_input):
    urls = form_input.split('\n')
    urls = map(lambda x:x.rstrip(), urls)
    payload = dict()
    payload['urls'] = urls

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    ret = db_req.request(path='/push_urls_to_queue',
                         payload=payload, method='POST')
    return ret
