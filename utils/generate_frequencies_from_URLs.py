from bs4 import BeautifulSoup
import requests
import nltk
import re
import sys
from nltk.corpus import stopwords


if __name__ == '__main__':
    infile = sys.argv[1]
    with open(infile) as f:
        urls = f.read().split('\n')
        urls = filter(lambda x: not x.isspace() and not x == '', urls)

    res = dict()
    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "lxml")
        text = soup.body.text

        words = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '"', "'", '?', '!', ':',
                           ';', '(', ')', '[', ']', '{', '}'])
        words = list(map(lambda x: x.lower(), words))
        words = list(filter(lambda x: x not in stop_words, words))
        pat = r"[a-z]+"
        repat = re.compile(pat)
        words = list(filter(lambda x: re.match(repat, x), words))
        for w in words:
            if w in res:
                res[w] += 1
            else:
                res[w] = 1
    aslist = list(res.items())
    aslist.sort(key=lambda x: x[1], reverse=True)
    for k, v in aslist:
        if 1 < v:
            print(k, v)
