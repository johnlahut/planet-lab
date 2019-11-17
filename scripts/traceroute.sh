#!/bin/bash
PATH=$PATH:/usr/sbin/:/bin/
DATE=`date +"%Y-%m-%d_%H-%M-%S"`
/bin/traceroute $1 > ~/jlahut/$2-$3_$DATE.txt