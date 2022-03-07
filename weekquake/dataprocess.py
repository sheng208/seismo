#!/usr/bin/python3

import os
import re
import sys
import subprocess
import glob
import calendar
import time
import math
import getopt



def usage():
    print(
    '''
    dataprocess.py [-o oyear.omonth.oday.ohour.ominute.osec.omsec -e evlat/evlon/evdep] 
    -m ../CMTSOLUTION -l starttime -L endtime -f filterhz 
    -F FILTERHZ -q align_S_phase -d delta SACfiles

    with
        -m -- using CMTSOLUTION file to set event info
        -l -- minimum start of record from o
        -L -- maximum end of record from o
        -f -- minimum filter
        -F -- maximum filter
        -q -- determin which phase you want to align for S (S(Sdiff) or SKS)
        -d -- interpolate data delta
        SACfiles -- name of SAC files to be processed

    Notice:
        1.-l -L will automatically take care of the origin length of the record.
            and cut will be from o+starttime to o+endtime
        2.For BH? component, remember to use -d option to choose different sampling delta
    ''')
    exit()

def mday2jday(oyear, omonth, oday):
    '''
    according to the CMTSOLUTION, we here try to calculate Julian day
    '''
    time_sec = calendar.timegm((int(oyear), int(omonth), int(oday), 3, 3, 3))
    t = time.gmtime(time_sec)
    jday = t[7]
    return str(jday)

def tdiff(oyear, omonth, oday, ohour, ominute, osec, omsec, tadd):
    newtime = calendar.timegm((int(oyear), int(omonth), int(oday), int(ohour), int(ominute), int(osec)))
    newtime += (tadd + omsec/1000.0)
    msec = int((newtime - math.floor(newtime))*1000)
    newtime = math.floor(newtime)
    year, month, day, hour, minute, sec, wday, jday, isdst = time.gmtime(newtime)
    return str(year), str(jday), str(hour), str(minute), str(sec), str(msec)

def getcmt(cmtfile):
    cmt = []
    fo = open(cmtfile)
    while 1:
        line = fo.readline().rstrip()
        cmt.append(line)
        if not(line):
            break
    fo.close()
    pde_oyear, omonth, oday, ohour, ominute, osec1, junk1, junk2, junk3, junk4, junk5, junk6, junk7 = cmt[0].split()
    oyear = pde_oyear[-4:]
    osec = osec1.split('.')[0]
    omsec = int((float(osec1) - float(osec))*1000)
    junk1, junk2, tshift = cmt[2].split()
    junk1, junk2, hdur = cmt[3].split()
    junk, elat = cmt[4].split()
    junk, elon = cmt[5].split()
    junk, edep = cmt[6].split()
    junk, Mrr = cmt[7].split()
    junk, Mtt = cmt[8].split()
    junk, Mpp = cmt[9].split()
    junk, Mrt = cmt[10].split()
    junk, Mrp = cmt[11].split()
    junk, Mtp = cmt[12].split()
    return oyear, omonth, oday, ohour, ominute, osec, omsec, tshift, hdur, elat, elon, edep, Mrr, Mtt, Mpp, Mrt, Mrp, Mtp

'''
===============================================================================================
'''
os.putenv('SAC_DISPLAY_COPYRIGHT', '0')

if not(sys.argv[1:]):
    usage()

opts, SACfiles = getopt.getopt(sys.argv[1:], 'o:e:m:l:L:f:F:q:d:', '')

optdict = dict.fromkeys(['-o', '-e', '-m', '-l', '-L', '-f', '-F', '-q', '-d'], '')
for optkey, optvalue in opts:
    if not(optvalue):
        sys.exit('You have to add a parameter for the option: %s!' % optkey)
    optdict[optkey] = optvalue
if not(SACfiles):
    sys.exit('You have to choose the processing datafiles!')

if optdict['-d']:
    delta = optdict['-d']
else:
    delta = '1.0'

if optdict['-m']:
    cmtfile = optdict['-m']
    # USE CMTSOLUTION FILE
    print ('Adding eventinfo from ' + cmtfile)
    oyear, omonth, oday, ohour, ominute, osec, omsec, tshift, hdur, elat, elon, edep, Mrr, Mtt, Mpp, Mrt, Mrp, Mtp = getcmt(cmtfile)
    tshift = 0   # Force tshift = 0 with origin time, not centroid time
    ojday = mday2jday(oyear, omonth, oday)
    oyear1, ojday1, ohour1, ominute1, osec1, omsec1 = tdiff(oyear, omonth, oday, ohour, ominute, osec, omsec, tshift)
else:
    if not(optdict['-o'] and optdict['-e']):
        sys.exit('While without CMTSOLUTION, you should use options -o and -e!')
    oyear1, omonth1, oday1, ohour1, ominute1, osec1, omsec1 = optdict['-o'].split('.')
    ojday1 = mday2jday(oyear1, omonth1, oday1)
    elat, elon, edep = optdict['-e'].split('/')
    tshift = 0

small = 1.0e-5
undef = -12345.0
cundef = '-12345'

'''
======================================================================================
'''

