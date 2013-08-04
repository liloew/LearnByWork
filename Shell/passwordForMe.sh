#! /bin/bash
echo ${1} | md5sum | head -c 10 | xargs
