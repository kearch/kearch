import flask
from kearch_common.data_format import unwrap_json
import specialist_admin

SP_ADMIN_PORT = 10080
app = flask.Flask(__name__)


@app.route('/send_db_summary', methods=['GET'])
def send_db_summary():
    meta_ip = flask.request.args.get('meta_ip')
    specialist_admin.send_db_summary(meta_ip)


@app.route('/init_crawl_urls', methods=['POST'])
def init_crawl_urls():
    inp = flask.request.form['urls']
    specialist_admin.init_crawl_urls(inp)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
