#!/usr/bin/python3


import os
import glob
import subprocess


print('Unlinking the *.BH[RTZ] whose DEPMIN is nan!')
for fname in glob.glob('*.BH[RTZ]'):
    cmdsaclst = "saclst depmin o f %s" % fname
    value = subprocess.getoutput(cmdsaclst).split()[1:]
    prefix = '.'.join(fname.split('.')[:-1])
    if value[0] == '-nan' or value[1] != '0':
        print('Due to the DEPMIN of %s is nan, python3 will unlink the corresponding RTZ!')
        BHR = prefix + '.BHR'
        if os.path.exists(BHR):
            os.unlink(BHR)
        else:
            print('No such file: ', BHR)
        BHT = prefix + '.BHT'
        if os.path.exists(BHT):
            os.unlink(BHT)
        else:
            print('No such file: ', BHT)
        BHZ = prefix + '.BHZ'
        if os.path.exists(BHZ):
            os.unlink(BHZ)
        else:
            print('No such file: ', BHZ)

print("Unlinking SAC files!")
for fname in glob.glob("*.SAC"):
    print(fname)
    os.unlink(fname)
 
