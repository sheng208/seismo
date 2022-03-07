#!/usr/bin/python3


import subprocess
import glob
import os
import sys


def usage():
    print(
    '''
    datarotate.py name_of_sacfiles
    ''')
    sys.exit()


os.putenv('SAC_DISPLAY_COPYRIGHT', '0')
if sys.argv[1:]:
    fnames = sys.argv[1:]
else:
    usage()

prefixs = set()
for fname in fnames:
    prefix = '.'.join(fname.split('.')[0:9])
    prefixs.add(prefix)

saccmd = 'echo off \n'
#saccmd = 'echo on \n'
for prefix in prefixs:
    # Checking BHZ,BHE.BHN and the orthogonality of BHE,BHN
    BHZ = prefix + '.BHZ.M.SAC'
    if not(os.path.exists(BHZ)):
        print('%s: Vertical component missing!' % prefix)
        continue
    if os.path.exists(prefix + '.BHE.M.SAC') and os.path.exists(prefix + '.BHN.M.SAC'):
        BHE = prefix + '.BHE.M.SAC'
        BHN = prefix + '.BHN.M.SAC'
    elif os.path.exists(prefix + '.BH1.M.SAC') and os.path.exists(prefix + '.BH2.M.SAC'):
        BHE = prefix + '.BH1.M.SAC'
        BHN = prefix + '.BH2.M.SAC'
    else:
        print('%s: Horizontal component missing!' % prefix)
        continue
    cmdsaclst = 'saclst cmpaz f ' + BHE
    junk, ecmpaz = subprocess.getoutput(cmdsaclst).split()
    cmdsaclst = 'saclst cmpaz f ' + BHN
    junk, ncmpaz = subprocess.getoutput(cmdsaclst).split()
    cmpazdelta = abs(float(ecmpaz) - float(ncmpaz))
    if not(abs(cmpazdelta-90) <= 0.01 or abs(cmpazdelta-270) <= 0.01):
        print('{}: cmpaz1={}, cmpaz2={} are not orthogonal!'.format(prefix, ecmpaz, ncmpaz))
        continue
    cmdsaclst = 'saclst delta f ' + BHZ
    junk, zdelta = subprocess.getoutput(cmdsaclst).split()
    cmdsaclst = 'saclst delta f ' + BHE
    junk, edelta = subprocess.getoutput(cmdsaclst).split()
    cmdsaclst = 'saclst delta f ' + BHN
    junk, ndelta = subprocess.getoutput(cmdsaclst).split()
    if not(float(zdelta) == float(edelta) and float(zdelta) == float(ndelta)):
        print('%s: delta not equal!' % prefix)
        continue

    BHR, BHT, BHZ0 = prefix + '.BHR', prefix + '.BHT', prefix + '.BHZ'
    
    print('Rotating %s, %s to %s, %s!' % (BHE, BHN, BHR, BHT))
    saccmd += 'r %s %s \n' % (BHE, BHN)
    saccmd += 'setbb bcut (max &1,b& &2,b&) \n'
    saccmd += 'setbb ecut (min &1,e& &2,e&) \n'
    saccmd += 'setbb bcut (%bcut% + 0.1) \n'
    saccmd += 'setbb ecut (%ecut% - 0.1) \n'
    saccmd += 'cut %bcut% %ecut% \n'
    saccmd += 'r %s %s \n' % (BHE, BHN)
    saccmd += 'rotate to gcp \n'
    saccmd += 'w %s %s \n' % (BHR, BHT)
    saccmd += 'r %s \n' % BHZ
    saccmd += 'w %s \n' % BHZ0
    saccmd += 'cut off \n'
    saccmd += 'r %s \n' % BHR
    saccmd += 'ch kcmpnm BHR \n'
    saccmd += 'wh \n'
    saccmd += 'r %s \n' % BHT
    saccmd += 'ch kcmpnm BHT \n'
    saccmd += 'wh \n'
    saccmd += 'r %s \n' % BHZ0
    saccmd += 'ch kcmpnm BHZ \n'
    saccmd += 'wh \n'
saccmd += 'q \n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())



