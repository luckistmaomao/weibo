#coding:utf-8
import jieba
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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


with open('../data/raw_test_data.txt') as f:
    lines = [ line.strip() for line in f.readlines() ] 

tweets = []
for line in lines:
    content = line
    content = re.sub('http:\/\/t\.cn\/[\da-zA-Z]+','',content)
    content = content.replace(' ','')
    sentiment = line.split('\t')[0]
    words = jieba.cut(content,cut_all=False)
    words = words_filter(list(words))
    tweets.append(words)
    
with open('../data/test_data.txt','w') as f:
    for tweet in tweets:
        f.write(' '.join(tweet)+'\n')
