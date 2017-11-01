# -*- coding: utf-8 -*-

import sqlite3
import urllib3
from bs4 import BeautifulSoup
import time
import requests
import register_webpage
import argparse
import traceback
from urllib.parse import urlparse
import multiprocessing as mult
import datetime

class Webpage(object):
    def __init__(self, url, content):
        self.url = url
        self.content = content

def get_derive_link(w):
    try:
        html = w.content
        soup = BeautifulSoup(html,"html.parser")
    except:
        traceback.print_exc()
        return []

    res = list()
    ban_extension = set(["pdf","PDF","jpg","JPG","png","PNG"])
    for link in soup.findAll("a"):
        l = link.get("href")
        if l != None and ":" in l and l[:4]=='http' and l[-3:] not in ban_extension:
            l = urlparse(l)
            res.append(l.scheme + '://' + l.netloc + l.path)
    return res

def create_webpage(url):
    try:
        c = requests.get(url).content
        w = Webpage(url,c)
        return w
    except:
        return None

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

    select_crawler =  """SELECT * FROM crawler WHERE last_date < ? ORDER BY last_date LIMIT 20"""
    update_crawler = """UPDATE crawler SET last_date = ? WHERE link = ?"""
    while True:
        crawl_start = datetime.datetime.today()

        cur.execute(select_crawler,(time.time()-24*60*60,))
        rows = cur.fetchall()
        # print("rows=",rows)
        if len(rows) == 0:
            break

        us = list()
        for u,d in rows:
            cur.execute(update_crawler,(time.time(),u))
            conn.commit()
            us.append(u)

        p = mult.Pool(mult.cpu_count())
        print("Page download start",datetime.datetime.today())
        ws = p.map(create_webpage,us)
        print("Page download end  ",datetime.datetime.today())
        ws = list(filter(lambda x:x!=None,ws))

        print("Page register start",datetime.datetime.today())
        sqlss = p.map(register_webpage.register,ws)
        print("Page register end  ",datetime.datetime.today())

        print("Sql proccess  start",datetime.datetime.today())
        for ss in sqlss:
            for s in ss:
                cur.execute(s[0],s[1])
        conn.commit()
        print("Sql proccess  end  ",datetime.datetime.today())
        
        print("Derive link   start",datetime.datetime.today())
        derivess = p.map(get_derive_link,ws)
        print("Derive link   end  ",datetime.datetime.today())

        p.close()
        
        derives = list()
        for s in derivess:
            derives.extend(s)
        derives = list(set(derives))

        print("Sql proccess  start",datetime.datetime.today())
        for u in derives:
            cur.execute(search,(u,))
            rows = cur.fetchall()
            if len(rows) == 0:
                cur.execute(insert_crawler,(u,0))
        print("Sql proccess  end  ",datetime.datetime.today())

        crawl_end = datetime.datetime.today()
        print("It takes ",crawl_end-crawl_start," to process ",len(list(ws))," pages.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seed_url_list", help="initial url list to start crawl")
    args = parser.parse_args()
    with open(args.seed_url_list, 'r') as f:
        s = f.readlines()
        s = list(map(lambda x:x.replace('\n',''),s))
    f.close()
    crawl(s)
