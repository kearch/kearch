import gensim
from gensim import corpora
import webpage
import argparse


def urls_to_words(urls):
    words = list()
    for u in urls:
        w = webpage.Webpage(u)
        words.append(w.words)
    return words

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic_url_list", help="sample webpages about topic")
    parser.add_argument(
        "random_url_list", help="random webpages")
    args = parser.parse_args()
    with open(args.topic_url_list, 'r') as f:
        topic_urls = f.readlines()
        topic_urls = list(map(lambda x: x.replace('\n', ''), topic_urls))
    f.close()
    with open(args.random_url_list, 'r') as f:
        random_urls = f.readlines()
        random_urls = list(map(lambda x: x.replace('\n', ''), random_urls))
    f.close()

    # urls = ['https://en.wikipedia.org/wiki/1966_New_York_City_smog',
    #         'https://en.wikipedia.org/wiki/Smog',
    #         'https://en.wikipedia.org/wiki/Portmanteau',
    #         'https://en.wikipedia.org/wiki/Compound_(linguistics)']
    # texts = list(map(lambda u: webpage.Webpage(u).words, urls))
    texts = urls_to_words(topic_urls) + urls_to_words(random_urls)
    # print(texts)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print(corpus)
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus, num_topics=10, id2word=dictionary)
    print(lda.show_topics())

    print("topic_urls")
    for u in topic_urls:
        test_text = [webpage.Webpage(u).words]
        test_corpus = [dictionary.doc2bow(text) for text in test_text]
        for topics_per_document in lda[test_corpus]:
            print(topics_per_document)

    print("random_urls")
    for u in random_urls:
        test_text = [webpage.Webpage(u).words]
        test_corpus = [dictionary.doc2bow(text) for text in test_text]
        for topics_per_document in lda[test_corpus]:
            print(topics_per_document)



    # test_text = [webpage.Webpage(
    #     'https://en.wikipedia.org/wiki/Salvator_Mundi_(Leonardo').words]
    # test_corpus = [dictionary.doc2bow(text) for text in test_text]
    # # print(test_corpus)
    # for topics_per_document in lda[test_corpus]:
    #     print(topics_per_document)
