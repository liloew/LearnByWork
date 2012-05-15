#!/bin/bash
###########################################
#
#	Version 1.0
#	auther	lilo
#	E-mail	lo.yu.linux@gmail.com	# priority
#	E-mail	liushuililuo@126.com
#	E-mail	564901391@qq.com
#	date	2012-05-15
# This scripts can generate the password by
# special number that somebody input through
# stdin.
#
###########################################
genpasswd(){
	local l=$1
	[ "$l" == "" ]	&& l=16
	tr -dc A-Za-z0-9_ < /dev/urandom | head -c ${l} | xargs
}
