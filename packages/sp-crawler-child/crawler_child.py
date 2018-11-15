# -*- coding: utf-8 -*-

import math
import sys
import os
import base64
import datetime
from collections import Counter

import kearch_classifier.average_document as ave
import kearch_classifier.classifier
import kearch_classifier.webpage
from kearch_common.requester import KearchRequester, RequesterError

DATABASE_HOST = 'sp-db.kearch.svc.cluster.local'
DATABASE_PORT = 3306
REQUESTER_NAME = 'sp-crawler-child'

confidence_threshold = -1.0e-10
n_outer_derives = 100
n_inner_derives = 20

timestamp = dict()


def web_to_tfidf(web):
    counter = list(Counter(web.words).most_common())
    sum_count = 0
    for w, c in counter:
        sum_count += c

    tfidf = dict()
    average_document_dict = ave.average_document_dict()
    size_of_average_document = len(average_document_dict)

    for w, c in counter:
        tf = float(c) / float(sum_count)
        word_count_in_average = 0
        if w in average_document_dict:
            word_count_in_average = average_document_dict[w]
        idf = 0
        if 0 < word_count_in_average:
            idf = math.log2(float(size_of_average_document) /
                            float(word_count_in_average))
        else:
            idf = math.log2(float(size_of_average_document) / 1.0)
        tfidf[w] = tf * idf
    return tfidf


def url_to_webpage(url):
    print('Start checking parameter files.', file=sys.stderr)
    update_param_file(kearch_classifier.classifier.PARAMS_FILE)
    update_param_file(ave.CACHE_FILE)
    print('End checking parameter files.', file=sys.stderr)

    try:
        w = kearch_classifier.webpage.Webpage(url)
    except kearch_classifier.webpage.WebpageError:
        print('Cannot make webpage of ', url, file=sys.stderr)
        return None

    cls = kearch_classifier.classifier.Classifier()
    cls.load_params(kearch_classifier.classifier.PARAMS_FILE)
    if cls.classify(w) == kearch_classifier.classifier.IN_TOPIC:
        return w
    else:
        None


def update_param_file(filename):
    db_req = KearchRequester(
        DATABASE_HOST, DATABASE_PORT, REQUESTER_NAME, conn_type='sql')
    try:
        ret = db_req.request(path='/sp/db/check_binary_file_timestamp',
                             params={'name': filename})
        dt = ret['updated_at']
        print('db:', dt, file=sys.stderr)
        if filename not in timestamp or timestamp[filename] < dt:
            timestamp[filename] = dt
            ret = db_req.request(path='/sp/db/pull_binary_file',
                                 params={'name': filename})
            body = base64.b64decode(ret['body'].encode())
            with open(filename, 'wb') as f:
                f.write(body)
    except RequesterError:
        return


def url_to_json(url):
    print('Start download ', url, file=sys.stderr)
    web = url_to_webpage(url)
    print('End download ', url, file=sys.stderr)
    print('web = ', web, file=sys.stderr)

    if web is not None:
        ret = dict()
        ret['url'] = url
        ret['title'] = web.title
        ret['text'] = web.text
        ret['tfidf'] = web_to_tfidf(web)
        ret['inner_links'] = web.inner_links
        ret['outer_links'] = web.outer_links
        print("ret['url'] =", ret['url'], file=sys.stderr)
        return ret
    else:
        return {}


if __name__ == '__main__':
    # Test codes

    w = url_to_webpage('https://shedopen.deviantart.com/')
    print(w.title_words)
    tfidf = web_to_tfidf(w)
    print(tfidf)
    url_json = url_to_json('https://shedopen.deviantart.com/')
    print(url_json)
