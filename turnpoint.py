#!/usr/bin/python3

import subprocess
import glob
import sys
import os

# red brown(maroon) gray purple4 

# Define option -R
Region = '-R110/170/0/50'
# Derive working path currently
dirpath = os.getcwd()


# plotting turn points of S wave
gmtcmd = 'export GMT_SESSION_NAME=$$\n'
gmtcmd += 'gmt begin turnpoint pdf\n'

gmtcmd += 'gmt basemap -JM15c %s -Bxa30f10 -Bya30f10 -BWSen+tGyPSuM\n' % Region
# absolute path of GyPSuM model file
fpath = '/home/sheng/GyPSuM/GyPSuM.Grids.1deg.S.P/Grid.GyPSuM.S.22.2650-2900km'
gmtcmd += 'gmt xyz2grd ' + fpath + ' -G' + fpath + '.grd %s -I1/1 -fg\n' % Region
gmtcmd += 'gmt grd2cpt ' + fpath + '.grd -Cseis -D\n'
gmtcmd += 'gmt grdimage ' + fpath + '.grd -C -E500\n'
gmtcmd += 'gmt colorbar -C -DjCR+w5c/0.4c+o-1c/0c+m -Bxa2f1 -By+l\"dvs\"\n'
gmtcmd += 'gmt coast -A1000 -W0.05\n'


# go to SAC files
fspath = dirpath + '/20170520a/sac1'
if os.path.exists(fspath):
    os.chdir(fspath)
else:
    sys.exit('%s isn\'t existing!' % fspath)
# focal mechanism file
fpath = dirpath + '/20170520a/beachball'
if os.path.exists(fpath):
    fo = open(fpath, 'r')
    strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent = fo.readline().rstrip().split('/')
    fo.close()
else:
    sys.exit('%s isn\'t existing!' % fpath)

for fname in glob.glob('*.BHT'):
    cmdsaclst = 'saclst evdp evla evlo stla stlo kt2 f %s' % fname
    evdp, evla, evlo, stlat, stlon, phase = subprocess.getoutput(cmdsaclst).split()[1:]
    cmdtaup = 'taup_pierce -ph %s -mod prem -h %s -evt %s %s -sta %s %s -turn' % (phase, evdp, evla, evlo, stlat, stlon)
    try:
        turnlat, turnlon = subprocess.getoutput(cmdtaup).split()[-2:]
    except ValueError:
        print('Couldn\'t get the turn point\'s lat,lon of S wave in %s' % fname)
    else:
        gmtcmd += 'echo %s %s | gmt plot -Sa0.2c -W0.5p,brown,solid\n' % (turnlon, turnlat)
gmtcmd += 'echo %s %s | gmt plot -Sa0.25c -W0.5p,brown,solid -Gbrown\n' % (evlo, evla)
#gmtcmd += 'gmt meca -Sc0.2c -Gred <<EOF\n%s %s %s %s %s %s %s %s %s %s %s\nEOF\n' % (evlo, evla, evdp, strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent)

# go to SAC files
fspath = dirpath + '/20181104b/sac1'
if os.path.exists(fspath):
    os.chdir(fspath)
else:
    sys.exit('%s isn\'t existing!' % fspath)
# focal mechanism file
fpath = dirpath + '/20181104b/beachball'
if os.path.exists(fpath):
    fo = open(fpath, 'r')
    strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent = fo.readline().rstrip().split('/')
    fo.close()
else:
    sys.exit('%s isn\'t existing!' % fpath)

for fname in glob.glob('*.BHT'):
    cmdsaclst = 'saclst evdp evla evlo stla stlo kt2 f %s' % fname
    evdp, evla, evlo, stlat, stlon, phase = subprocess.getoutput(cmdsaclst).split()[1:]
    cmdtaup = 'taup_pierce -ph %s -mod prem -h %s -evt %s %s -sta %s %s -turn' % (phase, evdp, evla, evlo, stlat, stlon)
    try:
        turnlat, turnlon = subprocess.getoutput(cmdtaup).split()[-2:]
    except ValueError:
        print('Couldn\'t get the turn point\'s lat,lon of S wave in %s' % fname)
    else:
        gmtcmd += 'echo %s %s | gmt plot -St0.2c -W0.5p,gray,solid\n' % (turnlon, turnlat)
gmtcmd += 'echo %s %s | gmt plot -St0.25c -W0.5p,gray,solid -Ggray\n' % (evlo, evla)
#gmtcmd += 'gmt meca -Sc0.2c -Gred <<EOF\n%s %s %s %s %s %s %s %s %s %s %s\nEOF\n' % (evlo, evla, evdp, strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent)

# go to SAC files
fspath = dirpath + '/20200801a/sac1'
if os.path.exists(fspath):
    os.chdir(fspath)
else:
    sys.exit('%s isn\'t existing!' % fspath)
# focal mechanism file
fpath = dirpath + '/20200801a/beachball'
if os.path.exists(fpath):
    fo = open(fpath, 'r')
    strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent = fo.readline().rstrip().split('/')
    fo.close()
else:
    sys.exit('%s isn\'t existing!' % fpath)

for fname in glob.glob('*.BHT'):
    cmdsaclst = 'saclst evdp evla evlo stla stlo kt2 f %s' % fname
    evdp, evla, evlo, stlat, stlon, phase = subprocess.getoutput(cmdsaclst).split()[1:]
    cmdtaup = 'taup_pierce -ph %s -mod prem -h %s -evt %s %s -sta %s %s -turn' % (phase, evdp, evla, evlo, stlat, stlon)
    try:
        turnlat, turnlon = subprocess.getoutput(cmdtaup).split()[-2:]
    except ValueError:
        print('Couldn\'t get the turn point\'s lat,lon of S wave in %s' % fname)
    else:
        gmtcmd += 'echo %s %s | gmt plot -Sc0.15c -W0.5p,red,solid\n' % (turnlon, turnlat)
gmtcmd += 'echo %s %s | gmt plot -Sc0.2c -W0.5p,red,solid -Gred\n' % (evlo, evla)
#gmtcmd += 'gmt meca -Sc0.2c -Gred <<EOF\n%s %s %s %s %s %s %s %s %s %s %s\nEOF\n' % (evlo, evla, evdp, strike1, dip1, rake1, strike2, dip2, rake2, mantissa, exponent)

os.chdir(dirpath)

gmtcmd += 'gmt end show'
subprocess.Popen(['bash'], stdin=subprocess.PIPE).communicate(gmtcmd.encode())



