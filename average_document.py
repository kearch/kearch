# -*- coding: utf-8 -*-
import register_webpage
import argparse
import sqlite3
from crawler import create_webpage

def make_average_document(links):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    size = len(links)
    cur.execute("""INSERT INTO size_of_average_document VALUES (?)""",(size,))

    word_count = dict()

    for l in links:
        webpage = create_webpage(l)
        ws = list(set(register_webpage.text_to_words(webpage.text)))
        for w in ws:
            if w not in word_count:
                word_count[w]=1
            else:
                word_count[w]+=1

    search = """SELECT * FROM average_document WHERE word = ?"""
    insert = """INSERT INTO average_document VALUES (?,?)"""
    update = """UPDATE average_document SET number_of_document = ? WHERE word = ?"""
    for (w,c) in word_count.items():
        cur.execute(insert,(w,c))
    conn.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('document_list_file')
    args = parser.parse_args()

    with open(args.document_list_file, 'r') as f:
        l = f.readlines()
        l = list(map(lambda x:x.replace('\n',''),l))
        make_average_document(l)
