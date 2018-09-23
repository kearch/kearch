# -*- coding: utf-8 -*-

import argparse
import random
import re
import urllib
import os
from bs4 import BeautifulSoup

URLS_FOR_EXTRACT = ["https://en.wikipedia.org/wiki/Programming_language",
                    "https://en.wikipedia.org/wiki/History",
                    "https://en.wikipedia.org/wiki/Kyoto"]

MAX_SIZE_OF_QUERY = 3
CONCURRENCY_LIST = [30, 100, 300, 1000]
SIZE_OF_TEST = 100

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scheme', '-s', default='http')
    parser.add_argument('--host', '-H', default='163.43.108.218')
    parser.add_argument('--port', '-p', default=2222, type=int)
    args = parser.parse_args()

    words = []
    for url in URLS_FOR_EXTRACT:
        f = urllib.request.urlopen(url)
        html = f.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find_all("a")
        for link in a_list:
            s = link.get("href")
            r = re.compile(r'^/wiki/([a-zA-Z]*)$')
            if r.match(str(s)) is not None:
                words.append(r.match(str(s)).groups()[0])

    for u in CONCURRENCY_LIST:
        for s in range(1, MAX_SIZE_OF_QUERY+1):
            with open('/tmp/tmp_file_for_benchmark', 'w') as f:
                for t in range(0, SIZE_OF_TEST):
                    ws = random.sample(words, s)
                    query_str = urllib.parse.urlencode({'query': ' '.join(ws)})
                    netloc = '{}:{}'.format(args.host, args.port)
                    url_str = urllib.parse.urlunparse(
                        (args.scheme, netloc, '/search', '', query_str, ''))
                    f.write(url_str + '\n')

            print('======================================================')
            print('Size of query = ' + str(s) + ',Connections = ' + str(u))
            os.system('siege --concurrent=' + str(u) +
                      ' --time=10S --file=/tmp/tmp_file_for_benchmark')
