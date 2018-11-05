import flask
from flask import jsonify
import specialist_admin

SP_ADMIN_PORT = 10080
app = flask.Flask(__name__)


@app.route('/send_db_summary', methods=['POST'])
def send_db_summary():
    me_host = flask.request.form['me_host']
    sp_host = flask.request.form['sp_host']

    result = specialist_admin.send_db_summary(me_host, sp_host)
    return jsonify(result)


@app.route('/init_crawl_urls', methods=['POST'])
def init_crawl_urls():
    form_input = flask.request.form['urls']
    result = specialist_admin.init_crawl_urls(form_input)
    return jsonify(result)


@app.route('/learn_params', methods=['POST'])
def learn_params():
    form_input_topic = flask.request.form['topic_urls']
    form_input_random = flask.request.form['random_urls']
    language = flask.request.form['language']
    result = specialist_admin.learn_params(
        form_input_topic, form_input_random, language)
    return result


@app.route("/update_config", methods=['POST'])
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    return flask.redirect(flask.url_for("index"))


@app.route("/")
def index():
    config = specialist_admin.get_config()
    requests = specialist_admin.get_requests()
    return flask.render_template('index.html', config=config,
                                 requests=requests)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に
