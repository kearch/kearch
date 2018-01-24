# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import random
from urllib.parse import urlparse
from langdetect import detect
import nltk
import traceback
from nltk.corpus import stopwords


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
        ban_domain = list(["twitter.com", "2ch.sc"])
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
                outer_links.append(link.scheme + '://' + link.netloc + link.path)
        self.inner_linkss = inner_links
        self.outer_links = outer_links
        random.shuffle(inner_links)
        random.shuffle(outer_links)
        self.random_links = outer_links[:20]

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
        except:
            print('Cannot get content.')
            print(traceback.format_exc())

        try:
            soup = BeautifulSoup(content, "lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip javascript out
        except:
            print(traceback.format_exc())

        try:
            self.set_links(soup)
        except:
            self.links = []
            self.outer_links = []
            self.inner_links = []
            self.random_links = []
            print('Cannot get links of ', url)
            print(traceback.format_exc())

        try:
            if(soup.title.string is None):
                self.title = url
                self.title_words = []
            else:
                self.title = str(soup.title.string)
                self.title_words = self.text_to_words(self.title)
        except:
            self.title = url
            print('Cannot get title of ', url)
            print(traceback.format_exc())

        try:
            if(soup.body.text is None):
                self.text = ''
            else:
                self.text = str(soup.body.text)
        except:
            self.text = ''
            print('Cannot get text of ', url)
            print(traceback.format_exc())

        # convert all white space to sigle space
        self.text = ' '.join(
            filter(lambda x: not x == '', re.split('\s', self.text)))

        self.language = detect(self.text)

        # This version do not respond to mutibyte characters
        self.text = self.remove_non_ascii_character(self.text)
        self.summary = self.text[:500]
        self.words = self.text_to_words(self.text)


if __name__ == '__main__':
    t = "Hé ! bonjour, Monsieur du Corbeau.Que vous êtes joli ! Que vous me semblez beau !"
    detector = detect(t)
    print(detector)

    w = Webpage('https://en.wikipedia.org/wiki/X-Cops_(The_X-Files)')
    print(w.words)
