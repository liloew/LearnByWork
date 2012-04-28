#!/bin/bash
########################################################################
# Version 1.0
# auther lilo
# email lo.yu.linux@gmail.com
# date:2012-04-28
#
# This file is used to modify the permissions of the directory and files
#
########################################################################
x=`ls -al | grep "^d" | cut -d " " -f9 | grep -v "\." | grep "."`
for i in $x ;do
pwd
cd "$i/cn/"
pwd
chmod 666 data/ 2>>~/errorlog-20120428
chmod 666 data/* 2>>~/errorlog-20120428
chmod 555 sys_manage/ 2>>~/errorlog-20120428
chmod 555 sys_manage/* 2>>~/errorlog-20120428
cd -
done
