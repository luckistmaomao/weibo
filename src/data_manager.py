#coding:utf-8

import pymongo
import time
import re
import pickle
import os

class DataBase(object):
    """
        mongodb connection and information retrieval
    """
    def __init__(self,dbname='',host='localhost',port=27017):
        self.client = pymongo.MongoClient(host,port)
        
        self.db = self.client[dbname]
        self.single_weibo_documents = list(self.db.single_weibo.find())
        self.comment_adv_documents = list(self.db.comment_adv.find())
        self.retweet_adv_documents = list(self.db.retweet_adv.find())

    def close(self):
        self.client.close()

    def get_comment_pairs(self):
        comment_pairs = []
        for i in self.single_weibo_documents:
            mid = i['mid']
            uid = i['uid']
            a = self.comment_adv_collection_5.find({'attached_mid':mid})
            b = self.comment_adv_collection_6.find({'attached_mid':mid})
            for j in a:
                comment_pairs.append((j['uid'],uid))
            for j in b:
                comment_pairs.append((j['uid'],uid)) 
        with open('../data/comment_pairs.pickle','w') as f:
            pickle.dump(comment_pairs,f)
        return comment_pairs

    def get_comment_pairs_1(self):
        comment_pairs = []
        for i in self.comment_adv_collection_5.find():
            mid = i['attached_mid']
            uid = i['uid']
            a = self.single_weibo_collection_5.find_one({'mid':mid})
            if a:
                comment_pairs.append((uid,a['uid']))
            else:
                b = self.single_weibo_collection_6.find_one({'mid':mid})
                if b:
                    comment_pairs.append((uid,b['uid']))
        for i in self.comment_adv_collection_6.find():
            mid = i['attached_mid']
            uid = i['uid']
            a = self.single_weibo_collection_5.find_one({'mid':mid})
            if a:
                comment_pairs.append((uid,a['uid']))
            else:
                b = self.single_weibo_collection_6.find_one({'mid':mid})
                if b:
                    comment_pairs.append((uid,b['uid']))
        print len(comment_pairs)



class SingleWeibo(object):
    """
        store wiebo related information
    """
    def __init__(self,document):
        self.mid = document['mid']
        self.uid = document['uid']
        self.content = document['content'].strip()
        self.n_forward = document['n_forward']
        self.n_comment = document['n_comment']
        self.create_time = document['create_time']
        self.is_forward = document['is_forward']
        self.original_content = document['original_cntnt'].strip()
        self.forward_uid = document['forward_uid']
        self.url = document['url']
        self.nickname = document['nickname']
        self.n_at = self.at_count(self.content)
        self.at_usernames = self.get_at_users(self.content)
        self.hashtags = self.get_hashtags()

    def at_count(self,content):
        return content.count('@')

    def get_at_users(self,content):
        uesrname_pattern = re.compile(u"@([a-zA-Z\u4e00-\u9fa5\-\_]+)\s")
        usernames = uesrname_pattern.findall(content)
        return usernames

    def get_hashtags(self):
        hashtag_pattern = re.compile('#(.+?)#')
        hashtags = hashtag_pattern.findall(self.content)
        return hashtags

class Comment(object):
    """
        store weibo comment related information
    """
    def __init__(self,document):
        self.cid = document['cid']
        self.attached_mid = document['attached_mid']
        self.nickname = document['nickname']
        self.uid = document['uid']
        self.content = document['content']
        self.create_time = document['create_time']
        self.ori_uid = document['ori_uid']
        self.ori_nickname = document['ori_nickname']

class Retweet(object):
    def __init__(self,document):
        self.rid = document['rid']
        self.attached_mid = document['attached_mid']
        self.nickname = document['nickname']
        self.uid = document['uid']
        self.content = document['content']
        self.create_time = document['create_time']
        self.ori_uid = document['ori_uid']
        self.ori_nickname = document['ori_nickname']


class Timer():
    """
        Calculate how long this program takes.
    """
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self,*args):
        self.end = time.time()
        self.interval = self.end - self.start


#just for test
def main():
    db = DataBase()
    #db.get_comment_pairs()

if __name__ == "__main__":
    with Timer() as t:
        main()
    print t.interval
