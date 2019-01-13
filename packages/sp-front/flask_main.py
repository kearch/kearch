import flask
from kearch_common.requester import KearchRequester

QUERY_PROCESSOR_HOST = 'sp-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080
MAX_URLS = 100


app = flask.Flask(__name__)


@app.route('/sp/front/search', methods=['GET', 'POST'])
def search():
    if flask.request.method == 'GET':
        query = flask.request.args['query']
        queries = query.split()
        kr = KearchRequester(QUERY_PROCESSOR_HOST, QUERY_PROCESSOR_PORT)
        results = kr.request(path='/sp/query-processor/retrieve', method='GET',
                             params={'queries': ' '.join(queries),
                                     'max_urls': MAX_URLS})
        return flask.render_template('result.html', results=results['data'],
                                     query=query)
    else:
        return flask.redirect(flask.url_for('index.html'))


@app.route("/")
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
