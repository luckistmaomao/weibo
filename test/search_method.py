#coding:utf-8

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
import sys
from whoosh.analysis import Tokenizer,Token
import time
import math
from collections import Counter
import os

from TextRank import textrank

reload(sys)
sys.setdefaultencoding('utf-8')

class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False, keeporiginal=False,removestops=True,start_pos=0, start_char=0, mode='',**kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value 
        t = Token(positions, chars, removestops=removestops, mode=mode,**kwargs)
        seglist = value.split(' ')
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos=start_pos+value.find(w)
            if chars:
                t.startchar=start_char+value.find(w)
                t.endchar=start_char+value.find(w)+len(w)
            yield t         

def ChineseAnalyzer():
    return ChineseTokenizer()

def search(word,searcher):
    word = word.decode('utf-8')
    results = searcher.find('content',word)
    return results

def cal_clarity(hits,all_words):
    clarity = 0.0
    words = []
    for hit in hits:
        words.extend(hit['content'].split(' '))

    words_length = len(words)
    all_words_length = len(all_words)
    words_counter = Counter(words)
    all_words_counter = Counter(all_words)
    for word in set(words):
        p1 = (words_counter[word]*1.0)/words_length
        p2 = (all_words_counter[word]*1.0)/all_words_length
        tmp = p1 * math.log(p1/p2) 
        clarity += tmp
#    print clarity
    return clarity

def get_topwords(words,limit):
   docs = []
   docs.append(words)
   rank = textrank.KeywordTextRank(docs)
   rank.solve()
   ret = []
   for word in rank.top_index(limit):
       ret.append(word)
   return ret


def test(train_data,test_data):
    accuracy = 0.0

    analyzer = ChineseAnalyzer()
    schema = Schema(label=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    all_words = []
    wrongs = []
    for label,train_line,ori_line in train_data:
        label = label.decode('utf-8')
        content = train_line.decode('utf-8')
        writer.add_document(label=label,content=content)
        all_words.extend(content.split(' '))

    writer.commit()
    searcher = ix.searcher()
    
    count = 0
    for label,test_line,ori_line in test_data:
        test_line = test_line.decode('utf-8')
        
        words = test_line.split(' ')
        results = []
        max_clarity = 0
        max_word = ''
        limit = 6
        topwords = get_topwords(words,limit)
        for word in set(topwords):
            hits = search(word,searcher)
            if len(hits)>=3:
                clarity = cal_clarity(hits,all_words)
            else:
                clarity = 1.0

            if max_clarity < clarity:
                max_clarity = clarity
                max_word = word
            
            if hits:
                results.append((word,clarity,hits))

        negative = 0.0
        positive = 0.0
        neutral = 0.0
        spam = 0.0
        for word,clarity,hits in results:
            hit_labels = []
            for hit in hits:
                hit_labels.append(hit['label'])
            rank = Counter(hit_labels).items()
            for i,j in rank:
                if i == 'negative':
                    negative += j*clarity
                elif i == 'positive':
                    positive += j*clarity
                elif i == 'neutral':
                    neutral += j*clarity
                else:
                    spam += j*clarity
#        print negative,neutral,positive,spam
        if positive == max(negative,positive,neutral,spam):
            predict_label = 'positive'
        elif negative == max(negative,positive,neutral,spam):
            predict_label = 'negative'
        elif neutral == max(negative,positive,neutral,spam):
            predict_label = 'neutral'
        else:
            predict_label = 'spam'
        
        negative_words = ['?','？','哎']
        for negative_word in negative_words:
            if negative_word in ori_line:
                predict_label = 'negative'
                break

        if label == predict_label:
            count += 1
        else:
            print label,predict_label
            print test_line
            print ori_line
            wrongs.append((label,predict_label))

            
#        results = search(max_word,searcher)
#        labels = []
#        for result in results:
#            labels.append(result['label'])
#        rank = Counter(labels).items()
#        rank.sort(key= lambda x:x[1],reverse=True)
#        if label == rank[0][0]:
#            count += 1
#        else:
#            print max_word,label,rank,test_line

#    for i,j in Counter(wrongs).items():
#        print i[0],i[1],j
    accuracy = count*1.0/len(test_data)
    return accuracy

def main():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    data_directory = os.path.abspath('../data')
    with open(data_directory+'/train_data.txt') as f:
        lines = [line.strip() for line in f.xreadlines()]
    
    with open(data_directory+'/sample.txt') as f:
        ori_lines = [line.strip() for line in f.xreadlines()]

    with open(data_directory+'/result') as f:
        label_lines = [line.strip() for line in f.xreadlines()] 

    slice_num = 5
    for i in range(slice_num):
        train_lines = []
        test_lines = []
        test_labels = []
        train_labels = []
        test_ori_lines = []
        train_ori_lines = []
        
        line_num = len(lines)
        step = line_num / slice_num
        for j in range(slice_num):
            if i==j:
                test_lines.extend(lines[j*step:(j+1)*step])
                test_labels.extend(label_lines[j*step:(j+1)*step])
                test_ori_lines.extend(ori_lines[j*step:(j+1)*step])
            else:
                train_lines.extend(lines[j*step:(j+1)*step])
                train_labels.extend(label_lines[j*step:(j+1)*step])
                train_ori_lines.extend(ori_lines[j*step:(j+1)*step])
        
        train_data = zip(train_labels,train_lines,train_ori_lines)
        test_data = zip(test_labels,test_lines,test_ori_lines)
        accuracy = test(train_data,test_data) * 100
        print "Test case %s accuracy is %s%%" % (i+1,accuracy)
            

if __name__ == "__main__":
    main()
