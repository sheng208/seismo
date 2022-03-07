#!/usr/bin/python3

import getopt
import os
import subprocess
import sys
import re


def usage():
    sys.exit('''
    align.py -a s1 files
    ''')
    return

if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], "a:", "")

if not(opts):
    sys.exit("Check input arguments!!!!!!!!!!!!!")

optdict = dict.fromkeys(['-a'], '')

for optname, optvalue in opts:
    optdict[optname] = optvalue

if re.search("s1", optdict['-a']):
    align = 't3'
else:
    align = 't4'

saccmd = 'echo on\n'
for fname in fnames:
    fpath = '../criteria/' + fname
    if os.path.exists(fpath):
        cmdsaclst = 'saclst t3 f %s' % fpath
        t_S = subprocess.getoutput(cmdsaclst).split()[1]
        saccmd += 'r %s\n' % fname
        saccmd += 'ch kt3 spick t3 %s\n' % t_S
        saccmd += 'wh\n'
    else:
        print('No file: %s!' % fpath)
saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())



