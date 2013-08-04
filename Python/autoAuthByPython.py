#!/usr/bin/python2.7
# coding: utf-8

import urllib,urllib2,cookielib

# 确定cookie存放位置
cookiefile ="./cookies.txt"
# 获得cookie实例
cookies = cookielib.MozillaCookieJar(cookiefile)
# 查看是否有之前保存的cookie
try:
	cookies.load(ignore_discard=True, ignore_expires=True)
except Exception:
	cookies.save(cookiefile,ignore_discard=True, ignore_expires=True)

# 将cookie带入open中
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
urllib2.install_opener(opener)

#  通过认证页面认证
url = "http://was01.example.edu.cn/amserver/UI/Login"
auth = {'IDToken1':'username','IDToken2':'password'}
data = urllib.urlencode(auth)
# 设置浏览器头
headers = {'User-Agent' : 'Mozilla/5.0'}
req = urllib2.Request(url,data,headers)
response = opener.open(req)
# 保存cookie
if cookies is None:
    print "We don't have a cookie library available - sorry."
    print "I can't show you any cookies."
else:
    print 'These are the cookies we have received so far :'
    for index, cookie in enumerate(cookies):
		# 打印出具体的cookie
        print index, '  :  ', cookie
    cookies.save(cookiefile) 

# 打开欲访问的页面
urlWant = 'http://pay.example.edu.cn/index/navigate.html'
openHtml = opener.open(urlWant)
print openHtml.read()
