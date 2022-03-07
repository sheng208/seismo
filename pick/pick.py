#!/usr/bin/python3

import glob
import subprocess
import os

os.putenv("SAC_DISPLAY_COPYRIGHT", '0')

saccmd = 'echo off \n'
for fname in glob.glob('*BHR'):
    prefname = '.'.join(fname.split('.')[:-1])
    BHT = prefname + '.BHT'
    if os.path.exists(BHT):
        cmdsaclst = 'saclst kt3 t3 f %s' % BHT
        pick_phase, pick_s = subprocess.getoutput(cmdsaclst).split()[1:]
        saccmd += 'r %s \n' % fname
        saccmd += 'ch kt3 %s t3 %s \n' % (pick_phase, pick_s)
        saccmd += 'wh \n'
    else:
        print('Delete %s due to No %s' % (fname, BHT))
        os.unlink(fname)

saccmd += 'q \n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())
