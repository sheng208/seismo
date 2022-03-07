#!/usr/bin/python3

import glob
import os
import subprocess

for fname in glob.glob('*BH[RT]'):
    if os.path.exists(fname):
        cmdsaclst = 'saclst b t2 e f %s' % fname 
        # where we have saved the theoretical arrivaltime in HEADER t2
        begin, t2, endtime = subprocess.getoutput(cmdsaclst).split()[1:]
        indextime = float(t2) + 20
        if t2 == '-12345':
            print(fname, "    due to \'-12345\'")
            os.unlink(fname)
        elif float(t2) > float(endtime) or indextime > float(endtime) or float(t2) < float(begin):
            print(fname, "    due to \'t2 > e\' or \'index_time > e\' or \'t2 < b\'")
            os.unlink(fname)
