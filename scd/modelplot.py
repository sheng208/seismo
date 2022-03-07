#!/usr/bin/env python

import matplotlib.pyplot as plt

depth, depths, Vss = 0, [], []
with open('prem3', 'r') as fo:
    for out_string in fo.readlines():
        thick, Vs = out_string.split()[0:2]
        depth += float(thick)
        depths.append(depth)
        Vss.append(float(Vs))
fo.close()
depths[-1] = 2891.0

depth, depths_2, Vss_2 = 0, [], []
with open('model06', 'r') as fo:
    for out_string in fo.readlines():
        thick, Vs = out_string.split()[0:2]
        depth += float(thick)
        depths_2.append(depth)
        Vss_2.append(float(Vs))
fo.close()
depths_2[-1] = 2891.0
'''
depth, depths_3, Vss_3 = 0, [], []
with open('model50', 'r') as fo:
    for out_string in fo.readlines():
        thick, Vs = out_string.split()[0:2]
        depth += float(thick)
        depths_3.append(depth)
        Vss_3.append(float(Vs))
fo.close()
depths_3[-1] = 2891.0

depth, depths_4, Vss_4 = 0, [], []
with open('model80', 'r') as fo:
    for out_string in fo.readlines():
        thick, Vs = out_string.split()[0:2]
        depth += float(thick)
        depths_4.append(depth)
        Vss_4.append(float(Vs))
fo.close()
depths_4[-1] = 2891.0
'''
fig, ax = plt.subplots(figsize=(6,8))

ax.plot(Vss, depths, 'black')
ax.plot(Vss_2, depths_2, 'r')
#ax.plot(Vss_3, depths_3, 'b')
#ax.plot(Vss_4, depths_4, 'g')

ax.set(xlim=(6, 8), ylim=(3000, 2000))
ax.set_xlabel('Velocity (km/s)')
ax.set_ylabel('Depth (km)')

ax.legend(['prem', 'model06'])

plt.tight_layout()
#plt.show()
plt.savefig('model06.png')
