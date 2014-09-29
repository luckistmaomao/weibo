#coding:utf-8
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def words_filter(words):
    stop_words_set = set() 
    with open('/home/yu/workspace/project/weibo-food-security-analysis/data/stopwords') as f:
        for word in f:
            stop_words_set.add(word.strip())
    filtered_words = []
    for word in words:
        word = word.replace('/','')
        if word.encode('utf-8') not in stop_words_set:
            filtered_words.append(word)
    return filtered_words


data_directory = os.path.abspath('../data')

with open(data_directory+'/train_data') as f:
    lines = [line.strip() for line in f.xreadlines()]

with open(data_directory+'/filter_train_data','w') as f:
    for line in lines:
        line = re.sub('[\s]*http:\/\/t\.cn\/[\da-zA-Z]+[\s]*','',line)
        words = line.split(' ')
        words = words_filter(words)   #去掉停词
        f.write(' '.join(words)+'\n')
