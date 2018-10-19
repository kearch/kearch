# -*- coding: utf-8 -*-
import argparse
import multiprocessing as mult
import os
import pickle
import sys
import traceback

import kearch_classifier.webpage

CACHE_FILE = 'average_document.pickle'


class AverageDocumentError(Exception):
    def __init__(self, message='This is default messege'):
        self.message = message


def get_words(link_and_language):
    link = link_and_language[0]
    language = link_and_language[1]
    ws = list()
    try:
        web = kearch_classifier.webpage.create_webpage_with_cache(link, language)
        ws = list(set(web.words))
    except kearch_classifier.webpage.WebpageError:
        traceback.print_exc()
    return ws


def make_average_document_cache(links, language):
    word_count = dict()

    sys.stderr.write('Start download\n')
    p = mult.Pool(mult.cpu_count() * 3)
    link_and_language = list()
    for l in links:
        link_and_language.append((l, language))
    wss = p.map(get_words, link_and_language)
    sys.stderr.write('End download\n')

    for ws in wss:
        for w in ws:
            if w not in word_count:
                word_count[w] = 1
            else:
                word_count[w] += 1
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(word_count, f)
    return word_count


def average_document_dict():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            d = pickle.load(f)
            return d
    else:
        raise AverageDocumentError('There is no CACHE_FILE.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('document_list_file')
    parser.add_argument('language')
    args = parser.parse_args()

    with open(args.document_list_file, 'r') as f:
        link = list(map(lambda x: x.replace('\n', ''), f.readlines()))
        make_average_document_cache(link, args.language)
