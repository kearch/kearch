import flask
from flask import jsonify

import meta_gateway

META_GATE_PORT = 10080
BASEURL = '/v0/me/gateway/'
app = flask.Flask(__name__)


@app.route(BASEURL + 'add_a_summary', methods=['POST'])
def add_a_summary():
    summary = flask.request.get_json()
    result = meta_gateway.add_new_sp_server(summary)
    return jsonify(result)


@app.route(BASEURL + 'add_a_connection_request', methods=['POST'])
def add_a_connection_request():
    data = flask.request.get_json()
    sp_host = data['sp_host']
    engine_name = data['engine_name']
    scheme = data['scheme']
    result = meta_gateway.add_a_connection_request(sp_host, engine_name,
                                                   scheme)
    return jsonify(result)


@app.route(BASEURL + 'delete_a_connection_request', methods=['POST'])
def send_a_connection_request():
    data = flask.request.get_json()
    sp_host = data['sp_host']
    res = meta_gateway.delete_a_connection_request(sp_host)
    return jsonify(res)


@app.route(BASEURL + 'retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    max_urls = flask.request.args.get('max_urls', int)
    sp_host = flask.request.args.get('sp_host')
    results = meta_gateway.retrieve(sp_host, queries, max_urls)
    return jsonify(results)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=META_GATE_PORT)  # どこからでもアクセス可能に
