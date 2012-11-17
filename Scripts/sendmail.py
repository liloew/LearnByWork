#!/usr/bin/python2.7

import sys

import smtplib
####################################
#	Add by lilo 2012-11-15 08:58
from email.mime.multipart import MIMEMultipart
####################################
from email.mime.text import MIMEText

from email.message import Message
from email.header import Header
from base64 import b64encode

# Debug for this script
import pdb

# msg = Message()

def main(argv):
#	for arg in argv:
#		print arg
	
	#pdb.set_trace()
	
	#base64stromg = base64.b64encode(sys.argv[1])
	#base64string = b64encode(sys.argv[1])
#	header = Header(base64string,'utf-8')

	###################################
	#	2012-11-15 08:50
	#body = ''
	#while 1:
	#	line = sys.stdin.readline()
	#	if line == '%\n':
	#		break
	#	body = body + line
	###################################

	line = ''
	body = ''
	while 1:
		line = sys.stdin.readline()
		if line == "%\n":
			break
		body = body + line
	##########################################
	#	Comments 2012-11-15 09:35
	#for i in range(4,13):
	#	line = line + sys.argv[i]
	#msg = MIMEText(line,'plain','utf-8')
	###########################################


	###########################################
	#	Comments 2012-11-15 09:17
	#line = ''
	#msg = MIMEMultipart('alternative')
	#for i in range(4,13):
	#	line = MIMEText(sys.argv[i],'plain')
	
	#msg.attach(line)



	#msg = MIMEText(sys.argv[4],'plain','utf-8')

	############################################
	#	2012-11-15 08:55
	#msg = MIMEText(body,'plain','utf-8')
	############################################

	#msg = MIMEText(sys.stdin.readlines(),'plain','utf-8')
	msg = MIMEText(body,'plain','utf-8')
	#msg['Subject'] = header
	#msg['Subject'] = sys.argv[1]
	
	senter = sys.argv[2]		# Must be equal to username and username = someone@domain.com
	receiver = sys.argv[3]
	msg['Subject'] = Header(sys.argv[1],'utf-8')
	msg['From'] = senter
	msg['To'] = receiver
	
	#s = smtplib.SMTP('localhost')
	username = 'username@example.com'
	passwd = 'password'
	s = smtplib.SMTP('smtp.example.com',25)
	s.login(username,passwd)
	s.sendmail(senter, [receiver], msg.as_string())
	s.quit()

if __name__ == '__main__' :
	main(sys.argv)
