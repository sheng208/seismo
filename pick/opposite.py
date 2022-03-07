#!/usr/bin/python3

import subprocess
import glob
import os

os.putenv('SAC_DISPLAY_COPYRIGHT', '0')

saccmd = 'echo on\n'
for fname in glob.glob('*.BHR'):
    prefix = '.'.join(fname.split('.')[:-1])
    newfname = prefix + ".R"
    saccmd += 'r %s\n' % fname
    saccmd += 'mul -1.0\n'
    saccmd += 'w %s\n' % newfname

saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())
