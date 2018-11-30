# -*- coding: utf-8 -*-

import sys
from gensim import corpora
import pickle
from sklearn.naive_bayes import BernoulliNB
import abc
import tempfile
import zipfile
import os

PARAMS_FILE = 'evaluater_cache_params.zip'


class AbsEvaluater(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def learn_params(self, summaries):
        pass

    # This function dump all parameters to one json.
    @abc.abstractclassmethod
    def dump_params(self, filename):
        pass

    @abc.abstractclassmethod
    def load_params(self, filename):
        pass

    @abc.abstractmethod
    def evaluate(self, query):
        pass


class Evaluater(AbsEvaluater):
    def alist2vec(self, al, dictionary):
        r = [0 for i in range(len(dictionary))]
        for (i, f) in al:
            r[i] += f
        return r

    def learn_params(self, summaries):
        print('evaluater.py -- Making Classifier start',
              file=sys.stderr)
        texts = list()
        for s in summaries:
            texts.append(list(summaries[s].keys()))
        self.dictionary = corpora.Dictionary(texts)

        host2label = dict()
        self.label2host = dict()
        hosts = list(summaries.keys())
        for i in range(0, len(hosts)):
            host2label[hosts[i]] = i
            self.label2host[i] = hosts[i]

        sc_samples = list()
        sc_labels = list()

        for h in hosts:
            v = [(self.dictionary.token2id[w], f)
                 for w, f in summaries[h].items()]
            sc_samples.append(self.alist2vec(v, self.dictionary))
            sc_labels.append(host2label[h])

        self.clf = BernoulliNB()
        self.clf.fit(sc_samples, sc_labels)
        print('evaluater.py -- Making Classifier finish',
              file=sys.stderr)

    def evaluate(self, query):
        v = self.dictionary.doc2bow(query)
        p = self.clf.predict_proba([self.alist2vec(v, self.dictionary)])

        res = dict()
        for i in range(0, len(p[0])):
            res[self.label2host[i]] = p[0][i]
        return res

    def dump_params(self, filename):
        with tempfile.TemporaryDirectory() as tmpd:
            self.dictionary.save(os.path.join(
                tmpd, 'gensim_dictionary.pickle'))
            with open(os.path.join(tmpd, 'label2host.pickle'), 'wb') as f:
                pickle.dump(self.label2host, f)
            with open(os.path.join(tmpd, 'nb_clf.pickle'), 'wb') as f:
                pickle.dump(self.clf, f)
            with zipfile.ZipFile(filename, 'w') as f:
                f.write(os.path.join(tmpd, 'gensim_dictionary.pickle'),
                        arcname='gensim_dictionary.pickle')
                f.write(os.path.join(tmpd, 'nb_clf.pickle'),
                        arcname='nb_clf.pickle')
                f.write(os.path.join(tmpd, 'label2host.pickle'),
                        arcname='label2host.pickle')

    def load_params(self, filename):
        with tempfile.TemporaryDirectory() as tmpd:
            with zipfile.ZipFile(filename) as z:
                z.extractall(tmpd)
                self.dictionary = corpora.Dictionary.load(
                    os.path.join(tmpd, 'gensim_dictionary.pickle'))
                with open(os.path.join(tmpd, 'nb_clf.pickle'), 'rb') as f:
                    self.clf = pickle.load(f)
                with open(os.path.join(tmpd, 'label2host.pickle'), 'rb') as f:
                    self.label2host = pickle.load(f)


if __name__ == '__main__':
    summaries = {'192.168.99.100': {'google': 100, 'facebook': 20},
                 '192.168.99.200': {'haskell': 200, 'ocaml': 200}}
    query1 = ['google', 'yahoo']
    query2 = ['haskell', 'yahoo']
    e = Evaluater()
    e.learn_params(summaries)
    e.dump_params(PARAMS_FILE)
    e.load_params(PARAMS_FILE)
    print('label2host = ', e.label2host)
    print('Evaluation for ', query1, ' = ', e.evaluate(query1))
    print('Evaluation for ', query2, ' = ', e.evaluate(query2))
