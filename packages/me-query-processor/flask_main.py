# Example for api is
# http://localhost:10080/retrieve?queries=facebook+google&max_urls=100

import flask
from flask import jsonify

import meta_query_processor

app = flask.Flask(__name__)


@app.route('/retrieve', methods=['GET'])
def post():
    queries = flask.request.args.get('queries')
    queries = queries.split(' ')
    max_urls = flask.request.args.get('max_urls')
    if 'sp' in flask.request.args:
        sp = flask.request.args.get('sp')
        result = meta_query_processor.retrieve(queries, max_urls, sp=sp)
    else:
        result = meta_query_processor.retrieve(queries, max_urls)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
