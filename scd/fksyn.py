#!/usr/bin/python3

import subprocess
import sys
import getopt

def usage():
    print('''
    fksyn.py -d evdp -g gcmin/gcmax/gcgap -M mag/strike/dip/rake -m prem
    -A az
    ''')
    exit()

if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], 'd:g:M:m:A:', '')

optdict = dict.fromkeys(['-d', '-g', '-M', '-m', '-A'], '')
for optkey, optvalue in opts:
    if not(optvalue):
        sys.exit('You have to add a parameter for the option: %s!' % optkey)
    optdict[optkey] = optvalue

gcmin, gcmax, gcgap = optdict['-g'].split('/')
gcmin, gcmax, gcgap = float(gcmin), float(gcmax), float(gcgap)

evdp = optdict['-d']

gc = gcmin
while gc >= gcmin and gc <= gcmax:
    gcarc = '%.1f' % gc
    bashcmd = 'syn -M%s -D3.8 -A%s -O%s_%s_%s.z -G%s_%s/%s.grn.0' % (optdict['-M'], \
            optdict['-A'], optdict['-m'], evdp, gcarc, optdict['-m'], evdp, gcarc)
    gc += gcgap
    subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(bashcmd.encode())




