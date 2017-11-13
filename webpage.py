from bs4 import BeautifulSoup
import requests
import re
import random
from urllib.parse import urlparse
from polyglot.detect import Detector


class Webpage(object):
    def remove_non_ascii_character(self, text):
        ret = ""
        for c in list(text):
            if ord(c) < 128:
                ret += c
            else:
                ret += " "
        return ret

    def filter_links(self, links):
        ban_domain = list(["web.archive.org", "twitter.com", "2ch.sc"])
        ban_extension = list(
            ["pdf", "PDF", "jpg", "JPG", "png", "PNG", "gif", "GIF"])

        def check_domain(link):
            for b in ban_domain:
                if b in link:
                    return False
            return True

        innner_link = list()
        outer_link = list()
        self_loc = urlparse(self.url).netloc
        for link in links:
            href = link.get("href")
            if href is not None and ":" in href and href[:4] == 'http' and \
                    href[-3:] not in ban_extension and check_domain(href):
                href = urlparse(href)
                if href.netloc == self_loc:
                    innner_link.append(href.scheme + '://' + href.netloc + href.path)
                else:
                    outer_link.append(href.scheme + '://' + href.netloc + href.path)
        random.shuffle(innner_link)
        random.shuffle(outer_link)
        ninner = min(len(innner_link), 10)
        return (innner_link[:ninner] + outer_link[:20-ninner])

    def __init__(self, url):
        self.url = url
        try:
            content = requests.get(self.url).content
        except:
            print('Cannot get content.')

        try:
            soup = BeautifulSoup(content, "lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
        except:
            print('Cannot make soup for ', url)

        try:
            self.links = self.filter_links(list(soup.findAll("a")))
        except:
            self.links = []
            print('Cannot get links of ', url)

        try:
            if(soup.title.string is None):
                self.title = url
            else:
                self.title = str(soup.title.string)
        except:
            self.title = url
            print('Cannot get title of ', url)

        try:
            if(soup.body.text is None):
                self.text = ''
            else:
                self.text = str(soup.body.text)
        except:
            self.text = ''
            print('Cannot get text of ', url)

        self.text = ' '.join(
            filter(lambda x: not x == '', re.split('\s', self.text)))
        self.summary = self.text[:500]
        self.text = self.remove_non_ascii_character(self.text)
        detector = Detector(self.text)
        self.language = detector.language.code

if __name__ == '__main__':
    t = "Hé ! bonjour, Monsieur du Corbeau.Que vous êtes joli ! Que vous me semblez beau !"
    detector = Detector(t)
    print(detector)
