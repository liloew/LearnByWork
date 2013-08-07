#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import json
from threading import Thread
from sys import exit
import time

import db

class GetPages(Thread):

	def __init__(self,url=None,timeout=10):

		Thread.__init__(self)
		if not url:
			return None
		else:
			self.url = url
		# Initializing
		#super(GetPages,self).__init__(url,timeout)
		self.timeout = timeout
		# Get the name of googs.
		self.namere  = re.compile('<h1>.+</h1>')
		#self.linkre	 = patern = re.compile('<li>*?href=')
		self.goodsid = url.split('com/')[1].split('.html')[0]
		self.mysql   = db.mysql(hostname='192.168.88.129',passwd='lilo',user='lilo',db='test')

	def buildUserAgent(self,url=None,to=10):

		if url == None:
			print "Must special an url"
			eixt(-1)
		#opener = urllib2.build_opener()
		request = urllib2.Request(url)
		request.add_header('User-Agent',
			'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0')
		return urllib2.urlopen(request,timeout=to).read()


	def getProductUrl(self,wid=None):
		'''Refer `http://simigoods.jd.com/js/BiForWeb.B.js?t=20110804`
		But modified by me.
		'''
		if not wid:
			print 'Finished'
			exit(0)
		if wid > 10000000 & wid < 20000000:
			return 'http://book.jd.com/' + wid + '.html'
		elif wid > 20000000 & wid < 30000000:
			return 'http://mvd.jd.com/' + wid + '.html'
		else:
			return 'http://item.jd.com/' + wid + '.html'

	#def run(self,url=self.url,namere=self.namere,timeout=self.timeout,goodsid=self.goodsid):
	def run(self):

		time.sleep(10)
		html  = urllib2.urlopen(self.url,timeout=self.timeout).read()
		# Get the name of the goods
		name  = re.findall(self.namere,html)
		# Get the price of goods.
		price = urllib2.urlopen('http://p.3.cn/prices/get?skuid=J_'
				+ self.goodsid,
				#.append(self.goodsid),
				timeout=self.timeout).read()
		jsprice = json.loads(price)
		# Get the related goods
		thisurl = ''.join(('http://simigoods.jd.com/Book/GetInterimBookJsonData.aspx?ip='
				# Repalce `北京` because threading didn't recognize utf-8
				,'%E5%8C%97%E4%BA%AC'
				,'&callback=BuyBuyBooksJsonDataRec&wids='
				,self.goodsid))
		relat = urllib2.urlopen(thisurl,timeout=self.timeout).read()
		relat = relat.lstrip('BuyBuyBooksJsonDataRec(').rstrip(')')
		js	  = json.loads(relat, encoding='gbk')
		#title = name[0].decode('gbk').lstrip('<h1>').split('<span>')[0],jsprice[0]['p']
		title = name[0].decode('gbk').lstrip('<h1>').split('<span>')[0]
		#print relat
		#print js[0]['Name'],js[0]['Wmeprice']
		#print js[2]['Name'],js[2]['Wmeprice']
		have  = self.mysql.select(tb='jd',id=jsprice[0]['id'].lstrip('J_'))
		if have == 0:
			self.mysql.insert('jd',jsprice[0]['id'].lstrip('J_'),
					goods=title,price=jsprice[0]['p'])
		for x in js:
			#print x['Wid'],x['Name'],x['Wmeprice']
			# insert in threading calling
			have = self.mysql.select(tb='jd',id=x['Wid'])
			if have == 0:
				self.mysql.insert('jd',x['Wid'],goods=x['Name'],
						price=x['Wmeprice'])
			thre = GetPages(url='http://book.jd.com/'+x['Wid']+'.html')
			#thre.run()
			thre.start()


if __name__ == '__main__':
	#book = GetPages(url='http://book.jd.com/11220393.html')
	book = GetPages(url='http://book.jd.com/11116710.html')
	#book.start()
	#book.run()
	book.start()
