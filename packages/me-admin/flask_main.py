import flask
from flask import jsonify
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

REQUESTER_NAME = 'me_admin'

SP_ADMIN_PORT = 10080

app = flask.Flask(__name__)


@app.route("/")
def index():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    requests = db_req.request(path='/me/db/get_connection_requests')
    return flask.render_template('index.html', config=config,
                                 requests=requests)


@app.route("/update_config", methods=['POST'])
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


@app.route('/approve_a_connection_request', methods=['POST'])
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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
