#coding:utf-8


import jieba
import random
import re
from data_manager import Timer
import sys
import nltk
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')

def extract_features(tweet):
    words = tweet[1]
    sentiment = tweet[0]
    features = {}
    for word in words:
        features['contains %s' % (word)] = True
    return features

def get_words_in_tweets(tweets):
    all_words = []
    for (sentiment, words) in tweets:
        all_words.extend(words_filter(words))
        return all_words

def words_filter(words):
    stop_words_set = set() 
    with open('../data/stopwords.dic') as f:
        for word in f:
            stop_words_set.add(word.strip())
    filtered_words = []
    for word in words:
        if word.encode('utf-8') not in stop_words_set:
            filtered_words.append(word)
    return filtered_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def get_top_words(tweets):
    all_words = get_words_in_tweets(tweets)
    word_features = get_word_features(all_words)
    for word in word_features:
        print word

def main():
    with open('../data/sample20140819.txt') as f:
        lines = f.readlines()

    tweets = []
    spam_tweets = []
    pos_tweets = []
    neg_tweets = []
    neu_tweets = []
    for line in lines:
        content = line.split('\t')[1].strip()
        content = re.sub('http:\/\/t\.cn\/[\da-zA-Z]+','',content)
        content = content.replace(' ','')
        sentiment = line.split('\t')[0]
        words = jieba.cut(content,cut_all=False)
        words = list(words)
        words = words_filter(words)
        tweet = (sentiment,words)
        tweets.append(tweet)
        if sentiment == 'spam':
            spam_tweets.append(tweet)
        elif sentiment == 'positive':
            pos_tweets.append(tweet)
        elif sentiment == 'negative':
            neg_tweets.append(tweet)
        elif sentiment == 'neutral':
            neu_tweets.append(tweet)

    with open('../data/train_data.txt','w') as f:
        lines = []
        for tweet in tweets:
            sentiment = tweet[0]
            words = tweet[1]
            line = '%s\t%s' % (sentiment,' '.join(words))
            lines.append(line+'\n')
        f.writelines(lines)

#    print 'positive tweets count',len(pos_tweets)
#    print 'spam tweets count',len(spam_tweets)
#    print 'neutral tweets count',len(neu_tweets)
#    print 'negative tweets count',len(neg_tweets)
#
#    print "positive"
#    get_top_words(pos_tweets)
#
#    print "spam"
#    get_top_words(spam_tweets)
#
#    print 'neutral'
#    get_top_words(neu_tweets)
#
#    print 'negative'
#    get_top_words(neg_tweets)

if __name__ == "__main__":
    with Timer() as t:
        main()
