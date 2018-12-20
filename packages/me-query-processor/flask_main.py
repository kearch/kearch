# Example for api is
# http://localhost:10080/retrieve?query=facebook+google&max_urls=100

import flask
from flask import jsonify

import meta_query_processor

app = flask.Flask(__name__)


@app.route('/me/query-processor/retrieve', methods=['GET'])
def post():
    query = flask.request.args.get('query')
    max_urls = int(flask.request.args.get('max_urls'))
    if 'sp' in flask.request.args:
        sp = flask.request.args.get('sp')
        result = meta_query_processor.retrieve(query, max_urls, sp=sp)
    else:
        result = meta_query_processor.retrieve(query, max_urls)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
