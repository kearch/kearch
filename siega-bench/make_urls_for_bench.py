# -*- coding: utf-8 -*-

import random
import re
import urllib.request
from bs4 import BeautifulSoup

URL_FOR_EXTRACT = "https://en.wikipedia.org/wiki/Programming_language"
URL_FOR_EXTRACT = "https://en.wikipedia.org/wiki/History"

URL_FOR_SEARCH = "http://192.168.11.10/search?query="
SIZE_OF_QUERY = 2
SIZE_OF_TEST = 100

f = urllib.request.urlopen(URL_FOR_EXTRACT)
html = f.read().decode('utf-8')

soup = BeautifulSoup(html, "html.parser")
a_list = soup.find_all("a")

words = []
for link in a_list:
    s = link.get("href")
    r = re.compile(r'^/wiki/([a-zA-Z]*)$')
    if r.match(str(s)) is not None:
        words.append(r.match(str(s)).groups()[0])
for t in range(0, SIZE_OF_TEST):
    ws = random.sample(words, SIZE_OF_QUERY)
    print(URL_FOR_SEARCH + '+'.join(ws))
