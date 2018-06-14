# -*- coding: utf-8 -*-

import math
import webpage
import nb_topic_detect
import title_topic_detect
import sys
from collections import Counter
import average_document
import json

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

    tc = title_topic_detect.TitleTopicClassifier()
    if tc.classfy(w.title_words) == title_topic_detect.IN_TOPIC:
        return w
    elif tc.classfy_log_probability(w.title_words)[title_topic_detect.IN_TOPIC] < \
            confidence_threshold:
        c = nb_topic_detect.TopicClassifier()
        if c.classfy(w.words) == nb_topic_detect.IN_TOPIC:
            return w
        return None


def url_to_json_string(url):
    print('Start download ', url)
    web = url_to_webpage(url)
    print('End download ', url)
    ret = dict()
    ret['url'] = url
    ret['title_words'] = web.title_words
    ret['summary'] = web.summary
    ret['tfidf'] = web_to_tfidf(web)
    return json.dumps(ret)


if __name__ == '__main__':
    # Test codes

    w = url_to_webpage('https://shedopen.deviantart.com/')
    print(w.title_words)
    tfidf = web_to_tfidf(w)
    print(tfidf)
    json_string = url_to_json_string('https://shedopen.deviantart.com/')
    print(json_string)
