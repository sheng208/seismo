#!/usr/bin/python3

import os
import sys
import glob
import subprocess

os.putenv("SAC_DISPLAY_COPYRIGHT", '0')


def usage():
    print(
    '''
    addgc.py filenames
    '''
    )
    sys.exit()

if sys.argv[1:]:
    fnames = sys.argv[1:]
else:
    usage()

saccmd = ''

for fname in fnames:
    gcmin, gcmax = fname.split('_')[:-1]
    # as for 0.5 degree, discrepancy may be small
    #gc = (float(gcmin) + float(gcmax))*0.5
    gc = float(gcmin)
    gc = '%.2f' % gc
    saccmd += 'r %s\n' % fname
    saccmd += 'ch gcarc %s\n' % gc
    saccmd += 'wh\n'

saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())

