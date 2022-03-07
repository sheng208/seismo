#!/usr/bin/python3

import subprocess
import getopt
import sys
import os
import re


def usage():
    print(
    '''
    aftstack.py -a phase -G gcmin/gcmax/gcgap -T tmin/tmax/tgap -M scale 
    -e evla/evlo/evdp -t nzyear/nzjday -n BHT[|BHR] -S SKS[,ScS] 
    -E Edirname,Esuffix,Enzyear/Enzjday/Eevla/Eevlo/Eevdp/Egcmin/Egcmax filenames
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

opts, fnames = getopt.getopt(sys.argv[1:], "a:T:G:M:e:t:n:S:E:", "")

if not(opts):
    sys.exit('Check input arguments!')

# Specify input option
opt_dict = dict.fromkeys(['-a', '-T', '-G', '-M', '-e', '-t', '-n', '-S', '-E'], '')

for name, value in opts:
    opt_dict[name] = value

align = opt_dict['-a']

tmin, tmax, tgap = opt_dict['-T'].split('/')
optionC = '-C' + tmin + '/' + tmax

scale = opt_dict['-M']

gcmin, gcmax, gcgap = opt_dict['-G'].split('/')

evla, evlo, evdp = opt_dict['-e'].split('/')

nzyear, nzjday = opt_dict['-t'].split('/')

sufname = opt_dict['-n']

if opt_dict['-E']:
    Edirname, Esuffix, Etext = opt_dict['-E'].split(',')
    Enzyear, Enzjday, Eevla, Eevlo, Eevdp, Egcmin, Egcmax = Etext.split('/')
    Eplot = True
    Efnames = Edirname + '/*_' + Esuffix
    Eannotation1 = '%s %s, evla = %s, evlo = %s, evdp = %s' \
        % (Enzyear, Enzjday, Eevla, Eevlo, Eevdp)
    Eannotation2 = 'Signal Stack from %s to %s deg by %s deg for %s' \
        % (Egcmin, Egcmax, gcgap, Esuffix)
else:
    Eplot = False


# Select target files
subfnames = []
for fname in fnames:
    cmdsaclst = 'saclst gcarc f %s' % fname
    gc = subprocess.getoutput(cmdsaclst).split()[1]
    if float(gc) >= float(gcmin) and float(gc) <= float(gcmax):
        subfnames.append(fname)


# Specify plot option
if re.search('s1', align):
    tlabel = '-T+t3'
    xlabel = '\"Time [s] aligned on S true\"'

ymin = float(gcmin) - 1
ymax = float(gcmax) + 1
blabel = '-Bx' + tgap + '+l' + xlabel + ' -Bya5f1+l\"Distance [deg]\" -BWSen'

jlabel = '-JX14c/21c'
rlabel = '-R' + tmin + '/' + tmax + '/' + str(ymin) + '/' + str(ymax)
mlabel = '-M' + scale + 'c'

outfname = '%s_%s_%s_%s_%s_%s' % (nzyear, nzjday, gcmin, gcgap, gcmax, sufname)

annotation1 = '%s %s, evla = %s, evlo = %s, evdp = %s' \
    % (nzyear, nzjday, evla, evlo, evdp)
annotation2 = 'Signal Stack from %s to %s deg by %s deg for %s' \
    % (gcmin, gcmax, gcgap, sufname)
horizon = (float(tmin) + float(tmax))*0.5


# Plot
gmtcmd = 'export GMT_SESSION_NAME=$$\n'
gmtcmd += 'gmt begin %s pdf\n' % outfname

gmtcmd += 'gmt basemap %s %s %s\n' % (jlabel, rlabel, blabel)
for fname in subfnames:
    gmtcmd += 'gmt sac %s %s %s %s -Ed -W0.5p,black\n' % (fname, tlabel, optionC, mlabel)

gmtcmd += 'echo %.1f %.1f %s | gmt text -F+f12p,6,black+a0+jMC -D0c/0.7c -N\n' \
    % (horizon, ymax, annotation2)
gmtcmd += 'echo %.1f %.1f %s | gmt text -F+f10p,6,black+a0+jMC -D0c/1.2c -N\n' \
    % (horizon, ymax, annotation1)
gmtcmd += 'echo \"0 %.1f\n0 %.1f\" | gmt plot -W1p,red,-\n' % (ymin, ymax)

if opt_dict['-S']:
    phases = opt_dict['-S'].split(',')
    for phase in phases:
        phasetos(float(gcmin), float(gcmax), evdp, phase)

if Eplot:
    gmtcmd += 'gmt sac %s %s %s %s -Ed -W0.5p,red\n' \
        % (Efnames, tlabel, optionC, mlabel)
    gmtcmd += 'echo %.1f %.1f %s | gmt text -F+f12p,6,red+a0+jMC -D0c/1.9c -N\n' \
        % (horizon, ymax, Eannotation2)
    gmtcmd += 'echo %.1f %.1f %s | gmt text -F+f10p,6,red+a0+jMC -D0c/2.4c -N\n' \
        % (horizon, ymax, Eannotation1)

gmtcmd += 'gmt end show'
subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())



