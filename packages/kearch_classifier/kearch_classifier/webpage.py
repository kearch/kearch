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
import sys

CACHE_DIR = './webpage_cache/'
BAN_EXTENTION = [
    ".3dm",
    ".3ds",
    ".3g2",
    ".3gp",
    ".7z",
    ".a",
    ".aac",
    ".adp",
    ".ai",
    ".aif",
    ".aiff",
    ".alz",
    ".ape",
    ".apk",
    ".ar",
    ".arj",
    ".asf",
    ".au",
    ".avi",
    ".bak",
    ".baml",
    ".bh",
    ".bin",
    ".bk",
    ".bmp",
    ".btif",
    ".bz2",
    ".bzip2",
    ".cab",
    ".caf",
    ".cgm",
    ".class",
    ".cmx",
    ".cpio",
    ".cr2",
    ".csv",
    ".cur",
    ".dat",
    ".dcm",
    ".deb",
    ".dex",
    ".djvu",
    ".dll",
    ".dmg",
    ".dng",
    ".doc",
    ".docm",
    ".docx",
    ".dot",
    ".dotm",
    ".dra",
    ".DS_Store",
    ".dsk",
    ".dts",
    ".dtshd",
    ".dvb",
    ".dwg",
    ".dxf",
    ".ecelp4800",
    ".ecelp7470",
    ".ecelp9600",
    ".egg",
    ".eol",
    ".eot",
    ".epub",
    ".exe",
    ".f4v",
    ".fbs",
    ".fh",
    ".fla",
    ".flac",
    ".fli",
    ".flv",
    ".fpx",
    ".fst",
    ".fvt",
    ".g3",
    ".gh",
    ".gif",
    ".graffle",
    ".gz",
    ".gzip",
    ".h261",
    ".h263",
    ".h264",
    ".icns",
    ".ico",
    ".ief",
    ".img",
    ".ipa",
    ".iso",
    ".jar",
    ".jpeg",
    ".jpg",
    ".jpgv",
    ".jpm",
    ".jxr",
    ".key",
    ".ktx",
    ".lha",
    ".lib",
    ".lvp",
    ".lz",
    ".lzh",
    ".lzma",
    ".lzo",
    ".m3u",
    ".m4a",
    ".m4v",
    ".mar",
    ".mdi",
    ".mht",
    ".mid",
    ".midi",
    ".mj2",
    ".mka",
    ".mkv",
    ".mmr",
    ".mng",
    ".mobi",
    ".mov",
    ".movie",
    ".mp3",
    ".mp4",
    ".mp4a",
    ".mpeg",
    ".mpg",
    ".mpga",
    ".mxu",
    ".nef",
    ".npx",
    ".numbers",
    ".o",
    ".oga",
    ".ogg",
    ".ogv",
    ".otf",
    ".pages",
    ".pbm",
    ".pcx",
    ".pdb",
    ".pdf",
    ".pea",
    ".pgm",
    ".pic",
    ".png",
    ".pnm",
    ".pot",
    ".potm",
    ".potx",
    ".ppa",
    ".ppam",
    ".ppm",
    ".pps",
    ".ppsm",
    ".ppsx",
    ".ppt",
    ".pptm",
    ".pptx",
    ".psd",
    ".pya",
    ".pyc",
    ".pyo",
    ".pyv",
    ".qt",
    ".rar",
    ".ras",
    ".raw",
    ".resources",
    ".rgb",
    ".rip",
    ".rlc",
    ".rmf",
    ".rmvb",
    ".rtf",
    ".rz",
    ".s3m",
    ".s7z",
    ".scpt",
    ".sgi",
    ".shar",
    ".sil",
    ".sketch",
    ".slk",
    ".smv",
    ".so",
    ".stl",
    ".sub",
    ".swf",
    ".tar",
    ".tbz",
    ".tbz2",
    ".tga",
    ".tgz",
    ".thmx",
    ".tif",
    ".tiff",
    ".tlz",
    ".ttc",
    ".ttf",
    ".txz",
    ".udf",
    ".uvh",
    ".uvi",
    ".uvm",
    ".uvp",
    ".uvs",
    ".uvu",
    ".viv",
    ".vob",
    ".war",
    ".wav",
    ".wax",
    ".wbmp",
    ".wdp",
    ".weba",
    ".webm",
    ".webp",
    ".whl",
    ".wim",
    ".wm",
    ".wma",
    ".wmv",
    ".wmx",
    ".woff",
    ".woff2",
    ".wrm",
    ".wvx",
    ".xbm",
    ".xif",
    ".xla",
    ".xlam",
    ".xls",
    ".xlsb",
    ".xlsm",
    ".xlsx",
    ".xlt",
    ".xltm",
    ".xltx",
    ".xm",
    ".xmind",
    ".xpi",
    ".xpm",
    ".xwd",
    ".xz",
    ".z",
    ".zip",
    ".zipx"]
BAN_DOMAIN = ["twitter.com", "2ch.sc", "tumblr.com"]


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

    def is_normal_link(self, link):
        if link is None:
            return False
        for b in BAN_DOMAIN:
            if b in link:
                return False

        filename = link.split("/")[-1]
        ext = os.path.splitext(filename)[1]
        print("extention = ", ext, file=sys.stderr)
        # last condition is excluding web archives
        if link is None or link[:4] != 'http' or ":" not in link or \
                ext in BAN_EXTENTION or '://' in link[7:]:
                return False
        return True

    def set_links(self, soup):
        row_links = list(soup.findAll("a"))

        res = list()
        for rl in row_links:
            link = rl.get("href")
            if self.is_normal_link(link):
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
        if not self.is_normal_link(url):
            raise WebpageError('This link is excluded by "is_normal_link" \
                    function in Webpage class')
        if len(url) > 200:
            raise WebpageError('URL is too long.')
        try:
            print('webpage.py start downloading ' + url, file=sys.stderr)
            content = requests.get(self.url, timeout=5).content
            print('webpage.py finish downloading ' + url, file=sys.stderr)
        except requests.exceptions.RequestException:
            raise WebpageError('Cannot get content.')
        except (UnicodeError, urllib3.exceptions.LocationValueError):
            raise WebpageError('UnicodeError')
        except AttributeError:
            raise WebpageError('AttributeError in download.')

        print('webpage.py start BeautifulSoup ' + url, file=sys.stderr)
        soup = BeautifulSoup(content, "lxml")
        print('webpage.py finish BeautifulSoup ' + url, file=sys.stderr)
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
            print('webpage.py start detecting language ' + url,
                  file=sys.stderr)
            self.language = langdetect.detect(self.text)
            print('webpage.py finish detecting language ' + url,
                  file=sys.stderr)
            if not self.language == language:
                raise WebpageError("Language doesn't match.")
        except langdetect.lang_detect_exception.LangDetectException:
            raise WebpageError('Cannot detect language.')

        print('webpage.py start text_to_words for title ' + url,
              file=sys.stderr)
        self.title_words = self.text_to_words(
            self.title, language=self.language)
        print('webpage.py finish text_to_words for title ' + url,
              file=sys.stderr)
        # convert all white space to sigle space
        # self.text = ' '.join(
        # filter(lambda x: not x == '', re.split('\s', self.text)))

        # This version do not respond to mutibyte characters
        self.summary = self.text[:500]
        print('webpage.py start text_to_words for text ' + url,
              file=sys.stderr)
        self.words = self.text_to_words(self.text, language=self.language)
        print('webpage.py finish text_to_words for text ' + url,
              file=sys.stderr)


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
