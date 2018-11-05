import flask
import me_admin

SP_ADMIN_PORT = 10080
app = flask.Flask(__name__)


@app.route("/")
def index():
    config = me_admin.get_config()
    return flask.render_template('index.html', config=config)


@app.route("/update_config", methods=['POST'])
def update_config():
    update = dict()
    if 'connection_policy' in flask.request.form:
        update['connection_policy'] = flask.request.form['connection_policy']
    if 'host_name' in flask.request.form:
        update['host_name'] = flask.request.form['host_name']
    config = me_admin.update_config(update)
    return flask.render_template('index.html', config=config)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=SP_ADMIN_PORT)  # どこからでもアクセス可能に