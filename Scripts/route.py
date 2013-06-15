#!/usr/bin/env python

import os
from datetime import datetime

def run(route=None):
	fd = open('/proc/net/route')
	lines = fd.readlines()
	fd.close()
	lastLine = lines[len(lines)-1]
	change = ''.join(('/sbin/ip route change default via ', route))
	add    = ''.join(('/sbin/ip route add default via ', route))

	if lastLine.split('\t')[0] == 'wlan0' and lastLine.split('\t')[1] == '00000000':
		pass
	else:
		if lastLine.split('\t')[1] == '00000000':
			error = os.system(change)
			if error == 0:
				os._exit(0)
			else:
				os.system('echo "%s Changing Route error " >> /var/log/messages' % datetime.now())
		else:
			error = os.system(add)
			if error == 0:
				os._exit(0)
			else:
				os.system('echo "%s Adding route error " >> /var/log/messages' % datetime.now())

if __name__ == '__main__':
	run('192.168.1.1')
