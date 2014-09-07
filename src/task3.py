#coding:utf-8

from data_manager import Timer,DataBase
from networkx import MultiDiGraph
from data_manager import Timer,DataBase,SingleWeibo,WeiboComment
from numpy import average,std
from collections import Counter
import traceback
import pickle
import os

class WeiboGraph(MultiDiGraph):
    def __init__(self):
        super(WeiboGraph,self).__init__()

    def get_top_10percent_users(self):
        degrees = self.in_degree()
        sorted_degrees = sorted(degrees.items(), key=lambda x:x[1], reverse=True)
        top_10percent_users = [degree[0] for degree in sorted_degrees[:len(sorted_degrees)/10] ]
        return top_10percent_users

    def get_top100_users(self):
        degrees = self.in_degree()
        sorted_degrees = sorted(degrees.items(), key=lambda x:x[1], reverse=True)
        top100_users = [degree[0] for degree in  sorted_degrees[:100]]
        return top100_users

    def ten_to_ten(self):
        tmp = []
        top_10percent_users = self.get_top_10percent_users()
        top_10percent_users_set = set(top_10percent_users)
        edges = self.edges() 
        for edge in edges:
            if edge[0] in top_10percent_users_set and edge[1] in top_10percent_users_set:
               tmp.append(edge[1]) 
         
        tmp = Counter(tmp)
        mean = average(tmp.values())
        SD = std(tmp.values())
        return mean,SD

    def ten_to_ninety(self):
        tmp = []
        top_10percent_users = self.get_top_10percent_users()
        top_10percent_users_set = set(top_10percent_users)
        edges = self.edges() 
        for edge in edges:
            if edge[0] not in top_10percent_users_set and edge[1] in top_10percent_users_set:
                tmp.append(edge[1])

        tmp = Counter(tmp) 
        mean = average(tmp.values())
        SD = std(tmp.values())
        return mean,SD

    def get_100_prominent_users_addressivity_marker_from_top_10percent(self):
        top_10percent_users_set = set(self.get_top_10percent_users())
        top100_users_set = set(self.get_top100_users())
        edges = set(self.edges()) #去掉多重边
        result_list = []
        for edge in edges:
            if edge[0] in top100_users_set and edge[1] in top100_users_set:
                result_list.append(edge)
            if edge[0] in top100_users_set and edge[1] in top_10percent_users_set:
                result_list.append(edge)
            if edge[0] in top_10percent_users_set and edge[1] in top100_users_set:
                result_list.append(edge)
        return result_list


class RTGraph(WeiboGraph):
    def __init__(self,db):
        super(RTGraph,self).__init__()
        self.db = db
        self.init_edges()
        self.graph_type = "RT"

    def init_edges(self):
        documents = self.db.single_weibo_documents
        for document in documents:
            single_weibo = SingleWeibo(document)
            if single_weibo.is_forward:
                uid = single_weibo.uid
                forward_uid = single_weibo.forward_uid
                self.add_edge(uid,forward_uid)

    def get_top_user(self):
        degrees = self.in_degree()
        n_top_rt = 0
        top_user_id = ''
        for uid,count in degrees.items():
            if count > n_top_rt:
                n_top_rt = count
                top_user_id = uid
        return top_user_id,n_top_rt


class AtGraph(WeiboGraph):
    def __init__(self,db):
        super(MultiDiGraph,self).__init__()
        self.db = db
        self.init_edges()
        self.graph_type = "at"

    def init_edges(self):
        documents = self.db.single_weibo_documents
        for document in documents:
            single_weibo = SingleWeibo(document)
            if single_weibo.n_at > 0:
                uid = single_weibo.uid
                at_usernames = single_weibo.at_usernames
                for username in at_usernames:
                    self.add_edge(uid,username)

    def get_top_user(self):
        degrees = self.in_degree()
        n_top_at = 0
        top_username = ''
        for username,count in degrees.items():
            if count > n_top_at:
                n_top_at = count
                top_username = username
        return top_username,n_top_at


class CommentGraph(MultiDiGraph):
    def __init__(self,db):
        super(MultiDiGraph,self).__init__()
        self.db = db
        self.init_edges()
        self.graph_type = "comment"

    def init_edges(self):
        filepath = '../data/comment_pairs.pickle'
        if os.path.exists(filepath):
            with open(filepath) as f:
                comment_pairs = pickle.load(f)
        else:
            comment_pairs = self.db.get_comment_pairs()

        self.add_edges_from(comment_pairs)

    def get_top_user(self):
        pass


def main():
    try:
        db = DataBase() 
    except Exception:
        print traceback.format_exc()
        print "Connection Eorror"


    rt_graph = RTGraph(db)
    rt_graph.get_top_user()
    rt_graph.get_top_10percent_users()
    #print rt_graph.ten_to_ten()
    #print rt_graph.ten_to_ninety()
    #rt_graph.get_100_prominent_users_addressivity_marker_from_top_10percent()

    at_graph = AtGraph(db)
    at_graph.get_top_user()
    at_graph.get_top_10percent_users()
    #print at_graph.ten_to_ten()
    #print at_graph.ten_to_ninety()

    comment_graph = CommentGraph(db)

    weibo_graph = WeiboGraph()
    weibo_graph.add_edges_from(rt_graph.edges())
    #weibo_graph.add_edges_from(at_graph.edges())   #需先爬取被@用户的uid
    weibo_graph.add_edges_from(comment_graph.edges())
    weibo_graph.get_100_prominent_users_addressivity_marker_from_top_10percent()

if __name__ == "__main__":
    with Timer() as t:
        main()
    print t.interval
