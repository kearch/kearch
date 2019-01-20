# Example for api is
# http://localhost:10080/crawl_a_page?url=https%3A//shedopen.deviantart.com/
# http://localhost:10080/crawl_a_page?url=https%3A//en.wikipedia.org/wiki/Haskell_%28programming_language%29

import os
import random
import signal
import sys
import flask
from flask import jsonify
import sp_crawler_child

app = flask.Flask(__name__)


@app.route('/sp/crawler-child/crawl_a_page', methods=['GET'])
def crawl_a_page():
    url = flask.request.args.get('url')
    print(url, file=sys.stderr)
    result = sp_crawler_child.url_to_json(url)
    return jsonify(result)

def shutdown(signum, frame):
    print('Performing periodic shutdown ...', file=sys.stderr)
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == '__main__':
    restart_sec = int(os.getenv('KEARCH_SP_CRAWLER_CHILD_RESTART_SEC', '0'))
    restart_sec += random.randint(0, restart_sec)
    if restart_sec > 0:
        signal.signal(signal.SIGALRM, shutdown)
        signal.alarm(restart_sec)
        print('Server will shutdown after {} seconds.'.format(restart_sec),
              file=sys.stderr)

    app.debug = True
    app.run(host='0.0.0.0', port=10080)  # どこからでもアクセス可能に
