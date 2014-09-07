#coding:utf-8
"""
    @anthor:yzt
"""

import traceback
import pymongo
import time
import datetime
import sys
from data_manager import Timer,DataBase,SingleWeibo
from conf import HOST,DBNAME

reload(sys)
sys.setdefaultencoding('utf-8')

start_date = datetime.datetime(2014,6,1)

class NdayData(object):
    def __init__(self):
        self.count = 0
        self.at = 0
        self.RT = 0
        self.comment = 0

def time_process(create_time_string):
    """
       convert string to datetime type 
    """
    time_format = '%Y-%m-%d %h:%m:%s'
    create_time_string = create_time_string
    struct_time = time.strptime(create_time_string,time_format)
    day_time = datetime.datetime(*struct_time[:3])
    return day_time

def cmp(a,b):
    if a['create_time'] > b['create_time']:
        return 1
    else:
        return -1

def get_datetime_str(day_time):
    year = day_time.year
    month = day_time.month
    day = day_time.day
    time_str = "%s-%s-%s" % (year,month,day)
    return time_str

def counting(documents, interval=6):
    ndaydata_list = []
    documents.sort(cmp)
    for document in documents:
        single_weibo = SingleWeibo(document)
        create_time = single_weibo.create_time
        delta_days = (create_time - start_date).days
        if delta_days < 0:                  ###过滤掉数据中包含的4月5日的数据
            continue
        index = delta_days / interval
        if (index+1) == len(ndaydata_list):
            ndaydata_list[index].count += 1
            ndaydata_list[index].RT += single_weibo.n_forward
            ndaydata_list[index].comment += single_weibo.n_comment
            content = single_weibo.content
            ndaydata_list[index].at += content.count('@')
        else:
            ndaydata_list.append(NdayData())
            ndaydata_list[index].count += 1
            ndaydata_list[index].RT += single_weibo.n_forward
            ndaydata_list[index].comment += single_weibo.n_comment
            content = single_weibo.content
            ndaydata_list[index].at += content.count('@')

    j = 0
    for ndaydata in ndaydata_list:
        start_time = start_date + datetime.timedelta(j*interval)
        end_time = start_date + datetime.timedelta(j*interval+interval-1)
        start_time_str = get_datetime_str(start_time)
        end_time_str = get_datetime_str(end_time)
        j = j + 1

        #print "%s to %s" % (start_time_str,end_time_str)
        #print 'count:',ndaydata.count
        #print '@:',ndaydata.at
        #print 'RT:',ndaydata.RT
        #print 'comment:',ndaydata.comment,'\n'

        if interval == 1:
            print '%s,%s,%s,%s,%s' % (start_time_str,ndaydata.count,ndaydata.at,ndaydata.RT,ndaydata.comment)
        else:
            print '%s to %s,%s,%s,%s,%s' % (start_time_str,end_time_str,ndaydata.count,ndaydata.at,ndaydata.RT,ndaydata.comment)
    
def main():
    try:
        db = DataBase(DBNAME,HOST)
    except Exception:
        print traceback.format_exc()
        print "Connection Error"
       
    single_weibo_documents = db.single_weibo_documents
    results = counting(single_weibo_documents,interval=1)

if __name__ == "__main__":
    with Timer() as t:
        main()
    print "运行时间:",t.interval 
