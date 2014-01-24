# -*- coding: utf-8 -*- 
#coding:utf-8
# Get APP information from Google Play using Python
# Python 2.7 
# Author: KuangTien Wong
# Email: KuangTienWong@gmail.com
from pyquery import PyQuery as pq
from lxml import etree
import urllib
import urllib2
import csv
# Need the PyQuery package to conduct the jQuery-like manipulation of HTML
# package is the last part of Google Play's url,after 'id='
# I already got a list containing the package of many apps, so I write this code to get the detailed 
# information from Google Play
def spider(package):
    url='https://play.google.com/store/apps/details?id='+package
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Chrome/0.2.149.27')
    r  = urllib2.urlopen(req)  
    html = r.read()
    try:
        html=html.decode('utf-8')     
    except UnicodeDecodeError:
        html=html
    d=pq(html)  
    name=d('div').filter('.document-title').text()
    numDownloads=d('div').filter('.content').eq(2).text()
    score=d('div').filter('.score').text().replace(',','')
    starRating=d('div').filter('.rating-bar-container').text().replace(',','').split(' ')
    reviewsNum=d('span').filter('.reviews-num').text().replace(',','')
    primary=d('a').filter('.document-subtitle').eq(0).text()
    subCategory=d('a').filter('.document-subtitle').eq(1).attr('href').strip('/store/apps/category/')
    return {'name':name,'package':package,'num_downloads':numDownloads,'score':score,'star_rating_5':starRating[1],
            'star_rating_4':starRating[3],'star_rating3':starRating[5],'star_rating2':starRating[7],
            'star_rating_1':starRating[9],'reviews_num':reviewsNum,'developer':primary,
            'sub_category':subCategory
            }

f_read=file('package_name.csv','rb')
f_write=file('spider_output.csv','ab')
reader=csv.reader(f_read)
writer=csv.writer(f_write)
title=[u'name',u'package',u'developer',u'sub_category',u'num_downloads',u'score',u'star_rating_5',u'star_rating_4',u'star_rating_3',u'star_rating_2',u'star_rating_1',u'reviews_num']
writer.writerow([u'id',u'type']+title)
for line in reader:
    s=[]
    try:
        d=spider(line[2])
    except urllib2.HTTPError,e:
        d={u'package':line[2],u'sub_category':e.code}
        print e.code
    for x in title:
        s.append(d.get(x))
    writer.writerow([line[0],line[3]]+s)
f_read.close()
f_write.close()

