# -*- coding: utf-8 -*-
import sqlite3
import sys

dbname = 'keach.db'
max_limit_of_retrive = 30


class Retriever(object):
    def __init__(self):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def isInTitle(self, query, url):
        search_title = """SELECT * FROM title WHERE link = ? and word = ?"""
        self.cur.execute(search_title, (url, query))
        rows = self.cur.fetchall()
        if 0 < len(rows):
            return True
        return False

    def retrieve(self, query):
        search_tfidf = """SELECT * FROM tfidf WHERE word = ? ORDER BY tfidf DESC LIMIT ?"""
        self.cur.execute(search_tfidf, (query, max_limit_of_retrive))
        rows = self.cur.fetchall()
        search_summary = """SELECT * FROM summary WHERE link = ?"""
        search_pagerank = """SELECT * FROM pagerank_now WHERE link = ?"""
        res = list()
        # w = word ,l = link, t = tfidf
        for (w, l, t) in rows:
            self.cur.execute(search_summary, (l,))
            rows_summary = self.cur.fetchall()
            self.cur.execute(search_pagerank, (l,))
            rows_pagerank = self.cur.fetchall()
            if 0 < len(rows_summary):
                p = 1.0
                if 0 < len(rows_pagerank):
                    # rows_pagerank[0][0] = link, rows_pagerank[0][1] = pagerank
                    p = rows_pagerank[0][1]
                # rows_summary[0][0] = link, rows_summary[0][1] = title, rows_summary[0][2] = summary
                # if the query is in the url, add 1 to the evaluation
                if self.isInTitle(query, l):
                    res.append(
                        (l, rows_summary[0][1], rows_summary[0][2], t * p + 1))
                else:
                    res.append(
                        (l, rows_summary[0][1], rows_summary[0][2], t * p))
        res.sort(key=lambda x: x[3], reverse=True)
        return res


def retrieve(query):
    r = Retriever()
    return r.retrieve(query)


if __name__ == '__main__':
    res = retrieve(sys.argv[1])
    res.sort(key=lambda x: x[1], reverse=True)
    print(res)
