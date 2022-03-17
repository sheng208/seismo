#!/usr/bin/python3

import math

def prem(radii):

    veless, velesp, rhos = [], [], []
    for radius in radii:    
        x = radius/6371.0
        # Ocean and Crust
        if radius <= 6371.0 and radius > 6356.0:
            vels = 3.200
            velp = 5.800
            rho = 2.600
        elif radius <= 6356.0 and radius > 6346.6:
            vels = 3.900
            velp = 6.800
            rho = 2.900
        # There are Ocean in PREM, but we don't consider it here
        # Isotropic LID
        elif radius <= 6346.6 and radius > 6291.0:
            vels = 2.1519 + 2.3481*x
            velp = 4.1875 + 3.9382*x
            rho = 2.6910 + 0.6924*x
        # Isotropic LVZ
        elif radius <= 6291.0 and radius > 6151.0:
            vels = 2.1519 + 2.3481*x
            velp = 4.1875 + 3.9382*x
            rho = 2.6910 + 0.6924*x
        # Transition zone
        elif radius <= 6151.0 and radius > 5971.0:
            vels = 8.9496 - 4.4597*x
            velp = 20.3926 - 12.2569*x
            rho = 7.1089 - 3.8045*x
        elif radius <= 5971.0 and radius > 5771.0:
            vels = 22.3512 - 18.5856*x
            velp = 39.7027 - 32.6166*x
            rho = 11.2494 - 8.0298*x
        elif radius <= 5771.0 and radius > 5701.0:
            vels = 9.9839 - 4.9324*x
            velp = 19.0957 - 9.8672*x
            rho = 5.3197 - 1.4836*x
        # Lower mantle
        elif radius <= 5701.0 and radius > 5600.0:
            vels = 22.3459 - 17.2473*x - 2.0834*math.pow(x, 2) \
                    + 0.9783*math.pow(x, 3)
            velp = 29.2766 - 23.6027*x + 5.5242*math.pow(x, 2) \
                    - 2.5514*math.pow(x, 3)
            rho = 7.9565 - 6.4761*x + 5.5283*math.pow(x, 2) \
                    - 3.0807*math.pow(x, 3)
        elif radius <= 5600.0 and radius > 3630.0:
            vels = 11.1671 - 13.7818*x + 17.4575*math.pow(x, 2) \
                    - 9.2777*math.pow(x, 3)
            velp = 24.9520 - 40.4673*x + 51.4832*math.pow(x, 2) \
                    - 26.6419*math.pow(x, 3)
            rho = 7.9565 - 6.4761*x + 5.5283*math.pow(x, 2) \
                    - 3.0807*math.pow(x, 3)
        elif radius <= 3630.0 and radius > 3480.0:
            vels = 6.9254 + 1.4672*x - 2.0834*math.pow(x, 2) \
                    + 0.9783*math.pow(x, 3)
            velp = 15.3891 - 5.3181*x + 5.5242*math.pow(x, 2) \
                    - 2.5514*math.pow(x, 3)
            rho = 7.9565 - 6.4761*x + 5.5283*math.pow(x, 2) \
                    - 3.0807*math.pow(x, 3)
        # Outer core
        elif radius <= 3480.0 and radius > 1221.5:
            vels = 0
            velp = 11.0487 - 4.0362*x + 4.8023*math.pow(x, 2) \
                    - 13.5732*math.pow(x, 3)
            rho = 12.5815 - 1.2638*x - 3.6426*math.pow(x, 2) \
                    - 5.5281*math.pow(x, 3)
        # Inner core
        elif radius <= 1221.5 and radius > 0:
            vels = 3.6678 - 4.4475*math.pow(x, 2)
            velp = 11.2622 - 6.3640*math.pow(x, 2)
            rho = 13.0885 - 8.8381*math.pow(x, 2)
        veless.append(vels)
        velesp.append(velp)
        rhos.append(rho)

    return veless, velesp, rhos

def layers():

    # defining thickness of every layer
    thicks = []
    # Ocean and Crust (24.4)
    #thicks.append(15)
    #thicks.append(9.4)
    # LID
    thicks.append(27.8)
    thicks.append(27.8)
    # LVZ
    for i in range(7):
        thicks.append(20)
    # Transition zone
    for i in range(9):
        thicks.append(20)
    for i in range(10):
        thicks.append(20)
    thicks.append(20)
    thicks.append(25)
    thicks.append(25)
    # Lower mantle
    thicks.append(21)
    for i in range(4):
        thicks.append(20)
    thicks.append(30)
    for i in range(97):
        thicks.append(20)
    thicks.append(30)
    for i in range(6):
        thicks.append(20)
    # Outer core
    thicks.append(18.5)
    for i in range(50):
        thicks.append(20)
    thicks.append(1240)
    # Inner core
    thicks.append(1221.5)
    #thicks.append(21.5)
    #for i in range(60):
    #    thicks.append(20)

    return thicks

# Obtain a list for radius
radii = []
thicks = layers()
#depth = 0
depth = 24.4
r = 24.4
for thick in thicks:
    r += thick
    radius = 6371.0 - depth - 0.5*thick
    radii.append(radius)
    depth += thick
# Get Vs, Vp
veless, velesp, rhos = prem(radii)
thicks[0] += 24.4

# Creating a model for 'fk'
fo = open('prem', 'w')
for i in range(len(thicks)):
    element = "%6.2f %6.3f %6.3f %6.3f\n" \
        % (thicks[i], veless[i], velesp[i], rhos[i])
    fo.write(element)
fo.close()
print(r)


