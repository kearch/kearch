# -*- coding: utf-8 -*-

import math
import timeout_decorator
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
    size_of_average_document = average_document.size_of_average_document()

    for w, c in counter:
        tf = float(c) / float(sum_count)
        word_count_in_average = average_document.count_word_average_document(w)
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
    elif tc.classfy_log_probability(w.title_words)[title_topic_detect.IN_TOPIC] < \
            confidence_threshold:
        c = nb_topic_detect.TopicClassifier()
        if c.classfy(w.words) == nb_topic_detect.IN_TOPIC:
            return w
        return None


def url_to_json_string(url):
    web = url_to_webpage(url)
    ret = dict()
    ret['title_words'] = web.title_words
    ret['summary'] = web.summary
    ret['tfidf'] = web_to_tfidf(web)
    return json.dumps(ret)


@timeout_decorator.timeout(10)
def create_webpage1(url):
    w = webpage.Webpage(url)
    return w


if __name__ == '__main__':
    # Test codes

    # w = url_to_webpage('https://shedopen.deviantart.com/')
    # print(w.title_words)
    # tfidf = web_to_tfidf(w)
    # print(tfidf)
    json_string = url_to_json_string('https://shedopen.deviantart.com/')
    print(json_string)
