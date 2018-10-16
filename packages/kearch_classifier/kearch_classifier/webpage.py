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
import urllib3
import janome.tokenizer

CACHE_DIR = './webpage_cache/'


class WebpageError(Exception):
    def __init__(self, message='This is default messege'):
        self.message = 'WebpageError: ' + message


def create_webpage_with_cache(url, language='en'):
    cachefile = CACHE_DIR + \
        hashlib.sha256(url.encode('utf-8')).hexdigest() + '.pickle'
    if os.path.exists(cachefile):
        with open(cachefile, 'rb') as f:
            w = pickle.load(f)
            return w
    else:
        w = Webpage(url, language=language)
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
            # TEMPORAL SUPPORT FOR DATABASE LIMIT
            if len(link) > 200:
                continue
            if link.netloc == self_loc:
                inner_links.append(link.scheme + '://' +
                                   link.netloc + link.path)
            else:
                outer_links.append(link.scheme + '://' +
                                   link.netloc + link.path)
        self.inner_links = inner_links
        self.outer_links = outer_links

    def text_to_words(self, text, language='en'):
        if language == 'en':
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
        elif language == 'ja':
            t = janome.tokenizer.Tokenizer()
            r = re.compile('^(名詞|動詞).*')
            words = list()
            tokens = t.tokenize(text)
            for tk in tokens:
                if r.match(tk.part_of_speech) is not None:
                    words.append(tk.base_form)
            return words
        else:
            raise WebpageError('Cannot tokeninze language = ' + language + '.')

    def __init__(self, url, language='en'):
        self.language = language
        self.url = url
        if len(url) > 200:
            raise WebpageError('URL is too long.')
        try:
            content = requests.get(self.url, timeout=5).content
        except requests.exceptions.RequestException:
            raise WebpageError('Cannot get content.')
        except (UnicodeError, urllib3.exceptions.LocationValueError):
            raise WebpageError('UnicodeError')
        except AttributeError:
            raise WebpageError('AttributeError in download.')

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
            if not self.language == language:
                raise WebpageError("Language doesn't match.")
        except langdetect.lang_detect_exception.LangDetectException:
            raise WebpageError('Cannot detect language.')

        self.title_words = self.text_to_words(
            self.title, language=self.language)
        # convert all white space to sigle space
        # self.text = ' '.join(
        # filter(lambda x: not x == '', re.split('\s', self.text)))

        # This version do not respond to mutibyte characters
        self.summary = self.text[:500]
        self.words = self.text_to_words(self.text, language=self.language)


if __name__ == '__main__':
    t = "こんにちは。わたしはスーパーマンです。"
    detector = langdetect.detect(t)
    print(detector)

    url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    # url = 'https://news.ycombinator.com/'
    url = 'https://nginx-c-function.github.io/'
    url = 'https://www.haskell.org/'
    w = Webpage(url, 'en')
    print(w.text)
    # print(w.text)
