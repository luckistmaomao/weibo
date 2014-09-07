#coding:utf-8

import requests
import time
apikey = 'K2e0p6n4LzebaraDOwmEjHNNpQleWsKg6E2Q1Gjy'

with open('sample.txt') as f:
    lines = [ line.strip() for line in f.readlines() ] 

with open('train_data','a') as f:
    for line in lines[:]:
        line = line.replace('#','$')
        url = 'http://api.ltp-cloud.com/analysis/?api_key=%s&text=%s&pattern=ws&format=plain' % (apikey,line)
        r = requests.get(url)
        words = []
        for sentence in r.content.split('\n'):
            words.extend(sentence.split(' '))
        time.sleep(0.3)
        f.write(' '.join(words)+'\n')
