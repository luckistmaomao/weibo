#coding:utf8

import requests
from data_manager import Timer
import re
from BeautifulSoup import BeautifulSoup
import json


def is_valid_proxy1(ip,port):
    socket_address = "%s:%s" % (ip,port)
    verification_url = "http://proxies.site-digger.com/proxy-detect/"

    proxies = {}
    proxies['http'] = socket_address

    try:
        r = requests.get(verification_url, proxies=proxies,timeout=2)
    except :
#        print socket_address,'timeout'
        return False
    content = r.content
    
    if content.find('高匿')!=-1:
        return True
    else:
#        print socket_address,'failure'
        return False

def is_valid_proxy2(ip,port):
    verification_url = 'http://pachong.org/test.html'

    headers = {
            'Content-Type':'application/x-www-form-urlencoded'
            }

    payload = 'hosts=%s:%s' % (ip,port)
    try:
        r = requests.post(verification_url,headers = headers,data=payload,timeout=2)
        json_obejct = json.loads(r.content)
        proxy_type = json_obejct['data']['hosts'][0]['type']
        if proxy_type == 'HIGH':
            return True
        else:
            return False
    except:
        return False
   
def is_valid_proxy(ip,port):
    if is_valid_proxy1(ip,port) and is_valid_proxy2(ip,port):
        return True
    else:
        return False

def main():
    socket_list = []
#    url = 'http://proxy.com.ru/gaoni/'
#    r = requests.get(url)
#    content = BeautifulSoup(r.content)
#    pattern = re.compile('<tr><b></b><td>\d+</td><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>高度匿名</td><td>.+?</td></tr>')
#    socket_list += pattern.findall(str(content))

    url = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    tbody = soup.find('tbody')
    trs = tbody.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        socket_address = tds[0].text
        proxy_type = tds[1].text
        location = tds[2].text
        if proxy_type == 'Anonymous' and location == 'China':
            ip,port = socket_address.split(':')
            socket_list.append((ip,port))

    url = 'http://pachong.org/anonymous.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    tbody = soup.find('tbody')
    trs = tbody.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        ip = tds[1].text
        port = tds[2].text
        proxy_type = tds[4].a.text
        if proxy_type == 'high':
            socket_list.append((ip,port))

    for i in socket_list:
        ip = i[0]
        port = i[1]
        if is_valid_proxy(ip,port):
            print "%s:%s success" % (ip,port)
        
if __name__ == "__main__":
    main()
