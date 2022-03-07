#!/usr/bin/python3

import os
import glob
import subprocess

# 服务于从国家台网下载的数据重命名

for fname in glob.glob("*.SAC"):
    sections = fname.split('.')
    prefix = '.'.join(sections[:-2])
    newfname = prefix + '.M.SAC'
    print(newfname)
    os.rename(fname, newfname)

for fname in glob.glob("SAC_PZs*"):
    parts = fname.split('_')
    partone = '_'.join(parts[0:4])
    newfname = partone + '_' + parts[5] + '_' + parts[4]
    print(newfname)
    os.rename(fname, newfname)

# deleting sacfile not with pzfile
print("Deleting sacfile which don't have pzfile!")
for fname in glob.glob('*.SAC'):
    medium = '_'.join(fname.split('.')[6:10])
    pzfname = 'SAC_PZs_' + medium
    if not(os.path.exists(pzfname)):
        print(fname)
        os.unlink(fname)



