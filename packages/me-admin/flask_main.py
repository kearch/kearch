import flask
from flask import Response, jsonify, request, redirect, abort
from flask_login import LoginManager, logout_user, UserMixin, login_required, \
    login_user, current_user
import os
import sys
import base64
import hashlib
import kearch_evaluater.evaluater
from kearch_common.requester import KearchRequester

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'me-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

SP_GATEWAY_PORT = 32500
SP_GATEWAY_BASEURL = '/v0/sp/gateway/'

ME_ADMIN_PORT = 10080

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/me/admin/login"


class User(UserMixin):
    def __init__(self, id):
        self.id = 0
        self.name = 'root'


@app.route("/me/admin/login", methods=["GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_req = KearchRequester(
            DATABASE_HOST, DATABASE_PORT, conn_type='sql')
        auth_info = db_req.request(path='/me/db/get_authentication')
        is_valid = False
        for d in auth_info.values():
            u = d['username']
            h = d['password_hash']
            if u == username and \
               h == hashlib.sha512(password.encode('utf-8')).hexdigest():
                is_valid = True
        if is_valid:
            user = User(0)
            login_user(user)
            return redirect(flask.url_for("index"))
        else:
            return abort(401)
    else:
        return flask.render_template('login.html')


# somewhere to logout
@app.route("/me/admin/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/me/admin/update_password', methods=['POST'])
@login_required
def update_password():
    password = flask.request.form['password']
    password_again = flask.request.form['password_again']
    if password != password_again:
        r = {'message': 'Passwords do not match.'}
        abort(500, r)
    u = current_user.name
    h = hashlib.sha512(password.encode('utf-8')).hexdigest()
    print(u, h, file=sys.stderr)
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    ret = db_req.request(path='/me/db/update_password_hash',
                         payload={'username': u, 'password_hash': h},
                         method='POST')
    return flask.render_template('login.html')


@app.route('/me/admin/learn_params_for_evaluater', methods=['GET'])
@login_required
def learn_params_for_evaluater():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
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
@login_required
def index():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    requests = db_req.request(path='/me/db/get_connection_requests')
    sp_servers = db_req.request(path='/me/db/list_up_sp_servers')

    return flask.render_template('index.html', config=config,
                                 requests=requests, sp_servers=sp_servers)


@app.route("/me/admin/update_config", methods=['POST'])
@login_required
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    db_req.request(path='/me/db/set_config_variables',
                   payload=update, method='POST')
    return flask.redirect(flask.url_for("index"))


@app.route('/me/admin/approve_a_connection_request', methods=['POST'])
@login_required
def approve_a_connection_request():
    sp_host = flask.request.form['sp_host']

    gw_req = KearchRequester(sp_host, SP_GATEWAY_PORT)
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    config = db_req.request(path='/me/db/get_config_variables')
    me_host = config['host_name']

    summary = gw_req.request(path=SP_GATEWAY_BASEURL + 'get_a_summary',
                             params={'me_host': me_host})
    db_req.request(path='/me/db/add_new_sp_server',
                   payload=summary, method='POST')
    db_req.request(path='/me/db/approve_a_connection_request',
                   payload={'in_or_out': 'in', 'sp_host': sp_host},
                   method='POST')
    return jsonify(summary)


@app.route('/me/admin/delete_a_connection_request', methods=['DELETE'])
@login_required
def delete_a_connection_request():
    sp_host = flask.request.form['sp_host']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')

    db_req.request('/me/db/delete_a_connection_request',
                   payload={'sp_host': sp_host})

    config = db_req.request(path='/me/db/get_config_variables')
    me_host = config['host_name']
    gw_req = KearchRequester(sp_host, SP_GATEWAY_PORT)
    gw_req.request(path=SP_GATEWAY_BASEURL + 'delete_a_connection_request',
                   payload={'me_host': me_host}, method='DELETE')

    return flask.redirect(flask.url_for("index"))


@app.route('/me/admin/send_a_connection_request', methods=['POST'])
@login_required
def send_a_connection_request():
    sp_host = flask.request.form['sp_host']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')

    config = db_req.request(path='/me/db/get_config_variables')
    me_host = config['host_name']

    gw_req = KearchRequester(sp_host, SP_GATEWAY_PORT)

    db_req.request(path='/me/db/add_a_connection_request',
                   payload={'in_or_out': 'out', 'sp_host': sp_host})
    gw_req.request(path=SP_GATEWAY_BASEURL + 'send_a_connection_request',
                   payload={'me_host': me_host, 'scheme': 'http'},
                   method='POST')
    return flask.redirect(flask.url_for("index"))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=ME_ADMIN_PORT)  # どこからでもアクセス可能に
