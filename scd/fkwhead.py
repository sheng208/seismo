#!/usr/bin/python3

import subprocess
import os
import sys
import getopt

def usage():
    print('''
    fkwhead.py -d evdp -H f1/f2 prem_492.4_*
    ''')
    sys.exit()

if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], 'd:H:', '')

optdict = dict.fromkeys(['-d'], '')
for optkey, optvalue in opts:
    if not(optvalue):
        sys.exit('You have to add a parameter for the option: %s!' % optkey)
    optdict[optkey] = optvalue

evdp = optdict['-d']

f1, f2 = optdict['-H'].split('/')

os.putenv('SAC_DISPLAY_COPYRIGHT', '0')

saccmd = 'echo on\n'
for fname in fnames:
    if os.path.exists(fname):
        suffix = fname.split('_')[-1]
        gc = suffix[:-2]
        #taupcmd = 'taup time -mod prem -h %s -deg %s -ph S --time' % (evdp, gc)
        #travelS = subprocess.getoutput(taupcmd).split()
        saccmd += 'r %s\n' % fname
        saccmd += 'int\n'
        # interploate
        saccmd += 'interp delta 0.025\n'
        saccmd += 'w over\n'
        # cut the data window
        saccmd += 'setbb begin ( max &1,b ( &1,o + ' +  str(0) + ' ) )\n'
        saccmd += 'setbb end ( min &1,e ( &1,o + ' + str(3500) + ' ) )\n'
        saccmd += 'cut o %begin% %end%\n'
        saccmd += 'r %s\n' % fname
        saccmd += 'cut off\n'
        # 
        saccmd += 'rglitches;rmean;rtrend;taper\n'
        # filter
        saccmd += 'bp p 2 cor %s %s\n' % (f1, f2)
        saccmd += 'w over\n'
        saccmd += 'ch gcarc %s evdp %s\n' % (gc, evdp)
        #if travelS:
        #    saccmd += 'ch kt2 S t2 %s\n' % travelS[0]
        saccmd += 'wh\n'
    else:
        print('No such file: %s!' % fname)
saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())




