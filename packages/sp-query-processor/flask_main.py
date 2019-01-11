import flask
from flask import jsonify

import specialist_query_processor

app = flask.Flask(__name__)


@app.route('/sp/query-processor/retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    queries = queries.split(' ')
    max_urls = flask.request.args.get('max_urls', int)
    result = specialist_query_processor.retrieve(queries, max_urls)
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
