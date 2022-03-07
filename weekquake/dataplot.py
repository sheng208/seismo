#!/usr/bin/python3

'''
import modules
'''

import os
import glob
import sys
import subprocess
import math
import calendar
import time
import re
import getopt

################################## End


def usage():
    exit('''
    dataplot.py -a [o|p|s|r|l|vel] -T t_min/t_max/t_tick -M [size|size/alpha|size/s] -S [ScS,SKS]
    -s syn_dir,syn_prefix,syn_suffix,annotation -G gcarc_min/gcarc_max -A az_min/az_max -m mapname 
    -b strike1/dip1/slip1/strike2/dip2/slip2/mantissa/exponent -g xyzfile datafiles

    with:
        -a phase -- phase is one of:
            o -- align on origin time of event
            p,s -- align on p or s headers in data/synthetic-files
            r,l -- align on 3.8 or 4.4 km/s velocity
            vel -- align on given velocity (unit km/s)
        
        -T t_min/t_max/t_tick -- time window to plot
        
        -M mutiple traces
            size -- each trace will normalized to size (in inch)
            size/alpha -- plot absolute amplitude multiplied by size*r^alpha
                where r is the distance range inkm across surface
            size/s -- plot absolute amplitude multiplied by sprt(sin(gcarc))
                where gcarc is the distance in degrees
        
        -w width/r/g/b -- pen pen option for data. Default: 10/0/0/0
        
        -s syn_dir,syn_prefix,syn_suffix,annotation -- plot synthetics corresponding to datafiles
            with names: syn_dir/syn_prefix*.syn_suffix, such as ./s*.sac
        
        -G gcarc_min/gcarc_max -- will ignore data out of range. Default: 0/180
        
        -A az_min/az_max -- will ignore data out of range. Default 0/360
        
        -z -- Add this if TRINet data
    '''
    )

