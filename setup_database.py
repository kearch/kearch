# -*- coding: utf-8 -*-

import sqlite3

dbname = 'keach.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

create_table = "CREATE TABLE tfidf (word text,link text,tfidf real)"
c.execute(create_table)
create_index = "CREATE INDEX tfidf_word_index on tfidf(word)"
c.execute(create_index)

create_table = "CREATE TABLE crawler (link text,last_date real)"
c.execute(create_table)
create_index = "CREATE INDEX crawler_date_index on crawler(last_date)"
c.execute(create_index)

create_table = "CREATE TABLE average_document (word text,number_of_document integer)"
c.execute(create_table)
create_index = "CREATE INDEX average_document_word_index on average_document(word)"
c.execute(create_index)

create_table = "CREATE TABLE size_of_average_document (size integer)"
c.execute(create_table)

create_table = "CREATE TABLE summary (link text,title text,summary text)"
c.execute(create_table)
create_index = "CREATE INDEX summary_link_index on summary(link)"
c.execute(create_index)
