#!/bin/bash

`echo ~/seismo/weekquake/datarename.py`

# Only supported by CMTSOLUTION
`echo ~/seismo/weekquake/dataprocess.py -m ../CMTSOLUTION -l 0 -L 3500 -f 0.02 -F 5 -q S -d 0.025 *.SAC`
#`echo ~/seismo/weekquake/dataprocess.py -m ../CMTSOLUTION -l 0 -L 3500 -f 0.02 -F 20 -q S -d 0.025 *.SAC` # for Pcd
#`echo ~/seismo/weekquake/dataprocess.py -o 2021.12.12.8.58.8.0 -e -60.69/154.11/10 -l 0 -L 3500 -f 0.02 -F 0.5 -q S -d 0.025 *.SAC`
#`echo ~/seismo/weekquake/dataprocess.py -o 2021.12.12.8.58.8.0 -e -60.69/154.11/6.5 -l 0 -L 3500 -f 0.02 -F 0.2 -q S -d 0.025 *.SAC`

`echo ~/seismo/weekquake/datarotate.py *.SAC`

`echo ~/seismo/weekquake/unlink.py`

#`~/seismo/weekquake/dataplot.py -a p -T -150/250/a50f10 -M 0.6 -G 130/169 -A 225/294 -b 156/83/-2/247/88/-173/5.968/25 -m Europe *.BHZ`

#`~/seismo/weekquake/dataplot.py -a s -T -50/150/a50f10 -M 0.6 -G 59/92 -A 18/41 *.BHT`

#`echo ~/seismo/weekquake/dataplot.py -a s -T -50/150/a50f10 -M 0.6 -G 59/92 -A 18/41 -b 150/35/-128/13/63/-67/4.71/25 -g /home/sheng/GyPSuM/GyPSuM.Grids.1deg.S.P/Grid.GyPSuM.S.22.2650-2900km *.BHT`
# used time: 3m 23s 5ms

# 2021-10-11, Mw6.9, 69.1km, 56.26N 156.55W, Alaska Peninsula,  Bug: Cant process it by seisplot.sh
