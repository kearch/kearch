# -*- coding: utf-8 -*-

import sqlite3
import time
import register_webpage
import argparse
import multiprocessing as mult
import datetime
import timeout_decorator
import webpage
import nb_topic_detect
import title_topic_detect
from title_topic_detect import IN_TOPIC
import pagerank
import random
import sys

confidence_threshold = -1.0e-10
n_outer_derives = 100
n_inner_derives = 20


def create_webpage(url):
    try:
        w = create_webpage1(url)
    except timeout_decorator.TimeoutError:
        print('Timeout in create_webpage.', file=sys.stderr)
        return None
    except webpage.WebpageError:
        print('Cannot make webpage of ', url, file=sys.stderr)
        return None

    tc = title_topic_detect.TitleTopicClassifier()
    if tc.classfy(w.title_words) == title_topic_detect.IN_TOPIC:
        return w
    elif tc.classfy_log_probability(w.title_words)[IN_TOPIC] < \
            confidence_threshold:
        c = nb_topic_detect.TopicClassifier()
        if c.classfy(w.words) == nb_topic_detect.IN_TOPIC:
            return w
        return None


@timeout_decorator.timeout(10)
def create_webpage1(url):
    w = webpage.Webpage(url)
    return w


def crawl(initial_url_list):
    dbname = 'keach.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    search_link_to_date = """SELECT * FROM link_to_date WHERE link = ?"""
    insert_link_to_date = """insert into link_to_date values (?,?)"""
    insert_date_to_link = """insert into date_to_link values (?,?)"""

    for url in initial_url_list:
        cur.execute(search_link_to_date, (url,))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(insert_date_to_link, (url, 0))
            cur.execute(insert_link_to_date, (url, 0))
    conn.commit()

    ranker = pagerank.Pagerank()
    select_top_20 = """SELECT * FROM date_to_link WHERE last_date < ? \
            ORDER BY last_date LIMIT 20"""
    update_link_to_date = """UPDATE link_to_date SET last_date = ? \
            WHERE link = ? AND last_date = ?"""
    update_date_to_link = """UPDATE date_to_link SET last_date = ? \
            WHERE last_date = ? AND link = ?"""
    while True:
        crawl_start = datetime.datetime.today()

        cur.execute(select_top_20, (time.time() - 24 * 60 * 60,))
        rows = cur.fetchall()
        # print("rows=",rows)
        if len(rows) == 0:
            break

        us = list()
        for u, d in rows:
            cur.execute(update_link_to_date, (time.time(), u, d))
            cur.execute(update_date_to_link, (time.time(), d, u))
            conn.commit()
            us.append(u)

        download_start = datetime.datetime.today()
        print("Page download and webpage initialization start",
              datetime.datetime.today())
        p = mult.Pool(mult.cpu_count())
        ws = p.map(create_webpage, us)
        print("Page download and webpage initialization takes",
              datetime.datetime.today() - download_start)
        ws = list(filter(lambda x: x is not None and x.language == 'en', ws))
        register_start = datetime.datetime.today()
        print("Page register start", datetime.datetime.today())
        sqlss = p.map(register_webpage.register, ws)
        p.close()
        print("Page register takes",
              datetime.datetime.today() - register_start)

        derives_start = datetime.datetime.today()
        print("Derive link proccess to register start",
              datetime.datetime.today())
        outer_derives = list()
        inner_derives = list()
        for w in ws:
            outer_derives.extend(w.outer_links)
            inner_derives.extend(w.inner_links)
        outer_derives = list(set(outer_derives))[:n_outer_derives]
        inner_derives = list(set(inner_derives))[:n_inner_derives]
        random.shuffle(outer_derives)
        random.shuffle(inner_derives)
        outer_derives = outer_derives[:n_outer_derives]
        inner_derives = inner_derives[:n_inner_derives]
        print("Derive link proccess to register takes",
              datetime.datetime.today() - derives_start)

        sql_start = datetime.datetime.today()
        print("Sql proccess to register start", datetime.datetime.today())
        for ss in sqlss:
            for s in ss:
                cur.execute(s[0], s[1])
        conn.commit()

        insert_data = list()
        for u in outer_derives + inner_derives:
            cur.execute(search_link_to_date, [u])
            rows = cur.fetchall()
            if len(rows) == 0:
                insert_data.append([u, 0])
        cur.executemany(insert_link_to_date, insert_data)
        cur.executemany(insert_date_to_link, insert_data)
        conn.commit()
        print("Sql proccess to register takes",
              datetime.datetime.today() - sql_start)

        pagerank_start = datetime.datetime.today()
        print("Pagerank proccess start", datetime.datetime.today())
        for w in ws:
            ranker.add(w)
        ranker.check_renew()
        print("Pagerank process takes",
              datetime.datetime.today() - pagerank_start)

        print("It takes ", datetime.datetime.today() - crawl_start,
              " to process ", len(list(ws)), " pages.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "seed_url_list", help="initial url list to start crawl")
    args = parser.parse_args()
    with open(args.seed_url_list, 'r') as f:
        s = f.readlines()
        s = list(map(lambda x: x.replace('\n', ''), s))
    f.close()
    crawl(s)
