# -*- coding: utf-8 -*-

import sys
from gensim import corpora
import webpage
import argparse
import multiprocessing as mult
# import pickle
import random
from sklearn.naive_bayes import BernoulliNB
import abc

n_urls = 1000
n_tests = 100
IN_TOPIC = 0
OUT_OF_TOPIC = 1

CACHE_DIR = './classifier_cache/'


class Classifier(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def learn_params(self, topic_url_list, random_url_list, language):
        pass

    @abc.abstractclassmethod
    def dump_params(self):
        pass

    @abc.abstractclassmethod
    def load_params(self, json):
        pass

    @abc.abstractmethod
    def classfy(self, webpage):
        pass


# You can change the implementation of classifer.
# When you change it, the classifer class must inherit Classifier class.
# In short, you must implment 4 functions in Classifier class.
class NBTopicClassifier(Classifier):
    def alist_to_vector(self, al, dictionary):
        r = [0 for i in range(len(dictionary))]
        for (i, f) in al:
            r[i] += f
        return r

    def url_to_words(self, url):
        w = webpage.create_webpage_with_cache(url)
        return w.words

    def url_to_title_words(self, url):
        w = webpage.create_webpage_with_cache(url)
        return w.title_words

    def learn_params_body(self, topic_urls, random_urls, language):
        n_gensim_urls = int(min(len(topic_urls), len(random_urls)) / 2)

        sys.stderr.write('classifer.py -- Downloading start\n')
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(self.url_to_words, topic_urls[
                      :n_gensim_urls] + random_urls[:n_gensim_urls])
        sys.stderr.write('classifer.py -- Downloading finish\n')

        texts = list(filter(lambda x: not x == [], texts))
        p.close()
        self.dictionary_body = corpora.Dictionary(texts)
        sys.stderr.write('classifer.py -- Dictionary size = ' + str(len(self.dictionary_body)) + '\n')

        sys.stderr.write('classifer.py -- Making Classifier for main text start\n')
        sc_samples = list()
        sc_labels = list()
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_words, topic_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary_body.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary_body))
            sc_labels.append(IN_TOPIC)
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_words, random_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary_body.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary_body))
            sc_labels.append(OUT_OF_TOPIC)

        self.clf_body = BernoulliNB()
        self.clf_body.fit(sc_samples, sc_labels)
        sys.stderr.write('classifer.py -- Making Classifier for main text finish\n')

    def learn_params_title(self, topic_urls, random_urls, language):
        print('classifer.py -- Downloading start', file=sys.stderr)
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(self.url_to_title_words,
                      topic_urls[:n_urls] + random_urls[:n_urls])
        p.close()
        print('classifer.py -- Downloading finish', file=sys.stderr)

        texts = list(filter(lambda x: not x == [], texts))
        self.dictionary_title = corpora.Dictionary(texts)
        print('classifer.py -- dictionary size = ', len(self.dictionary_title))

        sc_samples = list()
        sc_labels = list()

        print('classifer.py -- Making Classifier for title start', file=sys.stderr)
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_title_words, topic_urls[:n_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary_title.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary_title))
            sc_labels.append(IN_TOPIC)
        p = mult.Pool(mult.cpu_count() * 3)
        texts = p.map(
            self.url_to_title_words, random_urls[:n_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        bows = [self.dictionary_title.doc2bow(text) for text in texts]
        for bow in bows:
            sc_samples.append(self.alist_to_vector(bow, self.dictionary_title))
            sc_labels.append(OUT_OF_TOPIC)

        self.clf_title = BernoulliNB()
        self.clf_title.fit(sc_samples, sc_labels)
        print('classifer.py -- Making Classifier for title end', file=sys.stderr)

    def learn_params(self, topic_urls, random_urls, language):
        self.language = language
        self.learn_params_body(topic_urls, random_urls, language)
        self.learn_params_title(topic_urls, random_urls, language)

    def classfy(self, webpage):
        bow_body = self.dictionary_body.doc2bow(webpage.words)
        res_body = self.clf_body.predict([self.alist_to_vector(bow_body, self.dictionary_body)])

        bow_title = self.dictionary_title.doc2bow(webpage.title_words)
        res_title = self.clf_title.predict([self.alist_to_vector(bow_title, self.dictionary_title)])
        if res_title[0] == IN_TOPIC or res_body[0] == IN_TOPIC:
            return IN_TOPIC
        else:
            return OUT_OF_TOPIC

    def classfy_log_probability(self, text):
        bow = self.dictionary_body.doc2bow(text)
        res = self.clf_body.predict_log_proba(
            [self.alist_to_vector(bow, self.dictionary_body)])
        return res[0]

    def dump_params(self):
        pass

    def load_params(self):
        pass


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

    cls = NBTopicClassifier()
    cls.learn_params(topic_urls, random_urls, 'en')

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for u in topic_urls1[n_urls:n_urls + n_tests]:
        w = webpage.create_webpage_with_cache(u)
        print(u, cls.classfy_log_probability(w.words))
        if cls.classfy(w) == IN_TOPIC:
            true_positive += 1
        else:
            true_negative += 1
    for u in random_urls1[n_urls:n_urls + n_tests]:
        w = webpage.create_webpage_with_cache(u)
        if cls.classfy(w) == OUT_OF_TOPIC:
            false_negative += 1
        else:
            false_positive += 1
    precision = true_positive / (true_positive + false_positive + 1)
    recall = true_positive / (true_positive + false_negative + 1)
    fmeasure = 2 * precision * recall / (precision + recall + 1)
    print('classifier.py -- TP=', true_positive, 'TN=', true_negative,
          'FP=', false_positive, 'FN=', false_negative,
          'precision=', precision, 'recall=', recall, 'fmeasure=', fmeasure)
