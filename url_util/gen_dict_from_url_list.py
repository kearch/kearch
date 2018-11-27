from bs4 import BeautifulSoup
import requests
import nltk
import re
from nltk.corpus import stopwords

urls_computer = [
        'https://en.wikipedia.org/wiki/Python_(programming_language)'
]

urls = urls_computer

if __name__ == '__main__':
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
    l = list(res.items())
    l.sort(key=lambda x:x[1], reverse=True)
    for k,v in l:
        if 1 < v:
            print(k, v)
