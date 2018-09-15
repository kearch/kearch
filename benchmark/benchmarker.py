# -*- coding: utf-8 -*-

import random
import re
import urllib.request
import os
from bs4 import BeautifulSoup

URLS_FOR_EXTRACT = ["https://en.wikipedia.org/wiki/Programming_language",
                    "https://en.wikipedia.org/wiki/History",
                    "https://en.wikipedia.org/wiki/Kyoto"]

URL_FOR_SEARCH = "http://163.43.108.218:2222/search?query="
MAX_SIZE_OF_QUERY = 3
MAX_CONCURRENT_USER = 1000
SIZE_OF_TEST = 100

if __name__ == '__main__':
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

    for s in range(1, MAX_SIZE_OF_QUERY+1):
        for u in list(range(20, 100, 20)) + list(range(200, MAX_CONCURRENT_USER, 200)):
            with open('tmp_file_for_benchmark', 'w') as f:
                for t in range(0, SIZE_OF_TEST):
                    ws = random.sample(words, s)
                    f.write(URL_FOR_SEARCH + '+'.join(ws) + '\n')

            print('======================================================')
            print('Size of query = ' + str(s) + ',Connections = ' + str(u))
            os.system('siege --concurrent=' + str(u) + ' --time=10S --file=tmp_file_for_benchmark')
