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

def url_to_title(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url),"lxml")
        if soup == None:
            return url
        return soup.title.string
    except:
        print("get exception in url_to_title")
        return url

def url_to_summary(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url),"lxml")
        text = soup.body.text
        text = ' '.join(filter(lambda x:not x=='',re.split('\s', text)))
        return text[:500]
    except:
        print("Cannot summarize the url = ",url)
        return ""

def url_to_main_text(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url),"lxml")
        text = soup.body.text
        text = ' '.join(filter(lambda x:not x=='',re.split('\s', text)))
    except:
        print('Cannot extract main text')
        text = ''

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
        if ord(c)<128:
            ret += c
        else:
            ret += " "
    return ret

def register(url):
    text = url_to_main_text(url)
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
    
    delete = """DELETE FROM tfidf WHERE link = ? """
    cur.execute(delete,(url,))

    for w,r in tfidf:
        insert = """INSERT INTO tfidf VALUES (?,?,?)"""
        cur.execute(insert,(w,url,r))
    conn.commit()

    delete = """DELETE FROM summary WHERE link = ? """
    cur.execute(delete,(url,))
    summary = url_to_summary(url)
    print("url=",url)
    print("summary=",summary)
    title = url_to_title(url)
    insert = """INSERT INTO summary VALUES (?,?,?)"""
    cur.execute(insert,(url,title,summary))
    conn.commit()

if __name__ == '__main__':
     # text = url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # words = text_to_words(text)
     # counter = Counter(words)
     # for w,c in counter.most_common():
         # print(w,c)
     # print(words)
     # main_text = url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # url_to_title('https://en.wikipedia.org/wiki/Spotted_green_pigeon')
     # print(url_to_summary('https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'))
     print(url_to_main_text('https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'))
     # print(main_text)
