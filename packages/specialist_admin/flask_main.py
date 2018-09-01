import flask
import specialist_admin

SP_ADMIN_PORT = 10080
app = flask.Flask(__name__)


@app.route('/send_db_summary', methods=['GET'])
def send_db_summary():
    meta_ip = flask.request.args.get('meta_ip')
    specialist_admin.send_db_summary(meta_ip)


@app.route('/init_crawl_urls', methods=['POST'])
def init_crawl_urls():
    form_input = flask.request.form['urls']
    specialist_admin.init_crawl_urls(form_input)


@app.route("/")
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
