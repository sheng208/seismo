#!/usr/bin/python3

import subprocess
import getopt
import sys
import os
import re


def usage():
    print(
    '''
    fkplot.py -a phase -G gcmin/gcmax/gcgap -T tmin/tmax/tgap -M scale 
    -e evla/evlo/evdp -t nzyear/nzjday -S SKS[,ScS] 
    -E Edir,Eprefix,Esuffix
    -s syndir,synprefix,synsuffix -o outfname filenames
    '''
    )
    sys.exit()

def phasetos(gcmin, gcmax, evdp, phase):
    gc = gcmin
    step = (gcmax - gcmin)*0.02
    alignline = ''
    global gmtcmd
    while gc <= gcmax:
        cmdtaup = 'taup time -mod prem -h %s -deg %.1f -ph S --time' \
            % (evdp, gc)
        St = subprocess.getoutput(cmdtaup).split()
        cmdtaup = 'taup time -mod prem -h %s -deg %.1f -ph %s --time' \
            % (evdp, gc, phase)
        phaset = subprocess.getoutput(cmdtaup).split()
        cmdtaup = 'taup time -mod prem -h %s -deg %.1f -ph Sdiff --time' \
            % (evdp, gc)
        Sdifft = subprocess.getoutput(cmdtaup).split()
        
        if St and phaset:
            phase_align_S_t = float(phaset[0]) - float(St[0])
        elif Sdifft and phaset:
            phase_align_S_t = float(phaset[0]) - float(Sdifft[0])
        else:
            phase_align_S_t = 0

        if phase_align_S_t:
            alignline += '%.1f %.1f\n' % (phase_align_S_t, gc)

        gc = gc + step

    gmtcmd += 'echo "%s" | gmt plot -W1p,red,-\n' % alignline


if not(sys.argv[1:]):
    usage()

opts, fnames = getopt.getopt(sys.argv[1:], "a:T:G:M:e:t:S:E:s:o:", "")

if not(opts):
    sys.exit('Check input arguments!')

# Specify input option
opt_dict = dict.fromkeys(['-a', '-T', '-G', '-M', '-e', '-t', \
    '-S', '-E', '-s', '-o'], '')

for name, value in opts:
    opt_dict[name] = value

align = opt_dict['-a']

tmin, tmax, tgap = opt_dict['-T'].split('/')
optionC = '-C' + tmin + '/' + tmax

scale = opt_dict['-M']

gcmin, gcmax, gcgap = opt_dict['-G'].split('/')

evla, evlo, evdp = opt_dict['-e'].split('/')

nzyear, nzjday = opt_dict['-t'].split('/')

outfname = opt_dict['-o']

if opt_dict['-E']:
    Edirname, Eprefix, Esuffix = opt_dict['-E'].split(',')
    Eplot = True
    Efnames = Edirname + '/' + Eprefix + '*' + Esuffix
else:
    Eplot = False

if opt_dict['-s']:
    syndir, synprefix, synsuffix = opt_dict['-s'].split(',')
    synplot = True
    synfnames = syndir + '/' + synprefix + '*' + synsuffix
else:
    synplot = False


# Select target files
subfnames = []
for fname in fnames:
    cmdsaclst = 'saclst gcarc f %s' % fname
    gc = subprocess.getoutput(cmdsaclst).split()[1]
    if float(gc) >= float(gcmin) and float(gc) <= float(gcmax):
        subfnames.append(fname)


# Specify plot option
if re.search('s1', align):
    tlabel = '-T+t3'    # changed with command line
    xlabel = '\"Time [s] aligned on S true\"'
elif re.search('s', align):
    tlabel = '-T+t2'
    xlabel = '\"Time [s] aligned on S\"'

ymin = float(gcmin) - 1
ymax = float(gcmax) + 1
blabel = '-Bx' + tgap + '+l' + xlabel + ' -Bya5f1+l\"Distance [deg]\" -BWSen'

jlabel = '-JX14c/21c'
rlabel = '-R' + tmin + '/' + tmax + '/' + str(ymin) + '/' + str(ymax)
mlabel = '-M' + scale + 'c'


# Plot
gmtcmd = 'export GMT_SESSION_NAME=$$\n'
gmtcmd += 'gmt begin %s pdf\n' % outfname

gmtcmd += 'gmt basemap %s %s %s\n' % (jlabel, rlabel, blabel)

if len(subfnames):
    for fname in subfnames:
        gmtcmd += 'gmt sac %s %s %s %s -Ed -W0.5p,black\n' \
            % (fname, tlabel, optionC, mlabel)

    if opt_dict['-S']:
        phases = opt_dict['-S'].split(',')
        for phase in phases:
            phasetos(float(gcmin), float(gcmax), evdp, phase)

if Eplot:
    gmtcmd += 'gmt sac %s %s %s %s -Ed -W0.5p,black\n' \
        % (Efnames, tlabel, optionC, mlabel)

if synplot:
    gmtcmd += 'gmt sac %s %s %s %s -Ed -W0.5p,red\n' \
        % (synfnames, tlabel, optionC, mlabel)

gmtcmd += 'echo \"0 %.1f\n0 %.1f\" | gmt plot -W1p,red,-\n' % (ymin, ymax)

gmtcmd += 'gmt end show'
subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())


