# Example for api is
# http://localhost:10080/crawl_a_page?url=https%3A//shedopen.deviantart.com/
# http://localhost:10080/crawl_a_page?url=https%3A//en.wikipedia.org/wiki/Haskell_%28programming_language%29

import flask
import crawler_child
import urllib.parse

app = flask.Flask(__name__)


@app.route('/crawl_a_page', methods=['GET'])
def post():
    url_q = flask.request.args['url']
    url = urllib.parse.unquote(url_q)
    result = crawler_child.url_to_json_string(url)
    return flask.render_template('result.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
