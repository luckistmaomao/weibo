#coding:utf-8
"""
date:2014.8.4
author:yuzt
"""

from data_manager import DataBase,Timer
import datetime
import random
import time
import pickle
import traceback
import numba

def convert_datetime_to_date(t):
    year = t.year
    month = t.month
    day = t.day
    return datetime.date(year,month,day)

def count_sample_user_documents(daily_sample_num,documents):
    at_count = 0
    RT_count = 0
    comment_count = 0

    for document in documents:
        at_count += document['content'].count('@')
        RT_count += document['n_forward']
        comment_count += document['n_comment']

    print daily_sample_num,at_count,RT_count,comment_count

"""
try to sample 300 weibos every day from 2014.6.2 to 2014.8.3,totally 9 weeks,
then store data in mongodb
"""

def data_sample(documents,daily_sample_num):
    #random.seed(time.time())

    start_date = datetime.date(2014,6,2)
    user_clustering_by_date = {}
    
    for date_delta in range(63):
        user_clustering_by_date[start_date+datetime.timedelta(date_delta)] = []
    
    date_set = set(user_clustering_by_date.keys())
    
    #get vaild document 
    for document in documents:
        create_time = document['create_time']
        create_date = convert_datetime_to_date(create_time)
        if create_date in date_set:
            user_clustering_by_date[create_date].append(document)

    sample_user_documents = []
    for date,documents in user_clustering_by_date.items():
        if len(documents) < daily_sample_num:
            sample_user_documents.extend(documents)
        else:
            sample_documents = random.sample(documents,daily_sample_num) 
            sample_user_documents.extend(sample_documents)

    count_sample_user_documents(daily_sample_num,sample_user_documents)

        
if __name__ == "__main__":
    with Timer() as t:
        try:
            db = DataBase()
        except:
            print traceback.format_exc()
        documents = db.single_weibo_documents
        
        sample_list = [30,50,100,150,200,250,300]
        for i in sample_list: 
            for j in range(100):
                data_sample(documents,i)
    print t.interval


