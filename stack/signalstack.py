#!/usr/bin/python3

import subprocess
import getopt
import sys
import os

os.putenv('SAC_DISPLAY_COPYRIGHT', '0')

def usage():
    print(
    '''
    signalstack.py -G gcarcmin/gcarcmax -t tmin/tmax -n BHT[|BHR] filenames
    '''
    )
    sys.exit()

def sss(gcmin, tmin, tmax, sufname, fnames=[]):
    global saccmd
    gcmax = gcmin + 0.5
    sub_fnames = []
    s_times = []

    for fname in fnames:
        cmdsaclst = 'saclst gcarc t3 f %s' % fname
        gc, s_t = subprocess.getoutput(cmdsaclst).split()[1:]
        if float(gc) >= gcmin and float(gc) < gcmax:
            sub_fnames.append(fname)
            s_times.append(float(s_t))

    try:
        t_win_min = min(s_times) + tmin
        t_win_max = max(s_times) + tmax
    except ValueError:
        print('No file between %.1f and %.1f' % (gcmin, gcmax))
    else:
        for fname in sub_fnames:
            cmdsaclst = 'saclst t3 dist f %s' % fname
            s_t, dist = subprocess.getoutput(cmdsaclst).split()[1:]
            delay = t_win_max - tmax - float(s_t)
            saccmd += 'as %s distance %s delay %.1f s\n' % (fname, dist, delay)
        saccmd += 'timewindow %.1f %.1f\n' % (t_win_min, t_win_max)
        saccmd += 'sumstack\n'
        gcmin = "%.1f" % gcmin
        gcmax = "%.1f" % gcmax
        newfname = '%s_%s_%s' % (gcmin, gcmax, sufname)
        saccmd += 'writestack %s\n' % newfname
        saccmd += 'zerostack\n'


if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], "G:t:n:", "")

if not(opts):
    sys.exit("Check input argument!")

opt_dict = dict.fromkeys(['-G', '-t', '-n'], '')

for opt_name, opt_value in opts:
    opt_dict[opt_name] = opt_value

gc, gcmax = opt_dict['-G'].split('/')
gc = float(gc)
gcmax = float(gcmax)

tmin, tmax = opt_dict['-t'].split('/')

sufname = opt_dict['-n']

saccmd = 'sss\n'

while gc <= gcmax:
    sss(gc, float(tmin), float(tmax), sufname, fnames)
    gc = gc + 0.5

saccmd += 'q\n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())



