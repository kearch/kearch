import flask
from flask import jsonify

import specialist_gateway

SPECIALIST_GATE_PORT = 10080
app = flask.Flask(__name__)


@app.route('/send_DB_summary', methods=['POST'])
def send_DB_summary():
    data = flask.request.get_json()
    sp_host = data['sp_host']
    me_host = data['me_host']
    summary = data['summary']
    result = specialist_gateway.send_DB_summary(sp_host, me_host, summary)
    return jsonify(result)


@app.route('/retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    queries = queries.split(' ')
    max_urls = flask.request.args.get('max_urls', int)
    result = specialist_gateway.retrieve(queries, max_urls)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SPECIALIST_GATE_PORT)  # どこからでもアクセス可能に
