#!/usr/bin/env python
import glob
import os
import re


def decode_gnu_time(line):
    s = '(\d+.\d+)s real, (\d+.\d+)s user, (\d+.\d+)s kernel, (\d+) mmem'
    res = re.search(s, line)
    return (float(res.group(1)), int(res.group(4))/ 1024)


if __name__ == '__main__':
    dirname = os.path.dirname(__file__) or '.'
    print('property,runtime,memory,pass,fail')
    for filename in glob.glob('%s/logs/*.log' % dirname):
        with open(filename) as f:
            lines = f.readlines()
            prop = int(lines[0][9:])
            passed = int(lines[1][5:])
            failed = int(lines[2][5:])
            runtime, mem = decode_gnu_time(lines[-1])
            
            print('%d,%2.2f,%d,%d,%d' % (
                prop, runtime, mem, passed, failed
            ))
