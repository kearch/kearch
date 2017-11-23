import gensim
from gensim import corpora
import webpage

if __name__ == '__main__':
    urls = ['https://en.wikipedia.org/wiki/1966_New_York_City_smog',
            'https://en.wikipedia.org/wiki/Smog',
            'https://en.wikipedia.org/wiki/Portmanteau',
            'https://en.wikipedia.org/wiki/Compound_(linguistics)']
    texts = list(map(lambda u: webpage.Webpage(u).words, urls))
    # print(texts)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # print(corpus)
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=5, id2word=dictionary)
    print(lda.show_topics())

    test_text = [webpage.Webpage('https://en.wikipedia.org/wiki/Salvator_Mundi_(Leonardo').words]
    test_corpus = [dictionary.doc2bow(text) for text in test_text]
    print(test_corpus)
    for topics_per_document in lda[test_corpus]:
        print(topics_per_document)
