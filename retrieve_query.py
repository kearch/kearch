# -*- coding: utf-8 -*-
import sqlite3
import sys


def retrieve(query):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search_tfidf = """SELECT * FROM tfidf WHERE word = ? ORDER BY tfidf DESC"""
    cur.execute(search_tfidf, (query,))
    rows = cur.fetchall()
    search_summary = """SELECT * FROM summary WHERE link = ?"""
    search_pagerank = """SELECT * FROM pagerank_now WHERE link = ?"""
    res = list()
    # w = word ,l = link, t = tfidf
    for (w, l, t) in rows:
        cur.execute(search_summary, (l,))
        rows_summary = cur.fetchall()
        cur.execute(search_pagerank, (l,))
        rows_pagerank = cur.fetchall()
        if 0 < len(rows_summary):
            p = 1.0
            if 0 < len(rows_pagerank):
                # rows_pagerank[0][0] = link, rows_pagerank[0][1] = pagerank
                p = rows_pagerank[0][1]
            # rows_summary[0][0] = link, rows_summary[0][1] = title, rows_summary[0][2] = summary
            res.append((l, rows_summary[0][1], rows_summary[0][2], t * p))
    res.sort(key=lambda x: x[3])
    return res


if __name__ == '__main__':
    res = retrieve(sys.argv[1])
    res.sort(key=lambda x: x[1], reverse=True)
    print(res)
