#coding:utf-8

from sklearn.cluster import KMeans, MiniBatchKMeans
import random
from collections import Counter
import math
import re
import time
from numpy import array

def main():
    km = KMeans(n_clusters=3,init='random')

    X = []

    with open("../data/train_data.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    all_words = []
    for line in lines:
        sentiment,sentence = line.split('\t')
        words = sentence.split(' ')
        all_words.extend(words)

    freq_words = Counter(all_words).items()
    freq_words.sort(key=lambda x:x[1], reverse=True)
    
    filter_words = set()
    for i,j in freq_words:
        if len(i) == 3 or j < 15:
            continue
        filter_words.add(i)

    for line in lines:
        x = []
        sentiment,sentence = line.split('\t')
        words = sentence.split(' ')
        words = set(words)
        for word in filter_words:
            if word in words:
                x.append(tfidf(word,sentence,lines))
            else:
                x.append(0.0001)
#        print x
        X.append(x)
    predict_result = km.fit_predict(X)
    for i in predict_result:
        print i

def n_containing(word,bloblist):
    return sum(1 for blob in bloblist if word in blob)

def tf(word,blob):
    return blob.count(word)*1.0/len(blob.split(' '))

def idf(word,bloblist):
    return math.log(len(bloblist)*1.0/(1 + n_containing(word,bloblist)))

def tfidf(word,blob,bloblist):
    return tf(word,blob)*idf(word,bloblist)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print end-start
