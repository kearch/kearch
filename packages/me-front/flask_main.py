import flask
import sys

from kearch_common.requester import KearchRequester

QUERY_PROCESSOR_HOST = 'me-query-processor.kearch.svc.cluster.local'
QUERY_PROCESSOR_PORT = 10080

DATABASE_HOST = 'me-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306

REQUESTER_NAME = 'meta_front'
MAX_URLS = 100


app = flask.Flask(__name__)


@app.route('/me/front/search', methods=['GET'])
def search():
    if flask.request.method == 'GET':
        query = flask.request.args['query']
        sp = flask.request.args['sp']

        query_processor_requester = KearchRequester(
            QUERY_PROCESSOR_HOST, QUERY_PROCESSOR_PORT, REQUESTER_NAME)
        database_requester = KearchRequester(
            DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type="sql")

        params = {'query': query, 'max_urls': MAX_URLS}
        if sp != "":
            params['sp'] = sp

        results = query_processor_requester.request(
            path='/retrieve', method='GET', params=params)
        sp_servers = database_requester.request(
            path='/me/db/list_up_sp_servers', method='GET')

        print('results = ', results, file=sys.stderr)

        return flask.render_template(
            'result.html', results=results['data'], selected_sp=sp,
            sp_servers=sp_servers, query=query)
    else:
        return flask.redirect(flask.url_for('index.html'))


@app.route("/")
def index():
    database_requester = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type="sql")
    sp_servers = database_requester.request(
        path='/me/db/list_up_sp_servers', method='GET')

    return flask.render_template('index.html', sp_servers=sp_servers)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
