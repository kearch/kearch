# -*- coding: utf-8 -*-

import subprocess
import nltk
from nltk.corpus import stopwords
from collections import Counter

def url_to_main_text(url):
    cmd = 'w3m "' + url + '"'
    text = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]
    text = remove_non_ascii_character(text)
    return text

def text_to_words(text):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    words = list(map(lambda x:x.lower(),words))
    words = list(filter(lambda x:x not in stop_words,words))
    return words

def remove_non_ascii_character(text):
    ret = ""
    for c in list(text):
        if c<128:
            ret += chr(c)
        else:
            ret += " "
    return ret

if __name__ == '__main__':
     text = url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     words = text_to_words(text)
     counter = Counter(words)
     for w,c in counter.most_common():
         print(w,c)
     # print(words)
