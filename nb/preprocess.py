#coding:utf-8

import jieba
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

with open(os.path.pardir+'/data/stopwords.txt') as f:
    stopwords = [line.strip().decode('utf-8') for line in f.xreadlines()]
stopwords = set(stopwords)

def filter_stopwords(words):
    return filter(lambda x: x not in stopwords,words)

def main():
    train_data_file = os.path.pardir + '/data/sample.txt'
    result_file = os.path.pardir + '/data/result'
    with open(train_data_file) as f:
        content_lines = [line.strip() for line in f.xreadlines()]

    with open(result_file) as f:
        result_lines = [line.strip() for line in f.xreadlines()]

    weibo_objs = list()
    for content,label in zip(content_lines,result_lines):
        content = content.decode('utf-8')
        label = label.decode('utf-8')
        weibo_obj = {}
        words = list(jieba.cut(content))
        words = filter_stopwords(words)
        weibo_obj['content'] = content
        weibo_obj['label'] = label
        weibo_obj['words'] = words
        weibo_objs.append(weibo_obj)

    with open('weibo.txt','w') as f:
        for weibo_obj in weibo_objs:
            words = weibo_obj['words']
            label = weibo_obj['label']
            line = label +'\t'+' '.join(words)
            line = line.encode('utf-8')
            f.write(line+'\n')

if __name__ == "__main__":
    main()
