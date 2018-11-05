from kearch_common.requester import KearchRequester
import kearch_classifier.classifier

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'sp-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'specialist_admin'


def get_requests():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    requests = db_req.request(path='/sp/db/get_connection_requests')
    return requests


def get_config():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    config = db_req.request(path='/sp/db/get_config_variables')
    return config


def update_config(update):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/sp/db/set_config_variables',
                   payload=update, method='POST')
    config = get_config()
    return config


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
    urls = map(lambda x: x.rstrip(), urls)
    payload = dict()
    payload['urls'] = urls

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    ret = db_req.request(path='/push_urls_to_queue',
                         payload=payload, method='POST')
    return ret


def learn_params(form_input_topic, form_input_random, language):
    topic_urls = form_input_topic.split('\n')
    topic_urls = list(map(lambda x: x.rstrip(), topic_urls))
    random_urls = form_input_random.split('\n')
    random_urls = list(map(lambda x: x.rstrip(), random_urls))

    cls = kearch_classifier.classifier.Classifier()
    cls.learn_params(topic_urls, random_urls, language)

    return "OK"
