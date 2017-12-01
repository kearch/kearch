# -*- coding: utf-8 -*-

import sqlite3


class Pagerank(object):
    def __init__(self):
        self.dbname = 'keach.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    # web のリンク先をpagerank_next に追加する
    def add(self, web):
        select_pagerank_now = """SELECT * FROM pagerank_now WHERE link = ?"""
        insert_pagerank_next = """INSERT INTO pagerank_next VALUES (?,?)"""
        self.cur.execute(select_pagerank_now, (web.url,))
        rows = self.cur.fetchall()
        rank = 1.0
        if 0 < len(rows):
            rank = rows[0][1]
        for l in web.links:
            self.cur.execute(insert_pagerank_next, (l, rank))
        self.conn.commit()

    # pagerank_nowとpagerank_nextを入れ替える
    # def renew():
