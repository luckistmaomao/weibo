#coding:utf-8

import sys
from data_manager import DataBase,Timer,SingleWeibo
from conf import HOST,DBNAME

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    try:
        db = DataBase(DBNAME,HOST)
    except Exception:
        print traceback.format_exc()
        print "Connection Error"

    single_weibo_documents = db.single_weibo_documents
    user_set = set()
    for single_weibo_document in single_weibo_documents:
        single_weibo = SingleWeibo(single_weibo_document)
        user_set.add(single_weibo.nickname)
        at_usernames = single_weibo.at_usernames
        for username in at_usernames:
            user_set.add(username)

    #print len(user_set)
    at = {}
    for user in user_set:
        at[user] = 0

    for single_weibo_document in single_weibo_documents:
        single_weibo = SingleWeibo(single_weibo_document)
        for username in single_weibo.at_usernames:
            at[username] += 1

    for nickname,count in sorted(at.items(),key = lambda x:x[1],reverse=True)[:100]:
        print nickname,count


if __name__ == "__main__":
    with Timer() as t:
        main()
    print "time:",t.interval
