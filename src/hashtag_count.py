#coding:utf-8

import traceback
from data_manager import Timer,SingleWeibo,DataBase
from conf import HOST,DBNAME
import sys

from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    try:
        db = DataBase(DBNAME,HOST)
    except:
        print "mongo connection error"

    single_weibo_documents = db.single_weibo_documents
    hashtags = list()
    
    for single_weibo_document in single_weibo_documents:
        single_weibo = SingleWeibo(single_weibo_document)
        hashtags.extend(single_weibo.hashtags)
    
    result = Counter(hashtags)

    for i,j in sorted(result.items(),key = lambda x:x[1],reverse=True)[:31]:
        print i,j


if __name__ == "__main__":
    main()
