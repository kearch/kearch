# -*- coding: utf-8 -*-

import gensim
from gensim import corpora
import webpage
import argparse
import multiprocessing as mult
import pickle
import random
from sklearn.linear_model import SGDClassifier

n_topic = 200
n_urls = 2000
n_tests = 100
IN_TOPIC = 0
OUT_OF_TOPIC = 1


class TopicClassifier(object):
    def __init__(self):
        self.dictionary = corpora.Dictionary.load_from_text('gensim.dict')
        with open('lda.pickle', 'rb') as f:
            self.lda = pickle.load(f)
        with open('clf.pickle', 'rb') as f:
            self.clf = pickle.load(f)

    def classfy(self, words):
        test_text = [words]
        test_corpus = [self.dictionary.doc2bow(text) for text in test_text]
        res = list()
        for topics_per_document in self.lda[test_corpus]:
            r = self.clf.predict([trans_vector(topics_per_document)])
            res.append(r)
        if res[0][0] == 0:
            return IN_TOPIC
        else:
            return OUT_OF_TOPIC


def sum_vector(vs):
    a = [0 for i in range(0, n_topic)]
    for v in vs:
        for (i, j) in v:
            a[i] += j / len(vs)
    return a


def trans_vector(v):
    a = [0 for i in range(0, n_topic)]
    for (i, j) in v:
        a[i] += j
    return a


def url_to_words(url):
    try:
        w = webpage.Webpage(url)
        return w.words
    except:
        return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic_url_list", help="sample webpages about topic")
    parser.add_argument(
        "random_url_list", help="random webpages")
    parser.add_argument('--cache', help='use cache', action='store_true')
    parser.add_argument('--ntopic', help='number of topics', nargs=1)
    args = parser.parse_args()

    if args.ntopic is None:
        n_topic = int(args.ntopic)

    with open(args.topic_url_list, 'r') as f:
        topic_urls = f.readlines()
        topic_urls = list(map(lambda x: x.replace('\n', ''), topic_urls))
    f.close()
    with open(args.random_url_list, 'r') as f:
        random_urls = f.readlines()
        random_urls = list(map(lambda x: x.replace('\n', ''), random_urls))
    f.close()

    random.shuffle(topic_urls)
    topic_urls = topic_urls[:300]
    random.shuffle(random_urls)
    random_urls = random_urls[:300]

    n_gensim_urls = int(min(len(topic_urls), len(random_urls)) / 2)

    if not args.cache:
        p = mult.Pool(mult.cpu_count())
        texts = p.map(url_to_words, topic_urls[
                      :n_gensim_urls] + random_urls[:n_gensim_urls])
        texts = list(filter(lambda x: not x == [], texts))
        p.close()
        dictionary = corpora.Dictionary(texts)
        dictionary.save_as_text('gensim.dict')
        corpus = [dictionary.doc2bow(text) for text in texts]
        lda = gensim.models.ldamodel.LdaModel(
            corpus=corpus, num_topics=n_topic, id2word=dictionary)
        with open('lda.pickle', 'wb') as f:
            pickle.dump(lda, f)

        sc_samples = list()
        sc_labels = list()

        p = mult.Pool(mult.cpu_count())
        texts = p.map(
            url_to_words, topic_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        corpus = [dictionary.doc2bow(text) for text in texts]
        for topics_per_document in lda[corpus]:
            sc_samples.append(trans_vector(topics_per_document))
            sc_labels.append(IN_TOPIC)

        p = mult.Pool(mult.cpu_count())
        texts = p.map(
            url_to_words, random_urls[n_gensim_urls:2 * n_gensim_urls])
        p.close()
        texts = list(filter(lambda x: not x == [], texts))
        corpus = [dictionary.doc2bow(text) for text in texts]
        for topics_per_document in lda[corpus]:
            sc_samples.append(trans_vector(topics_per_document))
            sc_labels.append(OUT_OF_TOPIC)

        clf = SGDClassifier(loss="hinge", penalty="l2")
        print(sc_samples)
        print(sc_labels)
        clf.fit(sc_samples, sc_labels)
        with open('clf.pickle', 'wb') as f:
            pickle.dump(clf, f)

    else:
        dictionary = corpora.Dictionary.load_from_text('gensim.dict')
        with open('lda.pickle', 'rb') as f:
            lda = pickle.load(f)
        with open('clf.pickle', 'rb') as f:
            clf = pickle.load(f)

    print("some_urls")
    for u in ['https://www.haskell.org/',
              'https://en.wikipedia.org/wiki/Napoleon',
              'https://en.wikipedia.org/wiki/French_Revolutionary_Wars',
              'https://ocaml.org/']:
        c = TopicClassifier()
        w = webpage.Webpage(u)
        print(c.classfy(w.words), u)

    with open(args.topic_url_list, 'r') as f:
        topic_urls = f.readlines()
        topic_urls = list(map(lambda x: x.replace('\n', ''), topic_urls))
    f.close()
    with open(args.random_url_list, 'r') as f:
        random_urls = f.readlines()
        random_urls = list(map(lambda x: x.replace('\n', ''), random_urls))
    f.close()

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for u in topic_urls[n_urls:n_urls + n_tests]:
        c = TopicClassifier()
        w = webpage.Webpage(u)
        # print(c.classfy(w.words), u)
        if c.classfy(w.words) == IN_TOPIC:
            true_positive += 1
        else:
            true_negative += 1
    for u in random_urls[n_urls:n_urls + n_tests]:
        c = TopicClassifier()
        w = webpage.Webpage(u)
        # print(c.classfy(w.words), u)
        if c.classfy(w.words) == OUT_OF_TOPIC:
            false_negative += 1
        else:
            false_positive += 1
    print('TP=', true_positive, 'TN=', true_negative,
          'FP=', false_positive, 'FN=', false_negative)
