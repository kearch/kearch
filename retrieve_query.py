# -*- coding: utf-8 -*-
import sqlite3

def retrieve(query):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search = """SELECT * FROM tfidf WHERE word = ? ORDER BY tfidf"""
    cur.execute(search,(query,))
    rows = cur.fetchall()
    res = list()
    for (w,l,t) in rows:
        res.append((l,t))
    return res

if __name__ == '__main__':
    res = retrieve('bird')
    print(res)

