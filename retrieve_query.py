# -*- coding: utf-8 -*-
import sqlite3
import sys

def retrieve(query):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search = """SELECT * FROM tfidf WHERE word = ? ORDER BY tfidf DESC"""
    cur.execute(search,(query,))
    rows = cur.fetchall()
    res = list()
    for (w,l,t) in rows:
        res.append((l,t))
    return res

if __name__ == '__main__':
    res = retrieve(sys.argv[1])
    res.sort(key=lambda x:x[1],reverse=True)
    print(res)

