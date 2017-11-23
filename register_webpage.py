# -*- coding: utf-8 -*-

import sqlite3
from collections import Counter
import math
import sys
import timeout_decorator

sys.setrecursionlimit(1000000)


def register(webpage):
    try:
        s = register1(webpage)
        return s
    except:
        print('Timeout in register.')
        return []


@timeout_decorator.timeout(20)
def register1(webpage):
    counter = list(Counter(webpage.words).most_common())
    sum_count = 0
    for w, c in counter:
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

    for w, c in counter:
        tf = float(c) / float(sum_count)
        cur.execute(search, (w,))
        rows = cur.fetchall()
        idf = 0
        if 0 < len(rows):
            idf = math.log2(float(size_of_average_document) /
                            float(rows[0][1]))
        else:
            idf = math.log2(float(size_of_average_document) / 1.0)
        tfidf.append((w, tf * idf))

    sqls = list()
    delete = """DELETE FROM tfidf WHERE link = ? """
    sqls.append((delete, (webpage.url,)))

    tfidf = sorted(tfidf, key=lambda x: x[1], reverse=True)
    for w, r in tfidf[0:100]:
        insert = """INSERT INTO tfidf VALUES (?,?,?)"""
        sqls.append((insert, (w, webpage.url, r)))

    delete = """DELETE FROM summary WHERE link = ? """
    sqls.append((delete, (webpage.url,)))
    insert = """INSERT INTO summary VALUES (?,?,?)"""
    sqls.append((insert, (webpage.url, webpage.title, webpage.summary)))
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
