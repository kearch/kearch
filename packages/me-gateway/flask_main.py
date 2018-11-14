import flask
from flask import jsonify
from kearch_common.data_format import unwrap_json

import meta_gateway

META_GATE_PORT = 10080
app = flask.Flask(__name__)


@app.route('/add_new_sp_server', methods=['POST'])
def add_new_sp_server():
    data = unwrap_json(flask.request.get_json())
    sp_host = data['host']
    summary = data['summary']
    result = meta_gateway.add_new_sp_server(sp_host, summary)
    return jsonify(result)


@app.route('/me/gateway/add_a_dump', methods=['POST'])
def add_a_dump():
    data = unwrap_json(flask.request.get_json())
    sp_host = data['host']
    summary = data['summary']
    result = meta_gateway.add_new_sp_server(sp_host, summary)
    return jsonify(result)


@app.route('/me/gateway/fetch_a_dump', methods=['GET'])
def fetch_a_dump():
    sp_host = flask.request.args.get('sp_host')
    dump = meta_gateway.fetch_a_dump(sp_host)
    return jsonify(dump)


@app.route('/me/gateway/add_a_connection_request', methods=['POST'])
def add_a_connection_request():
    data = unwrap_json(flask.request.get_json())
    sp_host = data['sp_host']
    result = meta_gateway.add_a_connection_request(sp_host)
    return jsonify(result)


@app.route('/me/gateway/send_a_connection_request', methods=['POST'])
def send_a_connection_request():
    data = unwrap_json(flask.request.get_json())
    sp_host = data['sp_host']
    res = meta_gateway.send_a_connection_request(sp_host)
    return jsonify(res)


@app.route('/retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    queries = queries.split(' ')
    max_urls = flask.request.args.get('max_urls', int)
    sp_host = flask.request.args.get('sp_host')
    results = meta_gateway.retrieve(sp_host, queries, max_urls)
    return jsonify(results)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=META_GATE_PORT)  # どこからでもアクセス可能に
