import flask

from kearch_common.data_format import get_payload
from kearch_common.requester import KearchRequester

QUERY_PROCESSOR_HOST = 'me-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'meta_front'
MAX_URLS = 100


app = flask.Flask(__name__)


@app.route('/search', methods=['GET'])
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
    database_requester = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type="sql")
    sp_servers = database_requester.request(
        PATH='/list_up_sp_servers', method='GET')

    return flask.render_template('index.html', sp_servers=sp_servers)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
