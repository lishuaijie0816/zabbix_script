#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from subprocess import check_output, call
import sys
import os


def parase_iostat(cmd_all, disk_name, disk_state):
    last_index = cmd_all.rindex('Device')
    cmd = cmd_all[last_index:]
    iostat_info = cmd.strip().split('\n')

    disk_dict = OrderedDict()

    for info in iostat_info:
        if 'Device' in info:
            device = info.strip().split()
            for dev in device:
                if dev == 'Device:':
                    continue
                disk_dict.setdefault(dev, 0)
        if disk_name in info:
            vdx = info.strip().split()[1:]
            for index, key in enumerate(disk_dict.keys()):
                disk_dict[key] = vdx[index]

    return disk_dict[disk_state]


if __name__ == '__main__':

    disk_name = sys.argv[1]
    disk_state = sys.argv[2]
    check_iostat = check_output('ps -ef |grep "iostat -x -d 1" |grep -v grep  |wc -l', shell=True)

    if int(check_iostat) and os.path.exists('/tmp/iostat_output'):
        cmd_all = check_output('/usr/bin/tail -n20 /tmp/iostat_output', shell=True)
        if os.path.getsize('/tmp/iostat_output') > 102400:
            call('pkill iostat', shell=True)
            call('rm /tmp/iostat_output', shell=True)
            call('nohup /usr/bin/iostat -x -d 1 > /tmp/iostat_output 2>/dev/null &', shell=True)
        print parase_iostat(cmd_all, disk_name, disk_state)
    else:
        call('nohup /usr/bin/iostat -x -d 1 > /tmp/iostat_output 2>/dev/null &', shell=True)
        print None
