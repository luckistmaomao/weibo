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
    clarity = 0
    words = []
    for hit in hits:
        words.extend(hit['content'].split(' '))
    for word in set(words):
        p1 = words.count(word)*1.0/len(words)
        p2 = words.count(word)*1.0/len(all_words)
        tmp = p1 * math.log(p1/p2) 
        clarity += tmp
    return clarity

def main():
    train_data_filepath = '/home/yu/workspace/weibo-food-security-analysis/data/train_data.txt'
    with open(train_data_filepath) as f:
        lines = [line.strip() for line in f.readlines()]

    retweets = []
    all_words = []
    for line in lines:
        retweet = dict()
        sentiment,content = line.split('\t')
        retweet['sentiment'] = sentiment
        retweet['words'] = content.split(' ')
        retweets.append(retweet)
        words = retweet['words']
        all_words.extend(words)

#    analyzer = RegexAnalyzer(ur"([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")
    analyzer = ChineseAnalyzer()
    schema = Schema(label=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    for retweet in retweets:
        label = retweet['sentiment'].decode('utf-8')
        content = ' '.join(retweet['words']).decode('utf-8')
        writer.add_document(label=label,content=content)
    writer.commit()
    searcher = ix.searcher()

    with open('../data/test_data.txt') as f:
        test_lines = [line.strip() for line in f.readlines()]

#    results = searcher.find('content',u'可耻')
#    for result in results:
#        print result['content']
    
#    test_line_num = int(sys.argv[1])
#    for line_num,line in enumerate(test_lines[test_line_num-1:test_line_num]):
    for line_num,line in enumerate(test_lines[:]):
        words = line.split(' ')
        hits = []
        max_clarity = 0
        max_word = ''
        ranks = []
        for word in set(words):
            hits = search(word,searcher)
            if len(hits)>3:
                clarity = cal_clarity(hits,all_words)
            else:
                clarity = 1.0
    #        print clarity
            if max_clarity < clarity:
                max_clarity = clarity
                max_word = word
#            results = search(word,searcher)
#            labels = []
#            for result in results:
#                labels.append(result['label'])
#            rank = Counter(labels).items()
#            rank.sort(key= lambda x:x[1],reverse=True)
#            if rank:
#                ranks.append([word,clarity,rank[0][0],rank])
#            ranks.sort(reverse=True,key=lambda x:x[1])
#        for rank in ranks:
#            rank = [str(i) for i in rank]
#            print ' '.join(rank)

        results = search(max_word,searcher)
        labels = []
        for result in results:
            labels.append(result['label'])
        rank = Counter(labels).items()
        rank.sort(key= lambda x:x[1],reverse=True)
        if max_word=='保障':
            sentence = ''.join(words)
            negative_words = ['不','怎样','什么','怎么','怎','吗','呢','哎','？','?']
            flag = True
            for negative_word in negative_words:
                if negative_word in sentence:
                    print max_word,rank[0][0],rank
                    flag = False
                    break
            if flag:
                print max_word,'neutral'
        else:
            print max_word,rank[0][0],rank

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print 'running time:',end-start
