# -*- coding: utf-8 -*-

import sqlite3
import urllib3
from bs4 import BeautifulSoup
import time
import requests
import register_webpage

def get_derive_link(url):
    html = ""
    try:
        html = (requests.get(url)).content
    finally:
        return []

    soup = BeautifulSoup(html,"html.parser")
    res = list()
    for link in soup.findAll("a"):
        if link.get("href") != None and ":" in link.get("href"):
            res.append(link.get("href"))
    return res

def crawl(initial_url_list):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search = """SELECT * FROM crawler WHERE link = ?"""
    insert_crawler = """INSERT INTO crawler VALUES (?,?)"""

    for url in initial_url_list:
        cur.execute(search,(url,))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(insert_crawler,(url,0))
    conn.commit()

    select_crawler =  """SELECT * FROM crawler WHERE last_date < ? ORDER BY last_date DESC LIMIT 1000"""
    update_crawler = """UPDATE crawler SET last_date = ? WHERE link = ?"""
    while True:
        cur.execute(select_crawler,(time.time()-24*60*60,))
        rows = cur.fetchall()
        print("rows=",rows)
        if len(rows) == 0:
            break

        derives = list()
        for u,d in rows:
            cur.execute(update_crawler,(time.time(),u))
            conn.commit()
            register_webpage.register(u)
            ds = get_derive_link(u)
            derives.extend(ds)
        derives = list(set(derives))
        derives = filter(lambda x:x[:4]=='http',derives)
        print("derives=",derives)
        for u in derives:
            cur.execute(search,(u,))
            rows = cur.fetchall()
            if len(rows) == 0:
                cur.execute(insert_crawler,(u,0))

if __name__ == '__main__':
    crawl(["https://stackoverflow.com/questions/36516183/what-should-i-use-instead-of-urlopen-in-urllib3"])
