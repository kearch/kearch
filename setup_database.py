# -*- coding: utf-8 -*-

import sqlite3

dbname = 'keach.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute("CREATE TABLE tfidf (word text,link text,tfidf real)")
c.execute("CREATE INDEX tfidf_word_index on tfidf(word)")

c.execute("CREATE TABLE title (word text,link text)")
c.execute("CREATE INDEX title_word_index on title(link)")

c.execute("CREATE TABLE pagerank_now (link word, pagerank real)")
c.execute("CREATE TABLE pagerank_next (link word, pagerank real)")

c.execute("CREATE TABLE link_to_date (link text,last_date real)")
c.execute("CREATE INDEX link_date_index on link_to_date(link)")

c.execute("CREATE TABLE date_to_link (link text,last_date real)")
c.execute("CREATE INDEX date_index on date_to_link(last_date)")

c.execute("CREATE TABLE average_document (word text,number_of_document integer)")
c.execute("CREATE INDEX average_document_word_index on average_document(word)")

c.execute("CREATE TABLE size_of_average_document (size integer)")
c.execute("CREATE TABLE summary (link text,title text,summary text)")
c.execute("CREATE INDEX summary_link_index on summary(link)")
