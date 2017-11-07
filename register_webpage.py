# -*- coding: utf-8 -*-

import sqlite3
import subprocess
import nltk
from nltk.corpus import stopwords
from collections import Counter
import math
import urllib.request
from bs4 import BeautifulSoup
import re
from readability.readability import Document
import html2text
from crawler import Webpage
import sys

sys.setrecursionlimit(1000000)

# return title,summary,text
def webpage_to_info(w):
    soup = BeautifulSoup(w.content,"lxml")

    def title():
        try:
            if soup == None:
                return w.url
            return soup.title.string
        except:
            print("get exception in url_to_title")
            return w.url
    
    def summary():
        try:
            text = soup.body.text
            text = ' '.join(filter(lambda x:not x=='',re.split('\s', text)))
            return text[:500]
        except:
            print("Cannot summarize the url = ",w.url)
            return ""
    
    def main_text():
        try:
            text = soup.body.text
            text = ' '.join(filter(lambda x:not x=='',re.split('\s', text)))
        except:
            print('Cannot extract main text')
            text = ''
    
        text = remove_non_ascii_character(text)
        return text

    return (title(),summary(),main_text())

    
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
        if ord(c)<128:
            ret += c
        else:
            ret += " "
    return ret

def register(webpage):
    (title,summary,text) = webpage_to_info(webpage)
    # text = url_to_main_text(webpage)
    # title = url_to_title(webpage)
    # summary = url_to_summary(webpage)

    words = text_to_words(text)
    counter = list(Counter(words).most_common())
    sum_count = 0
    for w,c in counter:
        sum_count += c

    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search = """SELECT * FROM average_document WHERE word = ?"""

    tfidf = list()
    size_of_average_document = 0
    cur.execute("""SELECT * FROM size_of_average_document""")
    rows = cur.fetchall()
    size_of_average_document = rows[0][0]

    for w,c in counter:
        tf = float(c)/float(sum_count)
        cur.execute(search,(w,))
        rows = cur.fetchall()
        idf = 0
        if 0 < len(rows):
            idf = math.log2(float(size_of_average_document)/float(rows[0][1]))
        else:
            idf = math.log2(float(size_of_average_document)/1.0)
        tfidf.append((w,tf*idf))
    
    sqls = list()
    delete = """DELETE FROM tfidf WHERE link = ? """
    sqls.append((delete,(webpage.url,)))
    # cur.execute(delete,(webpage.url,))

    tfidf = sorted(tfidf,key=lambda x:x[1])
    for w,r in tfidf[0:100]:
        insert = """INSERT INTO tfidf VALUES (?,?,?)"""
        # cur.execute(insert,(w,webpage.url,r))
        sqls.append((insert,(w,webpage.url,r)))

    delete = """DELETE FROM summary WHERE link = ? """
    # cur.execute(delete,(webpage.url,))
    sqls.append((delete,(webpage.url,)))
    # print("url=",webpage.url)
    # print("summary=",summary)
    insert = """INSERT INTO summary VALUES (?,?,?)"""
    # cur.execute(insert,(webpage.url,title,summary))
    sqls.append((insert,(webpage.url,title,summary)))
    # conn.commit()
    return sqls

# if __name__ == '__main__':
     # text = url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # words = text_to_words(text)
     # counter = Counter(words)
     # for w,c in counter.most_common():
         # print(w,c)
     # print(words)
     # main_text = url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # url_to_title('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # print(url_to_summary('https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'))
     # print(url_to_main_text('https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'))
     # print(main_text)
