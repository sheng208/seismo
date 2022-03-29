#!/usr/bin/python3

import math


def prem(radius):

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
    return vels

# five parameters describing D" layer
def model(radii, H_D, H_TL, d_Vs, H_BL, d_Vs_cmb, \
    H_LV, d_Vs_lv, H_HV, HV_top, d_Vs_hv):
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
        # velocity between D" layer and low velocity zone above
        if H_HV:
            # interface in D"
            r_D_0 = 3480.0 + H_D + H_LV + H_HV
            r_D_1 = 3480.0 + H_D + H_LV + H_HV - HV_top
            r_D_2 = 3480.0 + H_D + H_LV
            r_D_3 = 3480.0 + H_D
            r_D_4 = 3480.0 + H_D - H_TL
            r_D_5 = 3480.0 + H_BL
            # corresponding shear velocity
            Vs_D_0 = prem(r_D_0)
            Vs_D_1 = Vs_D_0*(1 + d_Vs_hv)
            Vs_D_2 = Vs_D_1
            Vs_D_3 = Vs_D_2*(1 + d_Vs_lv)
            Vs_D_4 = Vs_D_3*(1 + d_Vs)
            Vs_D_5 = Vs_D_4
            Vs_D_6 = Vs_D_5*(1 + d_Vs_cmb)
            # different shear velocity from PREM
            if radius <= r_D_0 and radius > r_D_1:
                vels = (radius - r_D_0)*(Vs_D_0 - Vs_D_1)/HV_top \
                    + Vs_D_0
            elif radius <= r_D_1 and radius > r_D_2:
                vels = (Vs_D_1 - Vs_D_2)*(radius - r_D_1)/(H_HV - HV_top) \
                    + Vs_D_1
            elif radius <= r_D_2 and radius > r_D_3:
                vels = (radius - r_D_2)*(Vs_D_2 - Vs_D_3)/H_LV \
                    + Vs_D_2
            elif radius <= r_D_3 and radius > r_D_4:
                vels = (radius - r_D_3)*(Vs_D_3 - Vs_D_4)/H_TL \
                    + Vs_D_3
            elif radius <= r_D_4 and radius > r_D_5:
                vels = (radius - r_D_4)*(Vs_D_4 - Vs_D_5)/(H_D - H_TL - H_BL) \
                    + Vs_D_4
            elif radius <= r_D_5 and radius > 3480.0:
                vels = (radius - r_D_5)*(Vs_D_5 - Vs_D_6)/H_BL \
                    + Vs_D_5

        elif H_LV:
            # interface in D"
            r_D_0 = 3480.0 + H_D + H_LV
            r_D_1 = 3480.0 + H_D
            r_D_2 = 3480.0 + H_D - H_TL
            r_D_3 = 3480.0 + H_BL
            # corresponding shear velocity
            Vs_D_0 = prem(r_D_0)
            Vs_D_1 = prem(r_D_1)*(1 + d_Vs_lv)
            Vs_D_2 = Vs_D_1*(1 + d_Vs)
            Vs_D_4 = Vs_D_2*(1 + d_Vs_cmb)
            # different shear velocity from PREM
            if radius <= r_D_0 and radius > r_D_1:
                vels = Vs_D_1 + (radius - r_D_1)*(Vs_D_0 - Vs_D_1)/H_LV
            elif radius <= r_D_1 and radius > r_D_2:
                vels = Vs_D_1 + (r_D_1 - radius)*(Vs_D_2 - Vs_D_1)/H_TL
            elif radius <= r_D_2 and radius > r_D_3:
                vels = Vs_D_2
            elif radius <= r_D_3 and radius > 3480.0:
                vels = ((radius - 3480.0)*(Vs_D_2 - Vs_D_4)) / H_BL \
                    + Vs_D_4
        else:
            r_D_1 = 3480.0 + H_D
            Vs_D_1 = prem(r_D_1)
            r_D_2 = 3480.0 + H_D - H_TL
            Vs_D_2 = Vs_D_1*(1 + d_Vs)
            r_D_3 = 3480.0 + H_BL
            Vs_D_4 = Vs_D_2*(1 + d_Vs_cmb)

            if radius <= r_D_1 and radius > r_D_2:
                vels = Vs_D_1 + (r_D_1 - radius)*(Vs_D_2 - Vs_D_1)/H_TL
            elif radius <= r_D_2 and radius > r_D_3:
                vels = Vs_D_2
            elif radius <= r_D_3 and radius > 3480.0:
                vels = ((radius - 3480.0)*(Vs_D_2 - Vs_D_4)) / H_BL \
                    + Vs_D_4
        
        veless.append(vels)
        velesp.append(velp)
        rhos.append(rho)
    
    return veless, velesp, rhos


def layers(H_D, H_TL, H_BL, H_LV, H_HV, HV_top):

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

    depth = (150 + 1970 - H_D - H_LV - H_HV) / 100
    for i in range(100):
        thicks.append(depth)
    # High velocity zone above low velocity
    if H_HV:
        depth = HV_top / 20
        for i in range(20):
            thicks.append(depth)
        depth = (H_HV - HV_top) / 10
        for i in range(10):
            thicks.append(depth)
    # low velocity zone or gradual increase above D"
    if H_LV:
        depth = H_LV / 40
        for i in range(40):
            thicks.append(depth)
    # top layer in D"
    if H_TL:
        depth = H_TL / 10
        for i in range(10):
            thicks.append(depth)
        #thicks.append(H_TL)
    # mid layer in D"
    depth = (H_D - H_TL - H_BL) / 40
    for i in range(40):
        thicks.append(depth)
    # bottom layer in D"
    if H_BL:
        depth = H_BL / 20
        for i in range(20):
            thicks.append(depth)
    
    # Outer core
    #thicks.append(18.5)
    #for i in range(50):
    #    thicks.append(20)
    #thicks.append(1240)
    # Inner core
    #thicks.append(1221.5)
    #thicks.append(21.5)
    #for i in range(60):
    #    thicks.append(20)
    thicks.append(3480.0)

    return thicks

# necessary parameters in D"
H_D, H_TL, d_Vs, H_BL, d_Vs_cmb = 460, 0, 0.03, 300, -0.02
H_LV, d_Vs_lv  = 300, -0.025
H_HV, HV_top, d_Vs_hv = 200, 100, 0.01

# Obtain a list for radius
radii = []
thicks = layers(H_D, H_TL, H_BL, H_LV, H_HV, HV_top)
radius = 6371.0 - 24.4
r = 24.4
for thick in thicks:
    radius -= 0.5*thick
    radii.append(radius)
    radius -= 0.5*thick
    r += thick
# Get Vs, Vp
veless, velesp, rhos = model(radii, H_D, H_TL, d_Vs, H_BL, d_Vs_cmb, \
    H_LV, d_Vs_lv, H_HV, HV_top, d_Vs_hv)
thicks[0] += 24.4

# Creating a model for 'fk'
fo = open('modelz3', 'w')
for i in range(len(thicks)):
    element = "%6.2f %6.3f %6.3f %6.3f\n" \
        % (thicks[i], veless[i], velesp[i], rhos[i])
    fo.write(element)
fo.close()
print(r)

# three parameters: H_D, H_TL, d_Vs
# sublayer in D", model
# don't need Qs and Qp
# 地壳部分也许可以视为一个整体融入上地幔，在模型中

