# Example for api is
# http://localhost:10080/crawl_a_page?url=https%3A//shedopen.deviantart.com/
# http://localhost:10080/crawl_a_page?url=https%3A//en.wikipedia.org/wiki/Haskell_%28programming_language%29

import flask
import sys
import crawler_child

app = flask.Flask(__name__)


@app.route('/crawl_a_page', methods=['GET'])
def post():
    url = flask.request.args.get('url')
    print(url)
    sys.stderr.write(url + '\n')
    result = crawler_child.url_to_json_string(url)
    return flask.render_template('result.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
