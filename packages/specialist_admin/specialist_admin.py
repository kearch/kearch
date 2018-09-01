from kearch_common.requester import KearchRequester

DATABASE_HOST = '192.168.11.10'
DATABASE_PORT = 10080

GATEWAY_HOST = '192.168.11.30'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'specialist_admin'


def send_db_summary(meta_ip):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    summary = db_req.request(path='/dump_database')

    gw_req = KearchRequester(
        GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    gw_req.request(path='/send_DB_summary', payload=summary, method='POST')


# inputs is just text contains URLs separated by newline.
def init_crawl_urls(form_input):
    urls = form_input.split('\n')
    json = dict()
    json['urls'] = urls

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/push_links_to_queue', payload=json, method='POST')
