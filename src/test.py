#coding:utf-8

import sys
from data_manager import DataBase,Timer,SingleWeibo
from conf import HOST,DBNAME
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    try:
        db = DataBase(DBNAME,HOST)
    except Exception:
        print traceback.format_exc()
        print "Connection Error"

    single_weibo_documents = db.single_weibo_documents
    count = 0
    content_set = set()
    content_list = list()
    for document in single_weibo_documents:
        if document['forward_uid']:
            count+=1
            content_set.add(document['original_cntnt'])
            content_list.append(document['original_cntnt'])
    print count
    print len(single_weibo_documents)
    print len(content_set)
    items = Counter(content_list).items()
    items.sort(key=lambda x:x[1],reverse=True)
    item_count = 0
    for i,j in items[:200]:
        item_count += j
    print item_count


if __name__ == "__main__":
    main()
