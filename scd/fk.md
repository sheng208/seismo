## Construct a prem model file for 'fk'

# ~/seismo/scd/fkmodel.py
used for generating the model file, prem, whick is necessary for 'fk'

## Plot the synthetics produced by 'fk' and 'syn'

##### fkrun.py
./fkrun.py -g 60.0/90.0/0.5 -N 4096/0.5/1/0.2/0.3 -M prem/492.4/f

# ~/seismo/scd/fkrun.py -g 64.0/90.0/0.5 -N 8192/0.25/1/0.2/0.3 -M prem/492.4/f

./fkrun.py -g 60.0/90.0/0.5 -N 4096/0.5/1/0.2/0.3 -M model/492.4/f
./fkrun.py -g 73/85/1 -N 4096/0.5/1/0.2/0.3 -M model/492.4/f

##### fksyn.py
# ~/seismo/scd/fksyn.py -d 492.4 -g 64.0/90.0/0.5 -M 6.4/150/35/-128 -m prem -A 30

./fksyn.py -d 492.4 -g 60/90/1 -M 6.4/150/35/-128 -m model -A 30
./fksyn.py -d 492.4 -g 73/85/1 -M 6.4/150/35/-128 -m model -A 30


##### fkwhead.py
# ~/seismo/scd/fkwhead.py -d 492.4 -H 0.02/1 prem_492.4_*

./fkwhead.py -d 492.4 -H 0.02/0.2 model_492.4_*
./fkwhead.py -d 492.4 -H 0.02/1 model_492.4_*


mv model_492.4_* model_plot/
#### sac
ppk

##### fkplot.py
../fkplot.py -a s1 -G 64/90/0.5 -T -50/150/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -n BHT -s .,prem_492.4_,t

../fkplot.py -a s1 -G 64/90/0.5 -T -50/150/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -n BHT -s .,model_492.4_,t -E ../fkdata,BHT,2020/214/7.26/124.05/492.4/60/90



## Note:

While want to change the value of nt in model.h, you should take the memory into account.



### Conclusion
根据CMTSOLUTION决定syn中-D的值；
滤波不要局限于5-50s，可以更宽的滤波；
fk中的dt推荐0.5，可以信服看到更多的东西；
......


# ~/seismo/scd/vsplot.py -a s1 -G 64/90/0.5 -T -50/150/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -s ./model200_plot,model200_492.4_,t -E ./model300_plot,model300_492.4,t -o 200_300_t


# ../vsplot.py -a s1 -G 64/90/0.5 -T -30/100/a50f10 -M 0.6 -e 7.26/124.05/492.4 -t 2020/214 -s ./model01syn,model01_492.4_,t -E ./sac,,_BHT -o model

### Record
