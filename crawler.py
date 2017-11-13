# -*- coding: utf-8 -*-

import sqlite3
import urllib3
import time
import requests
import register_webpage
import argparse
from urllib.parse import urlparse
import multiprocessing as mult
import datetime
from bs4 import BeautifulSoup
import random
import time
import timeout_decorator
import re
import traceback
import types


class Webpage(object):
    def remove_non_ascii_character(self,text):
        ret = ""
        for c in list(text):
            if ord(c)<128:
                ret += c
            else:
                ret += " "
        return ret
    
    def filter_links(self,links):
        res = list()
        ban_domain = list(["web.archive.org","twitter.com","2ch.sc"])
        ban_extension = list(["pdf","PDF","jpg","JPG","png","PNG","gif","GIF"])
    
        def check_domain(link):
            for b in ban_domain:
                if b in link:
                    return False
            return True
    
        for link in links:
            l = link.get("href")
            if l != None and ":" in l and l[:4]=='http' and l[-3:] not in ban_extension and check_domain(l):
                l = urlparse(l)
                res.append(l.scheme + '://' + l.netloc + l.path)
        random.shuffle(res)
        res = res[:20]
        return res

    def __init__(self, url):
        self.url = url
        try:
            content = requests.get(self.url).content
        except:
            print('Cannot get content.')

        try:
            soup = BeautifulSoup(content,"lxml")
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
        except:
            print('Cannot make soup for ',url)

        try:
            self.links = self.filter_links(list(soup.findAll("a")))
        except:
            self.links = []
            print('Cannot get links of ',url)

        try:
            if(soup.title.string is None):
                self.title = url
            else:
                self.title = str(soup.title.string)
        except:
            self.title = url
            print('Cannot get title of ',url)

        try:
            if(soup.body.text is None):
                self.text = ''
            else:
                self.text = str(soup.body.text)
        except:
            self.text = ''
            print('Cannot get text of ',url)

        self.text = ' '.join(filter(lambda x:not x=='',re.split('\s', self.text)))
        self.summary = self.text[:500]
        self.text = self.remove_non_ascii_character(self.text)

def create_webpage(url):
    try:
        w = create_webpage1(url)
        return w
    except:
        print('Timeout in create_webpage.')
        return None

@timeout_decorator.timeout(10)
def create_webpage1(url):
    try:
        w = Webpage(url)
        return w
    except:
        print('Cannot make webpage of ',url)
        traceback.print_exc()
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
        print("Page download takes",datetime.datetime.today()-download_start)
        ws = list(filter(lambda x:x!=None,ws))

        register_start = datetime.datetime.today()
        print("Page register start",datetime.datetime.today())
        sqlss = p.map(register_webpage.register,ws)
        print("Page register takes",datetime.datetime.today()-register_start)
        p.close()

        sql_start = datetime.datetime.today()
        print("Sql proccess  start",datetime.datetime.today())
        for ss in sqlss:
            for s in ss:
                # print(s)
                cur.execute(s[0],s[1])
        conn.commit()
        
        derives = list()
        for w in ws:
            derives.extend(w.links)
        derives = list(set(derives))

        insert_data = list()
        for u in derives:
            cur.execute(search_link_to_date,[u])
            rows = cur.fetchall()
            if len(rows) == 0:
                r = random.random()
                insert_data.append([u,r])
                # To select domains randomly, set the crawl time random in the range of [0,1)
        cur.executemany(insert_link_to_date,insert_data)
        cur.executemany(insert_date_to_link,insert_data)
        conn.commit()
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
