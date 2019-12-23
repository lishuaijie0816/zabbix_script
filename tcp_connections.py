#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess

status = {'TIME_WAIT': 0,
          'CLOSE_WAIT': 0,
          'FIN_WAIT1': 0,
          'ESTABLISHED': 0,
          'SYN_RECV': 0,
          'LAST_ACK': 0,
          'LISTEN': 0}

result = sys.argv[1]

output = subprocess.check_output(" netstat -an | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}' ",
                                 shell=True)

for i in output.strip().split('\n'):
    status[i.split()[0]] = i.split()[1]

print status[result]