# if you want to plot synthetics, the function will impact your work
# A question: I don't get meaning of the phase 'align'
def aligning(align, filename):
    if re.search('o', align):
        t_label = '-T+t-3'
    elif re.search('s1', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph ' + align + '-3 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t3'
    elif re.search('spn', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph ' + align + '-4 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t4'
    elif re.search('sks', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph ' + align + '-5 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t5'
    elif re.search('pcp', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph ' + align + '-7 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t7'
    elif re.search('pkikp', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph ' + align + '-6 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t6'
    elif re.search('p', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph P-1 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t1'
    elif re.search('s', align):
        cmd_taup = 'taup setsac -mod prem -evdpkm -ph S-2 ' + filename
        subprocess.getoutput(cmd_taup)
        t_label = '-T+t2'
    elif re.search('r', align):
        t_label = '-T+r3.8'
    elif re.search('l', align):
        t_label = '-T+r4.4'
    else:
        t_label = '-T+r' + align
def align1(datafiles, aligning_phase, evdep):
    time_gcarc = ''
    for datafile in datafiles:
        cmdsaclst = 'saclst gcarc t2 f %s' % datafile
        gcarc, S_arivltime = subprocess.getoutput(cmdsaclst).split()[1:]
        cmdtaup = 'taup time -mod prem -h %s -deg %s -ph %s --time' % (evdep, gcarc, aligning_phase)
        phase_arivltime = subprocess.getoutput(cmdtaup).split()[0]
        if phase_arivltime:
            phase_align_S = float(phase_arivltime) - float(S_arivltime)
            time_gcarc += '%f %s\n' % (phase_align_S, gcarc)
    return time_gcarc

def sortfiles(datafiles):
    gcsdict, gcslist, fnames = {}, [], []
    for datafile in datafiles:
        cmdsaclst = 'saclst gcarc f %s' % datafile
        gcarc = float(subprocess.getoutput(cmdsaclst).split()[1])
        gcsdict[gcarc] = datafile
        gcslist.append(gcarc)
    gcslist.sort()
    for gcarc in gcslist:
        fnames.append(gcsdict[gcarc])
    return fnames

###############################################################################

# Checking input arguments

if not(sys.argv[1:]):
    usage()

opts, data_files = getopt.getopt(sys.argv[1:], "a:T:M:w:s:G:A:zm:S:b:g:", "")

if not(opts):
    exit("Check input arguments!!!!!!!!!!!!!!!!!!")

opt_dict = dict.fromkeys(['-a', '-T', '-M', '-w', '-s', '-G', '-A', '-z', '-m', '-S', '-b', '-g'], '')

for opt_name, opt_value in opts:
    opt_dict[opt_name] = opt_value

# Wow, this's diferent from the linux_plotdata.pl
if not(re.search("^(o|s1|spn|sks|pcp|pkikp|p|s|r|l|\d*\.\d*)$", opt_dict['-a'])):
    exit("Align on o,p,s,r,l,vel not: " + opt_dict['-a'])
else:
    align = opt_dict['-a']

if not(opt_dict['-T']):
    exit("Specify time window -T")
else:
    time_min, time_max, time_tick = opt_dict['-T'].split('/')
    cut_option = '-C' + time_min + '/' + time_max
    if (not(re.search("^(-|\d)\d*$", time_min)) or not(re.search("^\d*$", time_max))):
        exit("Is this a number? min_time: " + time_min + ", max_time: " + time_max)
    if (float(time_min) >= float(time_max)):
        exit("min_time " + time_min + " has to be smaller than max_time " + time_max)

if not(opt_dict['-M']):
    exit("Specify scale -M")
else:
    scale = opt_dict['-M']

# last to be done
if opt_dict['-s']:
    syn_dir, syn_prefix, syn_suffix, annotation = opt_dict['-s'].split(',')
    syn_filename = syn_dir + '/' + syn_prefix + '*.' + syn_suffix
    plot_syn = 1
else:
    plot_syn = 0

if opt_dict['-G']:
    gcarc_min, gcarc_max = opt_dict['-G'].split('/')
    if (float(gcarc_min) > float(gcarc_max)):
        exit("gcarc_min has to be smaller than gcarc_max")
    print ("Only plotting data within distance " + gcarc_min + " to " + gcarc_max + " degree")
else:
    gcarc_min = 0
    gcarc_max = 180

if opt_dict['-A']:
    az_min, az_max = opt_dict['-A'].split('/')
    if (float(az_min) > float(az_max)):
        exit("az_min has to be smaller than az_max")
    print ("Only plotting data within azimuth from " + az_min + " to " + az_max + " degree")
else:
    az_min = 0
    az_max = 360


# To be noted: I haven't deal with the postscript file name. Wow, I solved the problem.
OUT_FILE_PRENAME = 'Az.' + az_min + '.' + az_max + '.D.' + gcarc_min + '.' + gcarc_max

if opt_dict['-z']:
    trinet_data = 1
else:
    trinet_data = 0

############################ Ending checking



'''
Finding data-files
'''

file_number = len(data_files)
if (file_number < 1):
    exit("Specify data files")
print ("Number of datafiles: " + str(file_number))

used_data_files = []
for data_file in data_files:
    if trinet_data:
        cmd_saclst = "saclst knetwk kstnm gcarc az dist evlo evla evdp kinst nzyear nzjday f " + data_file
        junk, netw, stat, gcarc, az, dist, evlo, evla, evdp, comp, nzyear, nzjday = subprocess.getoutput(cmd_saclst).split()
    else:
        cmd_saclst = "saclst knetwk kstnm gcarc az dist evlo evla evdp kcmpnm nzyear nzjday f " + data_file
        junk, netw, stat, gcarc, az, dist, evlo, evla, evdp, comp, nzyear, nzjday = subprocess.getoutput(cmd_saclst).split()
    if (float(gcarc) > float(gcarc_min) and float(gcarc) < float(gcarc_max) and float(az) > float(az_min) and float(az) < float(az_max)):
        used_data_files.append(data_file)

# there I will think how to solve the connecting syn_file
if plot_syn:
    used_syn_files = []
    for syn_file in glob.glob(syn_filename):
        cmd_saclst = 'saclst gcarc f ' + syn_file
        junk, gcarc = subprocess.getoutput(cmd_saclst).split()
        if (float(gcarc) > float(gcarc_min) and float(gcarc) < float(gcarc_max)):
            aligning(align,syn_file)
            used_syn_files.append(syn_file)

print('Number of plotting datafiles: %d' % len(used_data_files))
################################################### End



'''
specifying all plot options
'''
# Did you have picked the phase in SAC ?
if re.search('o', align):
    t_label = '-T+t-3'
    time_label = '\"Time [s] from event\"'
elif re.search('s1', align):
    t_label = '-T+t3'
    time_label = '\"Time [s] aligned on S true\"'
elif re.search('spn', align):
    t_label = '-T+t4'
    time_label = '\"Time [s] aligned on SPn\"'
elif re.search('sks', align):
    t_label = '-T+t5'
    time_label = '\"Time [s] aligned on SKS\"'
elif re.search('pcp', align):
    t_label = '-T+t7'
    time_label = '\"Time [s] aligned on pcp\"'
elif re.search('pkikp', align):
    t_label = '-T+t6'
    time_label = '\"Time [s] aligned on pkikp\"'
elif re.search('p', align):
    t_label = '-T+t1'
    time_label = '\"Time [s] aligned on P\"'
elif re.search('s', align):
    t_label = '-T+t2'
    time_label = '\"Time [s] aligned on S\"'
elif re.search('r', align):
    t_label = '-T+r3.8'
    time_label = '\"Time-distance/3.8(km/s) [s]\"'
elif re.search('l', align):
    t_label = '-T+r4.4'
    time_label = '\"Time-distance/4.4(km/s) [s]\"'
else:
    t_label = '-T+r' + align
    time_label = '\"Time-distance/' + align + '(km/s) [s]\"'
Rmin = float(gcarc_min) - 0.1
Rmax = float(gcarc_max) + 0.1
b_label = '-Bx' + time_tick + '+l' + time_label + ' -Bya5f1+l\"Distance [deg]\" -BWSen'

x = float(time_max)*1.01
x2 = float(time_min) + (float(time_max) - float(time_min))*0.01
OUT_FILE_PRENAME = comp + '.' + OUT_FILE_PRENAME

j_label = '-JX14c/21c'
r_label = '-R' + str(time_min) + '/' + str(time_max) + '/' + str(Rmin) + '/' + str(Rmax)
m_label = '-M' + scale + 'c'



# plotting data and synthetics in GMT6

gmtcmd = 'export GMT_SEISSION_NAME=$$\n'
gmtcmd += 'gmt begin ' + OUT_FILE_PRENAME + ' pdf\n'

gmtcmd += 'gmt basemap ' + j_label + ' ' + r_label + ' ' + b_label + '\n'
for used_data_file in used_data_files:
    gmtcmd += 'gmt sac ' + used_data_file + ' ' + t_label + ' ' + cut_option + ' ' + m_label + ' -Ed -W0.5p,black\n'
    cmd_saclst = 'saclst knetwk kstnm az gcarc f ' + used_data_file
    junk, netwk, station, az, gcarc = subprocess.getoutput(cmd_saclst).split()
    az = '%.1f' % float(az)
    gmtcmd += 'echo ' + str(x) + ' ' + gcarc + ' ' + netwk + '.' + station + ' ' + az + ' | gmt text -F+f8p,6,black+a0+jML -N\n'

# while mark the SKS and ScS
if opt_dict['-S']:
    phases = opt_dict['-S'].split(',')
    for phase in phases:
        gcarc = float(gcarc_min)
        echo_gmt = ''
        while gcarc >= float(gcarc_min) and gcarc <= float(gcarc_max):
            cmdtaup = 'taup time -mod prem -h %s -deg %f -ph S --time' % (evdp, gcarc)
            Sarivlt = subprocess.getoutput(cmdtaup).split()
            cmdtaup = 'taup time -mod prem -h %s -deg %f -ph Sdiff --time' % (evdp, gcarc)
            Sdiffarivlt = subprocess.getoutput(cmdtaup).split()
            if Sarivlt:
                cmdtaup = 'taup time -mod prem -h %s -deg %f -ph %s --time' % (evdp, gcarc, phase)
                pharivlt = subprocess.getoutput(cmdtaup).split()
                if pharivlt:
                    ph_align_S = float(pharivlt[0]) - float(Sarivlt[0])
                    echo_gmt += '%f %f\n' % (ph_align_S, gcarc)
            elif Sdiffarivlt:
                cmdtaup = 'taup time -mod prem -h %s -deg %f -ph %s --time' % (evdp, gcarc, phase)
                pharivlt = subprocess.getoutput(cmdtaup).split()
                if pharivlt:
                    ph_align_Sdiff = float(pharivlt[0]) - float(Sdiffarivlt[0])
                    echo_gmt += '%f %f\n' % (ph_align_Sdiff, gcarc)
            step = (float(gcarc_max) - float(gcarc_min))/50
            gcarc += step
        gmtcmd += 'echo "%s" | gmt plot -W1p,red,-\n' % echo_gmt

h = (float(time_min) + float(time_max))*0.5
gmtcmd += 'echo ' + str(h) + ' ' + gcarc_max + ' ' + comp + ' ' + 'Az = ' + az_min + '~' + az_max + ' deg.' + ' Delta = ' + gcarc_min + '~' + gcarc_max + ' deg.' + ' | gmt text -F+f12p,6,black+a0+jMC -D0c/0.7c -N\n'
gmtcmd += 'echo ' + str(h) + ' ' + gcarc_max + ' ' + nzyear + ' ' + nzjday + ', ' + 'lat = ' + evla + ', lon = ' + evlo + ', depth = ' + evdp + ' | gmt text -F+f10p,6,black+a0+jMC -D0c/1.2c -N\n'
gmtcmd += 'echo \"0 ' + gcarc_min + '\n0 ' + gcarc_max + '\" | gmt plot -W1p,red,-\n'
# plot synthetics
if plot_syn:
    for used_syn_file in used_syn_files:
        gmtcmd += 'gmt sac ' + used_syn_file + ' ' + t_label + ' ' + cut_option + ' ' + m_label + ' -Ed -W0.5p,red\n'
        if annotation == '1':
            cmdsaclst = 'saclst knetwk kstnm az gcarc f %s' % used_syn_file
            netwk, station, az, gcarc = subprocess.getoutput(cmdsaclst).split()[1:]
            az = '%.1f' % float(az)
            gmtcmd += 'echo ' + str(x) + ' ' + gcarc + ' ' + netwk + '.' + station + ' ' + az + ' | gmt text -F+f8p,6,red+a0+jML -N\n'

gmtcmd += 'gmt end show'
subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())


# Plotting station map
if opt_dict['-m']:
    gmtcmd = 'export GMT_SESSION_NAME=$$\n'
    gmtcmd += 'gmt begin %s pdf\n' % opt_dict['-m']

    gmtcmd += 'gmt basemap -JKf15c -Rg -Baf\n'
    gmtcmd += 'gmt coast -Ggray\n'
    
    if opt_dict['-b']:
        strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent = opt_dict['-b'].split('/')
        gmtcmd += 'gmt meca -Sc0.2c -Gred <<EOF\n%s %s %s %s %s %s %s %s %s %s %s\nEOF\n' % (evlo, evla, evdp, strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent)
    else:
        gmtcmd += 'echo %s %s | gmt plot -Sa0.2c -W0.5p,red,solid -Gred\n' % (evlo, evla)
    
    for used_data_file in used_data_files:
        cmdsaclst = 'saclst stlo stla f %s' % used_data_file
        stlon, stlat = subprocess.getoutput(cmdsaclst).split()[1:]
        gmtcmd += 'echo %s %s | gmt plot -St0.06c -W0.5p,blue,solid -Gblue\n' % (stlon, stlat)

    gmtcmd += 'gmt end show'
    subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())


# Plotting GyPSuM
if opt_dict['-g']:
    fname = opt_dict['-g']
    gmtcmd = 'export GMT_SESSION_NAME=$$\n'
    gmtcmd += 'gmt begin GyPSuM pdf\n'

    #gmtcmd += 'gmt basemap -JKf15c -R0/360/-90/90 -Bya30 -BWsen+tGyPSuM\n'
    gmtcmd += 'gmt basemap -JM15c -R95/285/-25/70 -Bxa30f10 -Bya30f10 -BWSen+tGyPSuM\n'
    gmtcmd += 'gmt xyz2grd ' + fname + ' -G' + fname + '.grd -R95/285/-25/70 -I1/1 -fg\n'
    gmtcmd += 'gmt grd2cpt ' + fname + '.grd -Cseis -Z\n'
    #gmtcmd += 'gmt makecpt -Cseis -T-2/2/0.1 -D -Z\n'
    gmtcmd += 'gmt grdimage ' + fname + '.grd -C -E500\n'
    gmtcmd += 'gmt colorbar -C -DjCR+w5c/0.4c+o-1c/0c+m -Bxa2f1 -By+l\"dvs\"\n'
    gmtcmd += 'gmt coast -A1000 -W0.05\n'

    for used_data_file in used_data_files:
        cmdsaclst = 'saclst kt2 stlo stla f %s' % used_data_file
        phase, stlon, stlat = subprocess.getoutput(cmdsaclst).split()[1:]
        gmtcmd += 'echo %s %s | gmt plot -St0.15c -W0.5p,brown,solid -Gbrown\n' % (stlon, stlat)
        cmdtaup = 'taup_pierce -ph %s -mod prem -h %s -evt %s %s -sta %s %s -turn' % (phase, evdp, evla, evlo, stlat, stlon)
        turnlat, turnlon = subprocess.getoutput(cmdtaup).split()[-2:]
        gmtcmd += 'echo %s %s | gmt plot -Sc0.15c -W0.5p,brown,solid\n' % (turnlon, turnlat)
        print(used_data_file, turnlat, turnlon)
    if opt_dict['-b']:
        strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent = opt_dict['-b'].split('/')
        gmtcmd += 'gmt meca -Sc0.2c -Gred <<EOF\n%s %s %s %s %s %s %s %s %s %s %s\nEOF\n' % (evlo, evla, evdp, strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent)
    else:
        gmtcmd += 'echo %s %s | gmt plot -Sa0.2c -W0.5p,red,solid -Gred\n' % (evlo, evla)

    gmtcmd += 'gmt end show'
    subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())



