#!/usr/bin/python2.7

import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.message import Message
from email.header import Header
from base64 import b64encode

def main(argv):

	line = ''
	body = ''
	while 1:
		line = sys.stdin.readline()
		if line == "%\n":
			break
		body = body + line

	msg = MIMEText(body,'plain','utf-8')
	
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
