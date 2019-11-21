#!/bin/bash
PATH=$PATH:/usr/sbin/:/bin/
while true; do
    DATE=`date +"%Y-%m-%d_%H-%M-%S"`;
    traceroute $1 > ~/traceroute_$2-$3_$DATE.txt;
    sleep 30s;
done