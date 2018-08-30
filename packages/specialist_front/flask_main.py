import flask
from kearch_common.requester import KearchRequester
from kearch_common.data_format import get_payload

QUERY_PROCESSOR_IP = '192.168.11.05'
QUERY_PROCESSOR_PORT = 10080
REQUESTER_NAME = 'specialist_front'
MAX_URLS = 100


app = flask.Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if flask.request.method == 'GET':
        query = flask.request.args['query']
        queries = query.split()
        query_processor_requester = KearchRequester(
            QUERY_PROCESSOR_IP, QUERY_PROCESSOR_PORT, REQUESTER_NAME)
        response = query_processor_requester.request(
            path='/retrieve', method='GET', payload={'queries': queries, 'max_urls': MAX_URLS})
        results = get_payload(response)
        return flask.render_template('result.html', results=results['data'], query=query)
    else:
        return flask.redirect(flask.url_for('index.html'))


@app.route("/")
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=2222)  # どこからでもアクセス可能に