saccmd = 'echo off \n'
#saccmd = 'echo on \n'
for SACfile in SACfiles:
    if not(os.path.exists(SACfile)):
        sys.exit('No such file to be processed:' + SACfile)
    print('Processing %s!' % SACfile)

    saccmd += 'r %s \n' % SACfile

    # step1: resample data
    print('Resampling!')
    cmdsaclst = 'saclst delta f %s ' % SACfile
    junk, delta0 = subprocess.getoutput(cmdsaclst).split()
    if float(delta) > float(delta0):
        delta1 = 0.5/float(delta)
        saccmd += 'lp p 2 c %.6f \n' % delta1
    saccmd += 'interp delta ' + delta + ' \n'
    saccmd += 'w over \n'

    # step2: Adding eventinfo
    print('Adding event info!')
    saccmd += 'ch o gmt %4s %3s %2s %2s %2s %3s \n' % (oyear1, ojday1, ohour1, ominute1, osec1, omsec1)
    saccmd += 'ch allt (0 - &1,o&) iztype IO \n'
    saccmd += 'ch evla ' + elat + ' evlo ' + elon + ' evdp ' + edep + ' \n'
    saccmd += 'wh \n'

    # step3: cut data window
    print('Cutting data window!')
    cmdsaclst = 'saclst o f %s' % SACfile
    junk, current_o = subprocess.getoutput(cmdsaclst).split()
    if abs(float(current_o) - undef) < small:
        print('you need origin info to cut record')
    saccmd += 'setbb begin (max &1,b& (&1,o& + %s)) \n' % optdict['-l']
    saccmd += 'setbb end (min &1,e& (&1,o& + %s)) \n' % optdict['-L']
    saccmd += 'cut o %begin% %end% \n'
    saccmd += 'r %s \n' % SACfile
    saccmd += 'cut off \n'
    
    # step4: rglitches; rmean; rtrend; taper
    print('rglitches; rmean; rtrend; taper')
    saccmd += 'rglitches; rmean; rtrend; taper \n'

    # step5: filter data
    print('Filtering!')
    f2, f3 = optdict['-f'], optdict['-F']
    saccmd += 'bp p 2 cor %12.6f %12.6f \n' % (float(f2), float(f3))
    saccmd += 'w over \n'

    # step6: transfer instrument responce
    print('Tranfering instrument responce!')
    f1, f4 = float(f2)*0.8, float(f3)*1.2
    netwk, stnm, isno, cmpnm = SACfile.split('.')[6:10]
    pzfile = 'SAC_PZs_' + netwk + '_' + stnm + '_' + isno + '_' + cmpnm
    print('transfer ' + pzfile)
    saccmd += 'trans from polezero subtype {} to none freq {:12.6f} {} {} {:12.6f} \n'.format(pzfile, f1, f2, f3, f4)
    saccmd += 'mul 1.0e9 \n'
    saccmd += 'w over \n'

    # step7: Adding P and S arrival info
    print('Adding P and S arrival info in kt1, t1 and kt2, t2!')
    cmd_saclst = "saclst gcarc f " + SACfile
    junk, gcarc = subprocess.getoutput(cmd_saclst).split()
    cmd_phtimes = "phtimes " + edep + " " + gcarc + " P"
    input_P_time = subprocess.getoutput(cmd_phtimes).split()
    Pph = input_P_time[0]
    Ptime = input_P_time[1]
    cmd_phtimes = "phtimes " + edep + " " + gcarc + " S"
    input_S_time = subprocess.getoutput(cmd_phtimes).split()[0:6]  # return in string
    list_number = len(input_S_time)
    while list_number < 6:
        input_S_time.append('')
        input_S_time.append('0')
        list_number += 2
    Sph_1 = input_S_time[0]
    Stime_1 = float(input_S_time[1])
    Sph_2 = input_S_time[2]
    Stime_2 = float(input_S_time[3])
    Sph_3 = input_S_time[4]
    Stime_3 = float(input_S_time[5])
    Sph = Sph_2
    Stime = Stime_2
    align_S_phase = optdict['-q']
    if (not(re.search('SKS', align_S_phase)) and not(re.search('SKS', Sph_1))):
        Sph = Sph_1
        Stime = Stime_1
    if (re.search('SKS', align_S_phase) and re.search('SKS', Sph_1)):
        Stime = Stime_1
        Sph = Sph_1
    if Sph_3:
        if re.search('Sdiff', Sph_3):
            Stime = Stime_3
            Sph = Sph_3
        else:
            Stime = Stime_1
            Sph = Sph_1
    saccmd += "evaluate to tmp1 " + str(Ptime) + " - " + str(tshift) + " \n"
    # if you want to use prem by taup rather than iasp91 in phtimes
    #cmdtaup = 'taup setsac -mod prem -ph %s-2 -evdpkm %s' % (Sph, SACfile)
    #subprocess.getoutput(cmdtaup)
    saccmd += "evaluate to tmp2 " + str(Stime) + " - " + str(tshift) + " \n"
    saccmd += "ch t1 %tmp1% t2 %tmp2% \n"
    #saccmd += 'ch t1 %tmp1% \n'
    saccmd += "ch kt1 " + str(Pph) + " kt2 " + str(Sph) + " \n"
    #saccmd += 'ch kt1 %s \n' % Pph
    saccmd += "wh \n"
saccmd += 'q \n'
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(saccmd.encode())



