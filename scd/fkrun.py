#!/usr/bin/python3

import subprocess
import getopt
import sys

def usage():
    print('''
    fkrun.py -g gcmin/gcmax/gcgap -N nt/dt/smth/dk/taper -M model/depth/f
    ''')
    sys.exit()

if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], 'g:N:M:', '')

optdict = dict.fromkeys(['-N', '-g', '-M'], '')
for optkey, optvalue in opts:
    if not(optvalue):
        sys.exit('You have to add a parameter for the option: %s!' % optkey)
    optdict[optkey] = optvalue

gcmin, gcmax, gcgap = optdict['-g'].split('/')
gcmin, gcmax, gcgap = float(gcmin), float(gcmax), float(gcgap)

fkcmd = 'fk.pl -M%s -N%s -D' % (optdict['-M'], optdict['-N'])
gc = gcmin
while gc >= gcmin and gc <= gcmax:
    fkcmd += ' %.1f' % gc
    gc += gcgap
subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(fkcmd.encode())



