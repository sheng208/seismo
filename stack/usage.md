signal stack

### ~/seismo/stack/signalstack.py -G 64/90 -t -100/200 -n BHT *.BHT

### sac: pick S arrivaltime in sac

### ~/seismo/stack/addgc.py *_BHT


don't recommend using 'aftstack.py' to plot wavetrain
### ~/seismo/stack/aftstack.py -a s1 -G 64/90/0.5 -T -50/150/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -n BHT -S SKS,ScS *_BHT

### ~/seismo/stack/aftstack.py -a s1 -G 64/90/0.5 -T -50/150/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -n BHT -S SKS,ScS -E .,R,2020/214/7.26/124.05/492.4/60/90 *_BHT