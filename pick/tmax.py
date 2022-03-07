#!/usr/bin/python3

import glob
import os
import subprocess

tmax = 0
for fname in glob.glob('*.BHT'):
    cmdsaclst = 'saclst t2 t3 f %s' % fname
    t2, t3 = subprocess.getoutput(cmdsaclst).split()[1:]
    t = float(t3) - float(t2)
    if t >= tmax:
        tmax = t
print('The maximum of t3-t2 is: %f' %tmax)