# -*- coding: utf-8 -*-

import hashlib
import os
import json
from urllib.parse import urlparse
import requests
import urllib3
from bs4 import BeautifulSoup

CACHE_DIR = './downloader_cache/'


class DownloaderError(Exception):
    def __init__(self, message='This is default messege'):
        self.message = message


# This class have
# - self.url
# - self.links
# - self.inner_links
# - self.outer_links
# - self.title
# - self.text
# When the constructor cannot find any of them, it raise up DownloaderError.
class Downloader(object):
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

    def __init__(self, url, cache=False):
        cachefile = CACHE_DIR + \
            hashlib.sha256(url.encode('utf-8')).hexdigest() + '.json'
        if cache and os.path.exists(cachefile):
            with open(cachefile, 'r') as f:
                d = json.load(f)
                self.url = d['url']
                self.links = d['links']
                self.inner_links = d['inner_links']
                self.outer_links = d['outer_links']
                self.title = d['title']
                self.text = d['text']
                return

        self.url = url
        try:
            content = requests.get(self.url).content
        except requests.exceptions.RequestException:
            raise DownloaderError('Cannot get content.')
        except (UnicodeError, urllib3.exceptions.LocationValueError):
            raise DownloaderError('UnicodeError')
        except AttributeError:
            raise DownloaderError('AttributeError in download.')

        soup = BeautifulSoup(content, "lxml")
        for script in soup(["script", "style"]):
            script.extract()    # rip javascript out

        try:
            self.set_links(soup)
        except ValueError:
            raise DownloaderError('Cannot set links')

        try:
            self.title = str(soup.title.string)
            self.text = str(soup.body.text)
        except AttributeError:
            raise DownloaderError('Cannot get title or text')

        if cache:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cachefile, 'w') as f:
                d = {'url': self.url, 'links': self.links, 'inner_links': self.inner_links,
                     'outer_links': self.outer_links, 'title': self.title, 'text': self.text}
                json.dump(d, f)


if __name__ == '__main__':
    url = 'https://shedopen.deviantart.com/'
    d = Downloader(url, cache=True)
    print(d.title)
