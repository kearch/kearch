import flask

from kearch_common.data_format import get_payload
from kearch_common.requester import KearchRequester

QUERY_PROCESSOR_HOST = 'me-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080
REQUESTER_NAME = 'meta_front'
MAX_URLS = 100


app = flask.Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if flask.request.method == 'GET':
        query = flask.request.args['query']
        queries = query.split()
        query_processor_requester = KearchRequester(
            QUERY_PROCESSOR_HOST, QUERY_PROCESSOR_PORT, REQUESTER_NAME)
        results = query_processor_requester.request(
            path='/retrieve', method='GET',
            params={'queries': ' '.join(queries), 'max_urls': MAX_URLS})

        print('results', results)

        return flask.render_template(
            'result.html', results=results['data'], query=query)
    else:
        return flask.redirect(flask.url_for('index.html'))


@app.route("/")
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
