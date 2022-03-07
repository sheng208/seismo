#!/usr/bin/python3

import subprocess
import sys
import os


os.putenv('SAC_DISPLAY_COPYRIGHT', '0')

def usage():
    print(
    '''
    reversed.py filenames
    '''
    )
    sys.exit()

if sys.argv[1:]:
    fnames = sys.argv[1:]
else:
    usage()

saccmd = 'echo on\n'
for fname in fnames:
    prefix = '_'.join(fname.split('_')[:-1])
    newfname = prefix + '_R'
    saccmd += 'r %s\n' % fname
    saccmd += 'mul -1.0\n'
    saccmd += 'w %s\n' % newfname

saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())
