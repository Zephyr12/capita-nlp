# coding: utf-8
import gensim.downloader as api
from gensim.models import KeyedVectors
import nltk
import numpy as np
from scipy.cluster.vq import kmeans2 
from scipy.cluster.hierarchy import linkage
import itertools

# word2vec = KeyedVectors.load_word2vec_format("../../GoogleNews-vectors-negative300.bin", binary=True)
word2vec = api.load("glove-twitter-25")

def pairwise(iterable):
    a,b = itertools.tee(iterable)
    return zip(a, itertools.islice(b, 1, None))

def x2vec(sent, tokenizer=nltk.word_tokenize, model=word2vec):
    words = list(
            map(
                np.concatenate,
                pairwise(
                    map(
                        lambda x: word2vec[x],
                        filter(
                            lambda w: w in word2vec,
                            tokenizer(sent)
                            )
                        )
                    )
                )
            )
    words = [word2vec[word] for word in nltk.word_tokenize(sent) if word in word2vec]
    return sum(words) / (len(words) + 1)

def doc2vec(doc):
    sentence_vectors =list(map(x2vec, nltk.sent_tokenize(doc.lower())))
    return sum(sentence_vectors) / (len(sentence_vectors) + 1)

def split(data, n=2):
    _, labels = kmeans2(np.array([t[0] for t in data]), n, minit='points')
    a = [[data[i] for i, c in enumerate(labels) if c == cat] for cat in range(n)]
    return a

def centres(data, n=2):
    centres, _ = kmeans2(np.array([t[0] for t in data]), n, minit='points')
    return centres

def split_raw(data, n=2):
    return [[d[1] for d in cls] for cls in split([(doc2vec(doc['raw_text']), doc) for doc in data], n)]

def interpret(data, n=2):
    return [word2vec.most_similar(positive=[ctr], topn=1) for ctr in centres([(doc2vec(doc), doc) for doc in data], n)]
