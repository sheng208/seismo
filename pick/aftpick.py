#!/usr/bin/python3

import os
import glob
import subprocess

for fname in glob.glob('*BH[RT]'):
    cmdsaclst = 'saclst t3 f %s' % fname
    t3 = subprocess.getoutput(cmdsaclst).split()[1]
    if t3 == '-12345':
        print(fname, "       due to t3 = \'-12345\'")
        os.unlink(fname)
