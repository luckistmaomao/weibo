#coding:utf-8

from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.metrics import confusion_matrix
import os
import jieba
import random
import numpy as np
from collections import Counter

import sys

def test_classifier(classifier,features,labels):
    skf = StratifiedKFold(labels,10)
    accuracies = list()
    for train_index,test_index in skf:
        X = features[train_index]
        y = labels[train_index]
        classifier.fit(X,y)
        predict_labels = classifier.predict(features[test_index])

        reuslt_labels = labels[test_index]
        count = 0
        cm = confusion_matrix(reuslt_labels,predict_labels)
    #    print cm
        for i in range(len(predict_labels)):
            if reuslt_labels[i] == predict_labels[i]:
                count += 1

        tmp = Counter(zip(reuslt_labels,predict_labels))
        accuracy = count*1.0/len(predict_labels)
        accuracies.append(accuracy)
        print "Test case %s accuracy is %s" % (len(accuracies),accuracy)
    print 'mean:',np.mean(accuracies)
    print 'var:',np.var(accuracies)
    print 'std',np.std(accuracies)

def cal_tf_and_tfidf(corpus):
    vectorizer = CountVectorizer(min_df=1)
    M = vectorizer.fit_transform(corpus)
    tf = M.toarray()
    transformer = TfidfTransformer()
    N = transformer.fit_transform(tf)
    tfidf = N.toarray()
    return tf,tfidf

def main():
    weibo_objs = list()
    with open('weibo.txt') as f:
        for line in f:
            line = line.strip() 
            weibo_obj = dict()
            label,content = line.split('\t')
            weibo_obj['label'] = label
            weibo_obj['words'] = content.split(' ')
            weibo_objs.append(weibo_obj)

    #random.seed(0)
    random.shuffle(weibo_objs)    #随机打乱

    corpus = [' '.join(weibo_obj['words']) for weibo_obj in weibo_objs]
    tf,tfidf = cal_tf_and_tfidf(corpus)

    labels = [weibo_obj['label'] for weibo_obj in weibo_objs]
    labels = np.array(labels)

    nbd = MultinomialNB()
    nbcg = GaussianNB()
    #test_classifier(nbd,tf,labels)
    weights = {'spam':1.0,'positive':10.0,'negative':10.0,'neutral':1.5}
    clf = svm.LinearSVC(class_weight=weights)
    test_classifier(clf,tfidf,labels)
    
if __name__ == "__main__":
    main()
