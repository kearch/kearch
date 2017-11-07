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
from bs4 import BeautifulSoup
import random
from timeout_decorator import timeout, TimeoutError
import database

class Webpage(object):
    def __init__(self, url, content):
        self.url = url
        self.content = content

def get_derive_link(w):
    try:
        soup = BeautifulSoup(w.content,"lxml")
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
    search_link_to_date = """SELECT * FROM link_to_date WHERE link = ?"""
    insert_link_to_date = """insert into link_to_date values (?,?)"""
    insert_date_to_link = """insert into date_to_link values (?,?)"""

    for url in initial_url_list:
        cur.execute(search_link_to_date,(url,))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(insert_date_to_link,(url,random.random()))
            cur.execute(insert_link_to_date,(url,random.random()))
            # To select domains randomly, set the crawl time random in the range of [0,1)
    conn.commit()

    select_top_20 =  """SELECT * FROM date_to_link WHERE last_date < ? ORDER BY last_date LIMIT 20"""
    update_link_to_date = """UPDATE link_to_date SET last_date = ? WHERE link = ? AND last_date = ?"""
    update_date_to_link = """UPDATE date_to_link SET last_date = ? WHERE last_date = ? AND link = ?"""
    while True:
        crawl_start = datetime.datetime.today()

        cur.execute(select_top_20,(time.time()-24*60*60,))
        rows = cur.fetchall()
        # print("rows=",rows)
        if len(rows) == 0:
            break

        us = list()
        for u,d in rows:
            r = random.random()
            cur.execute(update_link_to_date,(time.time()+r,u,d))
            cur.execute(update_date_to_link,(time.time()+r,d,u))
            conn.commit()
            us.append(u)

        download_start = datetime.datetime.today()
        p = mult.Pool(mult.cpu_count())
        print("Page download start",datetime.datetime.today())
        ws = p.map(create_webpage,us)
        # print("Page download end  ",datetime.datetime.today())
        print("Page download takes",datetime.datetime.today()-download_start)
        ws = list(filter(lambda x:x!=None,ws))

        register_start = datetime.datetime.today()
        print("Page register start",datetime.datetime.today())
        sqlss = p.map(register_webpage.register,ws)
        # print("Page register end  ",datetime.datetime.today())
        print("Page register takes",datetime.datetime.today()-register_start)

        sql_start = datetime.datetime.today()
        print("Sql proccess  start",datetime.datetime.today())
        for ss in sqlss:
            for s in ss:
                # print(s)
                cur.execute(s[0],s[1])
        conn.commit()
        # print("Sql proccess  end  ",datetime.datetime.today())
        print("Sql proccess  takes",datetime.datetime.today()-sql_start)
       
        derive_start = datetime.datetime.today()
        print("Derive link   start",datetime.datetime.today())
        derivess = p.map(get_derive_link,ws)
        # print("Derive link   end  ",datetime.datetime.today())
        print("Derive link   takes",datetime.datetime.today()-sql_start)

        p.close()
        
        derives = list()
        for s in derivess:
            derives.extend(s)
        derives = list(set(derives))

        sql_start = datetime.datetime.today()
        print("Sql proccess  start",datetime.datetime.today())
        insert_data = list()
        for u in derives:
            cur.execute(search_link_to_date,[u])
            rows = cur.fetchall()
            if len(rows) == 0:
                r = random.random()
                insert_data.append([u,r])
                # To select domains randomly, set the crawl time random in the range of [0,1)
        sd = database.insert_multiple_data('link_to_date',insert_data)
        for s,d in sd:
            cur.execute(s,d)
        sd = database.insert_multiple_data('date_to_link',insert_data)
        for s,d in sd:
            cur.execute(s,d)
        # cur.executemany(insert_link_to_date,insert_data)
        # cur.executemany(insert_date_to_link,insert_data)
        conn.commit()
        # print("Sql proccess  end  ",datetime.datetime.today())
        print("Sql proccess  takes",datetime.datetime.today()-sql_start)

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
