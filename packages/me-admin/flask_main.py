import flask
from flask import jsonify
import base64
import kearch_evaluater.evaluater
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'me_admin'

SP_ADMIN_PORT = 10080

app = flask.Flask(__name__)


@app.route('/me/admin/learn_params_for_evaluater')
def learn_params_for_evaluater():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    summaries = db_req.request(path='/me/db/get_sp_summaries')
    e = kearch_evaluater.evaluater.Evaluater()
    e.learn_params(summaries)
    e.dump_params(kearch_evaluater.evaluater.PARAMS_FILE)

    bparam = open(kearch_evaluater.evaluater.PARAMS_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': kearch_evaluater.evaluater.PARAMS_FILE,
              'body': tparam}
    res = db_req.request(path='/me/db/push_binary_file', params=params)
    return jsonify(res)


@app.route("/")
def index():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    requests = db_req.request(path='/me/db/get_connection_requests')
    sp_servers = db_req.request(path='/me/db/list_up_sp_servers')

    return flask.render_template('index.html', config=config,
                                 requests=requests, sp_servers=sp_servers)


@app.route("/me/admin/update_config", methods=['POST'])
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    db_req.request(path='/me/db/set_config_variables',
                   payload=update, method='POST')
    return flask.redirect(flask.url_for("index"))


@app.route('/me/admin/approve_a_connection_request', methods=['POST'])
def approve_a_connection_request():
    gt_req = KearchRequester(GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')

    sp_host = flask.request.form['sp_host']
    dump = gt_req.request(path='/me/gateway/fetch_a_dump',
                          params={'sp_host': sp_host})
    db_req.request(path='/add_new_sp_server',
                   payload={'host': sp_host, 'summary': dump}, method='POST')
    db_req.request(path='/me/db/approve_a_connection_request',
                   payload={'in_or_out': 'in', 'sp_host': sp_host},
                   method='POST')
    return jsonify(dump)


@app.route('/me/admin/send_a_connection_request', methods=['POST'])
def send_a_connection_request():
    sp_host = flask.request.form['sp_host']
    gt_req = KearchRequester(GATEWAY_HOST, GATEWAY_PORT, REQUESTER_NAME)
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')

    db_req.request(path='/me/db/add_a_connection_request',
                   payload={'in_or_out': 'out', 'sp_host': sp_host})
    gt_req.request(path='/me/gateway/send_a_connection_request',
                   payload={'sp_host': sp_host}, method='POST')
    return flask.redirect(flask.url_for("index"))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
