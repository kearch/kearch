import flask
import specialist_gateway


app = flask.Flask(__name__)


@app.route('/send_DB_summary', methods=['POST'])
def send_DB_summary():
    data = flask.request.args.get('payload')
    ip_sp = data['ip_sp']
    ip_me = data['ip_me']
    summary = data['summary']
    specialist_gateway.send_DB_summary(ip_sp, ip_me, summary)


@app.route('/retrieve', methods=['GET'])
def retrieve():
    queries = flask.request.args.get('queries')
    queries = queries.split(' ')
    max_urls = flask.request.args.get('max_urls', int)
    result = specialist_gateway.retrieve(queries, max_urls)
    return flask.render_template('result.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
