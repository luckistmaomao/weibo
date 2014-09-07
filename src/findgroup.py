
#coding:utf-8

import sys
from data_manager import DataBase,Timer,SingleWeibo,Comment,Retweet
from conf import HOST,DBNAME

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    try:
        db = DataBase(DBNAME,HOST)
    except Exception:
        print traceback.format_exc()
        print "Connection Error"

    comment_documents = db.comment_adv_documents
    retweet_documents = db.retweet_adv_documents


    user_set = set()
    for document in comment_documents:
        comment = Comment(document)
        #print '%s,%s,%s' % (comment.nickname,comment.ori_nickname,'comment')
        user_set.add(comment.uid)
        user_set.add(comment.ori_uid)

    for document in retweet_documents:
        retweet = Retweet(document)
        #print '%s,%s,%s' % (retweet.nickname,retweet.ori_nickname,'retweet')
        user_set.add(retweet.uid)
        user_set.add(retweet.ori_uid)
    
    for uid in user_set:
        print uid

if __name__ == "__main__":
    with Timer() as t:
        main()

