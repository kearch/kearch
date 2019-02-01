import flask
import sys
import hashlib
from flask_login import LoginManager, logout_user, UserMixin, login_required, \
    login_user, current_user
import base64
import os
from flask import Response, jsonify, request, redirect, abort
from kearch_common.requester import KearchRequester
import kearch_classifier.classifier
import kearch_classifier.average_document as ave

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

GATEWAY_HOST = 'sp-gateway.kearch.svc.cluster.local'
GATEWAY_PORT = 10080

SP_ADMIN_PORT = 10080

DEFAULT_DICT_EN_FILE = 'en_default_dict.txt'

ME_GATEWAY_PORT = 32400
ME_GATEWAY_BASEURL = '/v0/me/gateway/'

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/sp/admin/login"


class User(UserMixin):
    def __init__(self, id):
        self.id = 0
        self.name = 'root'


@app.route("/sp/admin/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_req = KearchRequester(
            DATABASE_HOST, DATABASE_PORT, conn_type='sql')
        auth_info = db_req.request(path='/sp/db/get_authentication')
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
@app.route("/sp/admin/logout")
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


def send_a_summary(me_host):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    summary = db_req.request(path='/sp/db/dump_database')
    gw_req = KearchRequester(me_host, ME_GATEWAY_PORT)
    res = gw_req.request(path=ME_GATEWAY_BASEURL + 'add_a_summary',
                         payload=summary, method='POST')
    return res


@app.route('/sp/admin/update_password', methods=['POST'])
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
    ret = db_req.request(path='/sp/db/update_password_hash',
                         payload={'username': u, 'password_hash': h},
                         method='POST')
    return jsonify(ret)


@app.route('/sp/admin/approve_a_connection_request', methods=['POST'])
@login_required
def approve_a_connection_request():
    me_host = flask.request.form['me_host']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')

    send_a_summary(me_host)

    db_req.request('/sp/db/approve_a_connection_request',
                   payload={'in_or_out': 'in', 'me_host': me_host})

    return flask.redirect(flask.url_for("index"))


@app.route('/sp/admin/delete_a_connection_request', methods=['POST'])
@login_required
def delete_a_connection_request():
    me_host = flask.request.form['me_host']
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')

    db_req.request('/sp/db/delete_a_connection_request',
                   payload={'me_host': me_host})

    config = db_req.request(path='/sp/db/get_config_variables')
    sp_host = config['host_name']
    gw_req = KearchRequester(me_host, ME_GATEWAY_PORT)
    gw_req.request(path=ME_GATEWAY_BASEURL + 'delete_a_connection_request',
                   payload={'sp_host': sp_host}, method='DELETE')

    return flask.redirect(flask.url_for("index"))


@app.route('/sp/admin/send_a_connection_request', methods=['POST'])
@login_required
def send_a_connection_request():
    me_host = flask.request.form['me_host']

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    payload = {'me_host': me_host, 'in_or_out': 'out', 'scheme': 'http'}

    db_req.request(path='/sp/db/add_a_connection_request',
                   payload=payload, method='POST')

    config = db_req.request(path='/sp/db/get_config_variables')
    sp_host = config['host_name']
    engine_name = config['engine_name']
    payload = {'sp_host': sp_host,
               'engine_name': engine_name, 'scheme': 'http'}

    gw_req = KearchRequester(me_host, ME_GATEWAY_PORT)
    gw_req.request(path=ME_GATEWAY_BASEURL + 'add_a_connection_request',
                   payload=payload, method='POST')

    return flask.redirect(flask.url_for("index"))


@app.route('/sp/admin/init_crawl_urls', methods=['POST'])
@login_required
def init_crawl_urls():
    form_input = flask.request.form['urls']
    urls = form_input.split('\n')
    urls = map(lambda x: x.rstrip(), urls)
    payload = dict()
    payload['urls'] = urls

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    ret = db_req.request(path='/sp/db/push_urls_to_queue',
                         payload=payload, method='POST')
    return jsonify(ret)


@app.route('/sp/admin/learn_params_from_url', methods=['POST'])
@login_required
def learn_params_from_url():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')

    form_input_topic = flask.request.form['topic_urls']
    form_input_random = flask.request.form['random_urls']
    language = flask.request.form['language']
    topic_urls = form_input_topic.split('\n')
    topic_urls = list(map(lambda x: x.rstrip(), topic_urls))
    random_urls = form_input_random.split('\n')
    random_urls = list(map(lambda x: x.rstrip(), random_urls))

    cls = kearch_classifier.classifier.Classifier()
    cls.learn_params_from_url(topic_urls, random_urls, language)
    cls.dump_params(kearch_classifier.classifier.PARAMS_FILE)

    bparam = open(kearch_classifier.classifier.PARAMS_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': kearch_classifier.classifier.PARAMS_FILE,
              'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    ave.make_average_document_from_urls(random_urls, language)
    bparam = open(ave.CACHE_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': ave.CACHE_FILE, 'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    return flask.redirect(flask.url_for("index"))


@app.route('/sp/admin/learn_params_from_dict', methods=['POST'])
@login_required
def learn_params_from_dict():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    form_input_topic = flask.request.form['topic_dict']
    language = flask.request.form['language']

    if 'use_default_dict' in flask.request.form:
        if language == 'en':
            with open(DEFAULT_DICT_EN_FILE, 'r') as f:
                form_input_random = f.read()
        else:
            r = {'message': language + ' default dictionary is not available.'}
            flask.abort(500, r)
    else:
        form_input_random = flask.request.form['random_dict']

    topic_lines = form_input_topic.split('\n')
    random_lines = form_input_random.split('\n')

    topic_dict = dict()
    random_dict = dict()
    for l in topic_lines:
        ws = l.split(None)
        if ws[0] not in topic_dict:
            topic_dict[ws[0]] = int(ws[1])
        else:
            topic_dict[ws[0]] += int(ws[1])
    for l in random_lines:
        ws = l.split(None)
        if len(ws) < 2:
            continue
        elif ws[0] not in random_dict:
            random_dict[ws[0]] = int(ws[1])
        else:
            random_dict[ws[0]] += int(ws[1])

    cls = kearch_classifier.classifier.Classifier()
    cls.learn_params_from_dict(topic_dict, random_dict, language)
    cls.dump_params(kearch_classifier.classifier.PARAMS_FILE)

    bparam = open(kearch_classifier.classifier.PARAMS_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': kearch_classifier.classifier.PARAMS_FILE,
              'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    ave.make_average_document_from_dict(random_dict, language)
    bparam = open(ave.CACHE_FILE, 'rb').read()
    tparam = base64.b64encode(bparam).decode('utf-8')
    params = {'name': ave.CACHE_FILE, 'body': tparam}
    db_req.request(path='/sp/db/push_binary_file', params=params)

    return flask.redirect(flask.url_for("index"))


@app.route("/sp/admin/update_config", methods=['POST'])
@login_required
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    if 'engine_name' in flask.request.form:
        update['engine_name'] = flask.request.form['engine_name']

    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    db_req.request(path='/sp/db/set_config_variables',
                   payload=update, method='POST')
    return flask.redirect(flask.url_for("index"))


@app.route("/")
@login_required
def index():
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, conn_type='sql')
    config = db_req.request(path='/sp/db/get_config_variables')
    requests = db_req.request(path='/sp/db/get_connection_requests')
    return flask.render_template('index.html', config=config,
                                 requests=requests)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
