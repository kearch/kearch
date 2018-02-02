# -*- coding: utf-8 -*-
import argparse
import sqlite3
import webpage
import traceback
import multiprocessing as mult

def get_words(link):
    print(link)
    ws = list()
    try:
        web = webpage.Webpage(link)
        ws = list(set(web.words))
    except:
        traceback.print_exc()
    return ws

def make_average_document(links):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    size = len(links)
    cur.execute("""INSERT INTO size_of_average_document VALUES (?)""", (size,))

    word_count = dict()

    p = mult.Pool(mult.cpu_count())
    wss = p.map(get_words, links)

    for ws in wss:
        for w in ws:
            if w not in word_count:
                word_count[w] = 1
            else:
                word_count[w] += 1

    # search = """SELECT * FROM average_document WHERE word = ?"""
    insert = """INSERT INTO average_document VALUES (?,?)"""
    # update = """UPDATE average_document SET number_of_document = ?
    # WHERE word = ?"""
    for (w, c) in word_count.items():
        cur.execute(insert, (w, c))
    conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('document_list_file')
    args = parser.parse_args()

    with open(args.document_list_file, 'r') as f:
        link = list(map(lambda x: x.replace('\n', ''), f.readlines()))
        make_average_document(link)
