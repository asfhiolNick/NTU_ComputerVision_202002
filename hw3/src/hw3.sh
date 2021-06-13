#!/usr/bin/env bash
STARTTIME=$(date +%s)
time python3 part1.py
time python3 part2.py
time python3 part3.py
time python3 part4.py; 
ENDTIME=$(date +%s)
echo "Time elpased $(($ENDTIME - $STARTTIME)) seconds"