#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
import sys, re, csv
import os
import codecs

encoding = 'UTF-8'
def convert(dir='.'):
	for dir, names, files in os.walk(dir):
		for file in files:
			if os.path.splitext(file)[1] == '.log':
				filename = os.path.splitext(file)[0]
				csvFile = open(filename + '.csv', 'wb')
				writer = csv.writer(csvFile, dialect='excel')
	
				with codecs.open(file, mode='rt', encoding=encoding) as f:
					while True:
					# 按行读文件，读至文件尾时退出循环
						NOW = f.readline()
						if not NOW:
							break
	
						else:
							patternHost = re.compile(u'\u4E3B\u673A\u901A\u77E5')
							patternService = re.compile(u'\u670d\u52a1\u901a\u77e5')
							# 经实验该处不可用match
							T1 =  patternHost.search(NOW)
							T2 = patternService.search(NOW)
							#if patternHost.search(NOW):	# 如果匹配成功，表明该段告警是主机告警
							if T1:	# 如果匹配成功，表明该段告警是主机告警
								#pass
								LISTS = []
								NOW = f.readline()
								NOW = f.readline()
								notify = NOW.split('Notification Type: ')[1]
								LISTS.append(notify.split('\n')[0])
								NOW = f.readline()
								host = NOW.split('Host: ')[1]
								#LISTS.append(host.split('\n')[0])
								LISTS.append(host.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								state = NOW.split('State: ')[1]
								LISTS.append(state.split('\n')[0])
								NOW = f.readline()
								addr = NOW.split('Address: ')[1]
								LISTS.append(addr.split('\n')[0])
								NOW = f.readline()
								info = NOW.split('Info: ')[1]							# 建议可去掉两侧英文括号
								#info = NOW.split('Info: ')[1].lstrip('(').rstrip(')')	# 建议可去掉两侧英文括号
								LISTS.append(info.split('\n')[0])
								#LISTS.append(info.split('(')[1].split(')')[0])
								NOW = f.readline()
								NOW = f.readline()
								time = NOW.split('Date/Time: ')[1]
								LISTS.append(time.split('\n')[0])
					
								writer.writerow(LISTS)
							elif T2:# 如果匹配成功，表明该段告警是服务告警
								#pass
								LISTS = []
								NOW = f.readline()
								NOW = f.readline()
								notify = NOW.split('Notification Type: ')[1]
								LISTS.append(notify.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								NOW = f.readline()
								service = NOW.split('Service: ')[1]
								LISTS.append(service.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								host = NOW.split('Host: ')[1]
								LISTS.append(host.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								addr = NOW.split('Address: ')[1]
								LISTS.append(addr.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								state = NOW.split('State: ')[1]
								LISTS.append(state.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								NOW = f.readline()
								time = NOW.split('Date/Time: ')[1]
								LISTS.append(time.split('\n')[0].encode('UTF-8'))
								NOW = f.readline()
								NOW = f.readline()
								NOW = f.readline()
								info = f.readline()	# 由于换行了，该处可不做正则
								LISTS.append(info.split('\n')[0].encode('UTF-8'))
				
								writer.writerow(LISTS)
				
if __name__ == '__main__':
	convert()
