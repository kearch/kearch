# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse
import langdetect
import nltk
from nltk.corpus import stopwords
import hashlib
import os
import pickle
import nb_topic_detect


class WebpageError(Exception):
    def __init__(self, message='This is default messege'):
        self.message = message


def create_webpage_with_cache(url):
    cachefile = './webcache/' + \
        hashlib.sha256(url.encode('utf-8')).hexdigest() + '.pickle'
    if os.path.exists(cachefile):
        with open(cachefile, 'rb') as f:
            w = pickle.load(f)
            return w
    else:
        w = Webpage(url)
        # if webpage parsing was failed w.tiel == url
        if w.title != url:
            with open(cachefile, 'wb') as f:
                pickle.dump(w, f)
        return w


class Webpage(object):
    def remove_non_ascii_character(self, text):
        ret = ""
        for c in list(text):
            if ord(c) < 128:
                ret += c
            else:
                ret += " "
        return ret

    def set_links(self, soup):
        row_links = list(soup.findAll("a"))
        ban_domain = list(["twitter.com", "2ch.sc", "tumblr.com"])
        ban_extension = list(
            ["pdf", "PDF", "jpg", "JPG", "png", "PNG", "gif", "GIF"])

        def check_domain(link):
            for b in ban_domain:
                if b in link:
                    return False
            return True

        res = list()
        for rl in row_links:
            link = rl.get("href")
            # last condition is excluding web archives
            if link is not None and link[:4] == 'http' and ":" in link and \
                    check_domain(link) and link[-3:] not in ban_extension and \
                    '://' not in link[7:]:
                res.append(link)
        self.links = res

        inner_links = list()
        outer_links = list()
        self_loc = urlparse(self.url).netloc
        for link in self.links:
            link = urlparse(link)
            if link.netloc == self_loc:
                inner_links.append(link.scheme + '://' +
                                   link.netloc + link.path)
            else:
                outer_links.append(link.scheme + '://' +
                                   link.netloc + link.path)
        self.inner_links = inner_links
        self.outer_links = outer_links

    def text_to_words(self, text):
        words = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '"', "'", '?', '!', ':',
                           ';', '(', ')', '[', ']', '{', '}'])
        words = list(map(lambda x: x.lower(), words))
        words = list(filter(lambda x: x not in stop_words, words))
        pat = r"[a-z]+"
        repat = re.compile(pat)
        words = list(filter(lambda x: re.match(repat, x), words))
        return words

    def __init__(self, url):
        self.url = url
        try:
            content = requests.get(self.url).content
        except requests.exceptions.RequestException:
            raise WebpageError('Cannot get content.')

        soup = BeautifulSoup(content, "lxml")
        for script in soup(["script", "style"]):
            script.extract()    # rip javascript out

        try:
            self.set_links(soup)
        except ValueError:
            raise WebpageError('Cannot set links')

        try:
            self.title = str(soup.title.string)
            self.text = str(soup.body.text)
        except AttributeError:
            raise WebpageError('Cannot get title or text')

        try:
            self.language = langdetect.detect(self.text)
        except langdetect.lang_detect_exception.LangDetectException:
            raise WebpageError('Cannot detect language.')

        self.title_words = self.text_to_words(self.title)
        # convert all white space to sigle space
        self.text = ' '.join(
            filter(lambda x: not x == '', re.split('\s', self.text)))

        # This version do not respond to mutibyte characters
        self.text = self.remove_non_ascii_character(self.text)
        self.summary = self.text[:500]
        self.words = self.text_to_words(self.text)


if __name__ == '__main__':
    t = "Hé ! bonjour, Monsieur du Corbeau.Que vous êtes joli ! \
        Que vous me semblez beau !"
    detector = langdetect.detect(t)
    print(detector)

    # w = Webpage('https://en.wikipedia.org/wiki/X-Cops_(The_X-Files)')
    # w = create_webpage_with_cache(
    # 'https://en.wikipedia.org/wiki/X-Cops_(The_X-Files)')
    # print(w.words)
    url = 'https://shedopen.deviantart.com/'
    w = create_webpage_with_cache(url)
    print(w.title)
    c = nb_topic_detect.TopicClassifier()
    print(w.title_words)
    print(c.classfy(w.title_words))
