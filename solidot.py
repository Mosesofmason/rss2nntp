# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 01:30:36 2017

"""

import feedparser
import os
import time
import base64
from nntplib import *

rss_url = r'http://www.solidot.org/index.rss'
newsgroup = r'cn.test'
sender = r'Mobot <mobot@fakemail.com>'
org = r'Illuminati'
xface = "]c\"B8MZeR}>9;^p0Wtq#Vgi)J%R->C'u9b\"d#9b?4_HclroWBGm\"<c9g|w>9X\"P#NsWdp\'mOM*N:Sw0gkI@`^|6FYsd7bs\"S0u8:<u!l+9`,%f4z3lX80n1P0cX6q;O7Vmy<;iyx5EStx,9rzjcl$tO[a"

directory = "./outdir/"
ext = ".eml"

feeds = feedparser.parse(rss_url)

# 获得rss版本
print(feeds.version)
# 获得Http头
print(feeds.headers)
print(feeds.headers.get('content-type'))
# rss的标题
print(feeds['feed']['title'])
# 链接
print(feeds['feed']['link'])
# 子标题
print(feeds.feed.subtitle)
# 查看文章数量
print(len(feeds['entries']))


if not os.path.exists(directory):
    os.makedirs(directory)

filelist = [ f for f in os.listdir(directory) if f.endswith(ext) ]
for f in filelist:
    os.remove(f)


for feed in feeds.entries:
    itemtitle = feed["title"].encode('utf-8')
    print itemtitle
    itemsumary = feed["summary"].encode('utf-8')
    print itemsumary
    itemlink = feed["link"].encode('utf-8')
    print itemlink
    itemdate = feed["date"].encode('utf-8')
    print itemdate
    itemparsedate = feed["date_parsed"]
    print itemparsedate #time.struct_time

    pubyday = str(itemparsedate.tm_yday) # 1 - 366
    pubhour = str(itemparsedate.tm_hour)
    pubmin = str(itemparsedate.tm_min)
    pubsec = str(itemparsedate.tm_sec)
    
    with open(directory + pubyday + pubhour + pubmin + pubsec + '.eml', 'wb+') as f1:
        #header
        f1.write('Newsgroups: ' + newsgroup + os.linesep)
        f1.write('From: ' + sender + os.linesep)
        f1.write('Orgnization: ' + org + os.linesep)
        f1.write('X-Face: ' + xface + os.linesep)  
        #=?charset?encoding?encoded-text?=
        b64subj = base64.b64encode(itemtitle)
        f1.write('Subject: =?utf-8?B?' + b64subj + '?=' + os.linesep)
        f1.write('Content-Type: text/plain; charset=utf-8' + os.linesep)
        #f1.write('Content-Transfer-Encoding: 8bit' + os.linesep)
        f1.write('Content-Transfer-Encoding: base64' + os.linesep)
        f1.write(os.linesep)
        f1.write(os.linesep)
        #body     
        body = itemtitle + os.linesep \
                                    + itemlink  + os.linesep \
                                    + os.linesep \
                                    + itemsumary + os.linesep \
                                    + os.linesep \
                                    + itemdate + os.linesep \
                                    + os.linesep \
                                    + '--' + os.linesep \
                                    + 'Mobot' + os.linesep \
                                    + os.linesep
        print body
        b64body = base64.b64encode(body)
        f1.write(b64body)
        
        
        '''f1.write(itemtitle + os.linesep)
        f1.write(itemlink  + os.linesep)
        f1.write(os.linesep)
        f1.write(itemsumary  + os.linesep)
        f1.write(os.linesep)
        f1.write(itemdate + os.linesep)        
        f1.write(os.linesep)
        f1.write('--' + os.linesep)
        f1.write('Mobot' + os.linesep)
        f1.write(os.linesep)'''
    f1.close ()
        

print ('parse completed.')

try:
    ns = NNTP ('nntp.aioe.org')
    #ns = NNTP_SSL ('news.mixmin.net')
    ns.set_debuglevel(1)
    
    n=0
    
    for file in os.listdir(directory):
        if file.endswith(ext):          
            try:
                print(os.path.join(os.linesep + directory, file) + os.linesep)
                f = open(os.path.join(directory, file))
                if n<10:
                    time.sleep(2*n)
                else:
                    time.sleep(600)
                ns.post(f) 
                print(os.path.join(directory, file) + os.linesep)
                f = open(os.path.join(directory, file))
                ns.post(f) 
                f.close()
                n = n+1
                os.remove (os.path.join(directory, file))
            except NNTPTemporaryError:
                print ('duplicated article')               
                f.close()     
                os.remove (os.path.join(directory, file))
                continue

finally:
    # Close the usenet connection.
    response = ns.quit()
    # Print the response.
    print(response)