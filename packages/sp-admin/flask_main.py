import flask
import base64
from flask import jsonify
from kearch_common.requester import KearchRequester
import kearch_classifier.classifier
import kearch_classifier.average_document as ave

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'sp-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'specialist_admin'
SP_ADMIN_PORT = 10080


app = flask.Flask(__name__)


@app.route('/approve_a_connection_request', methods=['POST'])
def approve_a_connection_request():
    me_host = flask.request.form['me_host']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')

    summary = db_req.request(path='/dump_database')
    config = db_req.request(path='/sp/db/get_config_variables')
    pld = {'sp_host': config['host_name'],
           'me_host': me_host, 'summary': summary}

    gw_req = KearchRequester(
        GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    gw_req.request(path='/send_DB_summary', payload=pld, method='POST')

    db_req.request('/sp/db/approve_a_connection_request',
                   payload={'in_or_out': 'in', 'me_host': me_host})
    return flask.redirect(flask.url_for("index"))


@app.route('/sp/admin/send_a_connection_request', methods=['POST'])
def send_a_connection_request():
    me_host = flask.request.form['me_host']

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/sp/db/add_a_connection_request',
                   payload={'me_host': me_host, 'in_or_out': 'out'},
                   method='POST')

    gw_req = KearchRequester(
        GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    gw_req.request(path='/sp/gateway/send_a_connection_request',
                   payload={'me_host': me_host}, method='POST')
    return flask.redirect(flask.url_for("index"))


@app.route('/send_db_summary', methods=['POST'])
def send_db_summary():
    me_host = flask.request.form['me_host']
    sp_host = flask.request.form['sp_host']

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    summary = db_req.request(path='/dump_database')
    pld = {'sp_host': sp_host, 'me_host': me_host, 'summary': summary}

    gw_req = KearchRequester(
        GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    ret = gw_req.request(path='/send_DB_summary', payload=pld, method='POST')
    return jsonify(ret)


@app.route('/init_crawl_urls', methods=['POST'])
def init_crawl_urls():
    form_input = flask.request.form['urls']
    urls = form_input.split('\n')
    urls = map(lambda x: x.rstrip(), urls)
    payload = dict()
    payload['urls'] = urls

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    ret = db_req.request(path='/push_urls_to_queue',
                         payload=payload, method='POST')
    return jsonify(ret)


@app.route('/learn_params', methods=['POST'])
def learn_params():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')

    form_input_topic = flask.request.form['topic_urls']
    form_input_random = flask.request.form['random_urls']
    language = flask.request.form['language']
    topic_urls = form_input_topic.split('\n')
    topic_urls = list(map(lambda x: x.rstrip(), topic_urls))
    random_urls = form_input_random.split('\n')
    random_urls = list(map(lambda x: x.rstrip(), random_urls))

    cls = kearch_classifier.classifier.Classifier()
    cls.learn_params(topic_urls, random_urls, language)
    cls.dump_params(kearch_classifier.classifier.PARAMS_FILE)

    bparam = open(kearch_classifier.classifier.PARAMS_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': kearch_classifier.classifier.PARAMS_FILE,
              'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    ave.make_average_document_cache(ave.CACHE_FILE, language)
    bparam = open(ave.CACHE_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': ave.CACHE_FILE, 'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    return flask.redirect(flask.url_for("index"))


@app.route("/update_config", methods=['POST'])
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/sp/db/set_config_variables',
                   payload=update, method='POST')
    return flask.redirect(flask.url_for("index"))


@app.route("/")
def index():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    config = db_req.request(path='/sp/db/get_config_variables')
    requests = db_req.request(path='/sp/db/get_connection_requests')
    return flask.render_template('index.html', config=config,
                                 requests=requests)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
