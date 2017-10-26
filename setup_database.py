# -*- coding: utf-8 -*-

import sqlite3

dbname = 'keach.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

create_table = "CREATE TABLE tfidf (word text,link text,tfidf real)"
c.execute(create_table)
create_table = "CREATE TABLE crawler (link text,last_date real)"
c.execute(create_table)
create_table = "CREATE TABLE average_document (word text,number_of_document integer)"
c.execute(create_table)
create_table = "CREATE TABLE size_of_average_document (size integer)"
c.execute(create_table)
create_table = "CREATE TABLE summary (link text,title text,summary text)"
c.execute(create_table)
