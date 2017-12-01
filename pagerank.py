# -*- coding: utf-8 -*-

import sqlite3


class Pagerank(object):
    def __init__(self):
        self.dbname = 'keach.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        self.pagerank_next_size = 1000000

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
    def renew(self):
        select_pagerank_next = """SELECT * FROM pagerank_next ORDER BY link"""
        create_pagerank_tmp = """CREATE TABLE pagerank_tmp (link word, pagerank real)"""
        insert_pagerank_tmp = """INSERT INTO pagerank_tmp VALUES (?,?)"""

        self.cur.execute(select_pagerank_next)
        rows = self.cur.fetchall()
        rank = dict()
        for l, v in rows:
            if l in rank:
                rank[l] += v
            else:
                rank[l] = v
        ratio = float(len(rank)) / float(len(rows))
        self.cur.execute(create_pagerank_tmp)
        for l, v in rank.items():
            self.cur.execute(insert_pagerank_tmp, (l, v * ratio))
        self.conn.commit()
        self.cur.execute("""DROP TABLE pagerank_now""")
        self.cur.execute("""DROP INDEX pagerank_index""")
        self.cur.execute("""ALTER TABLE pagerank_tmp RENAME TO pagerank_now""")
        self.cur.execute("""CREATE INDEX pagerank_index on pagerank_now(link)""")
        self.cur.execute("""DROP TABLE pagerank_next""")
        self.cur.execute("""CREATE TABLE pagerank_next AS SELECT * FROM pagerank_now""")
        self.cur.execute("""VACUUM""")
        self.conn.commit()

    # サイズが大きくなってきたら更新する
    def check_renew(self):
        self.cur.execute("""SELECT COUNT(*) FROM pagerank_next""")
        rows = self.cur.fetchall()
        if self.pagerank_next_size < rows[0][0]:
            self.renew()
