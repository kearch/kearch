# -*- coding: utf-8 -*-

import sys
from gensim import corpora
import webpage
import argparse
import multiprocessing as mult
import pickle
import random
from sklearn.naive_bayes import BernoulliNB
import abc

n_urls = 1000
n_tests = 100
IN_TOPIC = 0
OUT_OF_TOPIC = 1

CACHE_DIR = './classifier_cache/'


class Classifier(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def __init__(self, topic_url_list, random_url_list, language):
        pass

    @abc.abstractmethod
    def classfy(self, webpage):
        pass


class NBTopicClassifier(Classifier):
    def alist_to_vector(al, dictionary):
        r = [0 for i in range(len(dictionary))]
        for (i, f) in al:
            r[i] += f
        return r

    def url_to_words(url):
        w = webpage.create_webpage_with_cache(url)
        return w.words

    def __init__(self, topic_urls, random_urls, language):
        self.language = language
        n_gensim_urls = int(min(len(topic_urls), len(random_urls)) / 2)

        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(self.url_to_words, topic_urls[
                      :n_gensim_urls] + random_urls[:n_gensim_urls])
        sys.stderr.write("Downloading finish")

        texts = list(filter(lambda x: not x == [], texts))
        p.close()
        self.dictionary = corpora.Dictionary(texts)
        print('dictionary size = ', len(self.dictionary))

        sc_samples = list()
        sc_labels = list()

        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_words, topic_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary))
            sc_labels.append(IN_TOPIC)
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_words, random_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary))
            sc_labels.append(OUT_OF_TOPIC)

        self.clf = BernoulliNB()
        self.clf.fit(sc_samples, sc_labels)
        sys.stderr.write("Classifier making finish")

    def classfy(self, text):
        bow = self.dictionary.doc2bow(text)
        res = self.clf.predict([self.alist_to_vector(bow, self.dictionary)])
        return res[0]

    def classfy_log_probability(self, text):
        bow = self.dictionary.doc2bow(text)
        res = self.clf.predict_log_proba(
            [self.alist_to_vector(bow, self.dictionary)])
        return res[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic_url_list", help="sample webpages about topic")
    parser.add_argument(
        "random_url_list", help="random webpages")
    parser.add_argument('--cache', help='use cache', action='store_true')
    parser.add_argument('--ntopic', help='number of topics', nargs=1)
    args = parser.parse_args()

    with open(args.topic_url_list, 'r') as f:
        topic_urls1 = f.readlines()
        topic_urls1 = list(map(lambda x: x.replace('\n', ''), topic_urls1))
    f.close()
    with open(args.random_url_list, 'r') as f:
        random_urls1 = f.readlines()
        random_urls1 = list(map(lambda x: x.replace('\n', ''), random_urls1))
    f.close()

    random.shuffle(topic_urls1)
    topic_urls = topic_urls1[:n_urls]
    random.shuffle(random_urls1)
    random_urls = random_urls1[:n_urls]

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for u in topic_urls1[n_urls:n_urls + n_tests]:
        c = NBTopicClassifier(topic_urls, random_urls, 'en')
        w = webpage.create_webpage_with_cache(u)
        print(u, c.classfy_log_probability(w.words))
        if c.classfy(w.words) == IN_TOPIC:
            true_positive += 1
        else:
            true_negative += 1
    for u in random_urls1[n_urls:n_urls + n_tests]:
        c = NBTopicClassifier(topic_urls, random_urls, 'en')
        w = webpage.create_webpage_with_cache(u)
        if c.classfy(w.words) == OUT_OF_TOPIC:
            false_negative += 1
        else:
            false_positive += 1
    precision = true_positive / (true_positive + false_positive + 1)
    recall = true_positive / (true_positive + false_negative + 1)
    fmeasure = 2 * precision * recall / (precision + recall + 1)
    print('TP=', true_positive, 'TN=', true_negative,
          'FP=', false_positive, 'FN=', false_negative,
          'precision=', precision, 'recall=', recall, 'fmeasure=', fmeasure)
