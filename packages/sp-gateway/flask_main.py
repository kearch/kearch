import flask
from flask import jsonify

import specialist_gateway

SPECIALIST_GATE_PORT = 10080
BASEURL = '/v0/sp/gateway/'
app = flask.Flask(__name__)


@app.route(BASEURL + 'get_a_summary', methods=['GET'])
def get_a_dump():
    me_host = flask.request.args.get('me_host')
    result = specialist_gateway.get_a_dump(me_host)
    return jsonify(result)


@app.route(BASEURL + 'add_a_connection_request', methods=['POST'])
def add_a_connection_request():
    data = flask.request.get_json()
    me_host = data['me_host']
    scheme = data['scheme']
    result = specialist_gateway.add_a_connection_request(me_host, scheme)
    return jsonify(result)


@app.route(BASEURL + 'retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    max_urls = flask.request.args.get('max_urls', int)
    result = specialist_gateway.retrieve(queries, max_urls)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SPECIALIST_GATE_PORT)  # どこからでもアクセス可能に
