# -*- coding: utf-8 -*-
import register_webpage
import argparse
import sqlite3

def make_average_document(links):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    size = len(links)
    cur.execute("""INSERT INTO size_of_average_document VALUES (?)""",(size,))

    for l in links:
        t = register_webpage.url_to_main_text(l)
        ws = list(set(register_webpage.text_to_words(t)))
        search = """SELECT * FROM average_document WHERE word = ?"""
        insert = """INSERT INTO average_document VALUES (?,?)"""
        update = """UPDATE average_document SET number_of_document = ? WHERE word = ?"""
        for w in ws:
            cur.execute(search,(w,))
            rows = cur.fetchall()
            if [] == rows:
                cur.execute(insert,(w,1))
                conn.commit()
            else:
                c = rows[0][1]
                cur.execute(update,(c+1,w))
                conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--document-list-file',required=True)
    args = parser.parse_args()

    with open(args.document_list_file, 'r') as f:
        l = f.readlines()
        l = list(map(lambda x:x.replace('\n',''),l))
        make_average_document(l)
