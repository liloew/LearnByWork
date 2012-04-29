#!/bin/bash
########################################################################
# Version 2.0
# auther lilo
# email lo.yu.linux@gmail.com
# date:2012-04-29
#
# This file is used to modify the permissions of the directory and files
# Update the file by using chmod -R.It's implement in a rescursive way.
#
########################################################################
x=`ls -al | grep "^d" | cut -d " " -f9 | grep -v "\." | grep "."`
for i in $x ;do
	chmod -R 755 "$i"/cn/
	chmod -R 777 "$i"/cn/data/
	chmod -R 777 "$i"/cn/special/
	chmod -R 777 "$i"/cn/uploads/
	chmod 777 "$i"/cn/
done