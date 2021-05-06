#!/usr/bin/env python2

import csv
import glob
import re
import sys


def decode_filename(filename):
    parts = filename.split('.')
    res = re.search('T(\d+).*-(\d+)-(\d+).*.log', filename)
    return dict(tool=parts[-2],
                model='GB' if 'catboost' in filename else 'RF',
                timeout=int(res.group(1)),
                trees=int(res.group(2)),
                depth=int(res.group(3)))


def decode_gnu_time(line):
    s = '(\d+.\d+)s real, (\d+.\d+)s user, (\d+.\d+)s kernel, (\d+) mmem'
    res = re.search(s, line)
    #return dict(realtime=float(res.group(1)),
    #            usertime=float(res.group(2)),
    #            kerneltime=float(res.group(3)),
    #            memory=int(res.group(4))/ 1024)
    return dict(runtime=float(res.group(1)),
                memory=int(res.group(4))/ 1024)


def decode_silva_output(filename):
    d = decode_filename(filename)

    with open(filename, 'r') as f:
        lines = f.readlines()
        vals = lines[-2].split()
        d['unsolved'] = int(vals[7])
        d['robust'] = int(vals[8])
        d['fragile'] = int(vals[9])
        d['vulnerable'] = int(vals[10])
        d['broken'] = int(vals[11])
        d.update(decode_gnu_time(lines[-1]))
        
    return d


def decode_vote_output(filename):
    d = decode_filename(filename)

    with open(filename, 'r') as f:
        lines = f.readlines()
        d['robust'] = int(lines[-7][12:])
        d['fragile'] = int(lines[-6][12:])
        d['vulnerable'] = int(lines[-5][12:])
        d['broken'] = int(lines[-4][12:])
        d['unsolved'] = int(lines[-3][12:])
        
        d.update(decode_gnu_time(lines[-1]))
        
    return d


def decode_log(filename):
    print 'processing', filename
    
    if 'vote' in filename:
        return decode_vote_output(filename)
    else:
        return decode_silva_output(filename)


def decode_logdir(path):
    res = [decode_log(filename)
           for filename in glob.glob(path + '/*.log')]

    names = ['timeout', 'model', 'trees', 'depth', 'tool',
             'runtime', 'memory', 'robust', 'fragile',
             'vulnerable', 'broken', 'unsolved']

    table = sorted(res, key=lambda k: [k[name] for name in names])

    timeout = None
    model = None

    for row in table:
        if timeout != row['timeout'] or model != row['model']:
            timeout = row['timeout']
            model = row['model']
            filename = 'T%s.%s.csv' % (timeout, model)
            print 'saving to', filename
            f = open(filename, 'w')
            w = csv.DictWriter(f, fieldnames=names)
            w.writeheader()
        
        w.writerow(row)


if __name__ == '__main__':
    decode_logdir('logs')

