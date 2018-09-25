# -*- coding: utf-8 -*-

import math
import sys
from collections import Counter

import average_document
import classifier
import webpage

confidence_threshold = -1.0e-10
n_outer_derives = 100
n_inner_derives = 20


def web_to_tfidf(web):
    counter = list(Counter(web.words).most_common())
    sum_count = 0
    for w, c in counter:
        sum_count += c

    tfidf = dict()
    average_document_dict = average_document.average_document_dict()
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
    try:
        w = webpage.Webpage(url)
    except webpage.WebpageError:
        print('Cannot make webpage of ', url, file=sys.stderr)
        return None

    cls = classifier.Classifier()
    cls.load_params(classifier.PARAMS_FILE)
    if cls.classify(w) == classifier.IN_TOPIC:
        return w
    else:
        None


def url_to_json(url):
    print('Start download ', url, file=sys.stderr)
    web = url_to_webpage(url)
    print('End download ', url, file=sys.stderr)
    print('web = ', web, file=sys.stderr)

    if web is not None:
        ret = dict()
        ret['url'] = url
        ret['title'] = web.title
        ret['title_words'] = web.title_words
        ret['summary'] = web.summary
        ret['tfidf'] = web_to_tfidf(web)
        ret['inner_links'] = web.inner_links
        ret['outer_links'] = web.outer_links
        print('ret =', ret, file=sys.stderr)
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
