#coding:utf-8

import pymongo
import sys
from data_manager import DataBase,SingleWeibo,Timer
import re
import requests
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

class SavedLinks(object):
    def __init__(self):
        self.url_dict = dict()
        self.short_url_set = set()
        self.original_url_set = set()
        with open("../data/c_links") as f:
            for line in f:
                links = line.strip().split(' ')
                short_url = links[0]
                original_url = links[1]
                self.url_dict[short_url] = original_url
                self.short_url_set.add(short_url)
                self.original_url_set.add(original_url)


def trim_data(documents):
    data_info = {}
    saved_links= SavedLinks()
    lines = []
    for document in documents:
        single_weibo = SingleWeibo(document)
        content = single_weibo.content

        data_info['date'] = single_weibo.create_time
        data_info['body_text'] = content

        uesrname_pattern = re.compile(u"@([a-zA-Z\u4e00-\u9fa5\-\_]+)\s")
        data_info['at_username'] = uesrname_pattern.findall(content)
        #for i in data_info['at_username']:
        #    print i
        data_info['is_forward'] = single_weibo.is_forward
        data_info['original_userid'] = single_weibo.forward_uid
        data_info['n_comment'] = single_weibo.n_comment
        data_info['n_forward'] = single_weibo.n_forward

        link_pattern = re.compile("http:\/\/t\.cn\/[\da-zA-Z]+")
        links = link_pattern.findall(content)
        original_urls = []
        for link in links:
            try:
                original_url = saved_links.url_dict[link]
            except KeyError:
                r = requests.get(url, allow_redirects=False)
                original_url = r.headers['location']
            original_urls.append(original_url)
        data_info['hyperlink'] = original_urls

        hashtag_pattern = re.compile("#(.+?)#")
        hashtags = hashtag_pattern.findall(content)
        data_info["hashtag"] = hashtags
        line = pretty_print_data_info(data_info)
        lines.append(line)
    with open('../data/2.txt','w') as f:
        for line in lines:
            f.write(line+'\n')

def get_datetime_str(day_time):
    year = day_time.year
    month = day_time.month
    day = day_time.day
    time_str = "%s-%s-%s" % (year,month,day)
    return time_str

def pretty_print_data_info(data_info):
    date_str = get_datetime_str(data_info['date'])
    body_text = data_info['body_text'].replace('\n','')
    at_usernames = data_info['at_username']
    if at_usernames:
        at_usernames_str = ','.join(at_usernames)
    else:
        at_usernames_str = 'None'

    is_forward = data_info['is_forward']
    if is_forward:
        original_userid = data_info['original_userid']
    else:
        original_userid = 'None'
    
    links = data_info['hyperlink']
    if links:
        links_str = ','.join(links)
        has_hyperlink = True
    else:
        links_str = 'None'
        has_hyperlink = False
    
    hashtags = data_info['hashtag']
    if hashtags:
        hashtags_str = ','.join(hashtags)
    else:
        hashtags_str = 'None'
    n_comment = data_info['n_comment']
    n_forward = data_info['n_forward']
    line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % \
            (date_str,body_text,at_usernames_str,is_forward,original_userid,has_hyperlink,links_str,hashtags_str,n_comment,n_forward)
    return line





#def find_original_url(url):
#    with open("../data/c_links") as f:
#        for line in f:
#            links = line.strip().split(' ')
#            short_url = links[0]
#            original_url = links[1]
#            if url == short_url:
#                return original_url
#    print "error"
#    r = requests.get(url,allow_redirects=False)
#    return r.headers['location']
        
def main():
    #client = pymongo.MongoClient(host)
    #db_5 = client['sinaweibosearch_shipinanquan']
    #db_6 = client['sinaweibosearch_shipinanquan_6']
    #collection_5 = db_5['single_weibo']
    #collection_6 = db_6['single_weibo']
    #documents = list(collection_5.find()) + list(collection_6.find())  
    #client.close()

    db = DataBase()
    #print "DataBase Done"
    single_weibo_documents = db.single_weibo_documents
    trim_data(single_weibo_documents)

if __name__ == "__main__":
    with Timer() as t:
        main()
    #print t.interval
