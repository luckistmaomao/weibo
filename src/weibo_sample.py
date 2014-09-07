#coding;utf-8


import sys
from data_manager import DataBase,Timer,SingleWeibo
from conf import HOST,DBNAME
import random

ALL = False

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    try:
        db = DataBase(DBNAME,HOST)
    except Exception:
        print traceback.format_exc()
        print "Connection Error"


    if ALL is True:
        single_weibo_documents = db.single_weibo_documents
    else:
        single_weibo_documents = random.sample(db.single_weibo_documents,1500)

    for document in single_weibo_documents:
        single_weibo = SingleWeibo(document)
        if single_weibo.original_content == '':
            single_weibo.original_content = ' '
        print '%s\t%s\t%s' % (single_weibo.nickname,single_weibo.content,single_weibo.original_content)

if __name__ == "__main__":
    main()
