#!/usr/bin/python3

import os
import glob
import subprocess


# rename
print('Renaming sacfile and pzfile according to fixed pattern!')
for fname in glob.glob("*.SAC"):  
    cmdsaclst = 'saclst KZTIME f %s' % fname
    partone = '.'.join(fname.split('.')[5:7])
    ftime = subprocess.getoutput(cmdsaclst).split()[1]
    parttwo = '.'.join(ftime.split(':'))
    partthree = '.'.join(fname.split('.')[0:5])
    newfname = partone + '.' + parttwo + '.' + partthree + '.SAC'
    print (newfname)
    os.rename(fname, newfname)

cmd = 'mv ./*/* .'
subprocess.getoutput(cmd)

for fname in glob.glob("SACPZ*"):
    parts = fname.split('.')
    isnum = parts[3]
    partone = '_'.join(parts[1:3])
    parttwo = parts[4]
    if isnum == '--':
        newfname = 'SAC_PZs_' + partone + '_' + '_' + parttwo
    else:
        newfname = 'SAC_PZs_' + partone + '_' + isnum + '_' + parttwo
    print (newfname)
    os.rename(fname,newfname)

# deleting sacfile not with pzfile
print("Deleting sacfile which don't have pzfile!")
for fname in glob.glob('*.SAC'):
    medium = '_'.join(fname.split('.')[6:10])
    pzfname = 'SAC_PZs_' + medium
    if not(os.path.exists(pzfname)):
        print(fname)
        os.unlink(fname)



