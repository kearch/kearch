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
    search = """SELECT * FROM summary WHERE link = ?"""
    res = list()
    for (w,l,t) in rows:
        cur.execute(search,(l,))
        rows = cur.fetchall()
        if 0 < len(rows):
            res.append((l,rows[0][1],rows[0][2],t))
    return res

if __name__ == '__main__':
    res = retrieve(sys.argv[1])
    res.sort(key=lambda x:x[1],reverse=True)
    print(res)

