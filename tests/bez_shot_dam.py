# testing to make the bezier modelling accurate to the game data.

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gun_obj


def exact_check(x, gun_name):
    for i in range(len(x) - 1):
        current = x[i]
        ne = x[i+1]
        if current < ne:
            raise ValueError(f"problem at index {i} {gun_name}")


def perc_error(approx, exact):
    return abs(approx - exact)/exact*100


def print_res(dist, ret):
    # print a table on stdout showing the error each model has at various
    # points to the damage values recorded from the game.
    for gun in ret.keys():
        lin_error = []
        bez_error = []
        lin_bet_indicators = []
        lin_anywhere_better = False
        for i in range(len(dist)):
            exp = ret[gun]["exact"][i]
            lin = ret[gun]["lin_dam"][i]
            bez = ret[gun]["bez_dam"][i]
            lin_e = perc_error(lin, exp)
            bez_e = perc_error(bez, exp)
            if lin_e < bez_e:
                lin_anywhere_better = True
                lin_bet_indicators.append("V")
            else:
                lin_bet_indicators.append(" ")
            lin_error.append(lin_e)
            bez_error.append(bez_e)

        print()
        print(f"{gun}")
        print("      " + ' '.join([f"{i:>5}" for i in lin_bet_indicators]))
        print("dist: " + ' '.join([f"{i:>5}" for i in dist]))
        print("lin:  " + ' '.join([f"{i:>5.2f}" for i in lin_error]))
        print("bez:  " + ' '.join([f"{i:>5.2f}" for i in bez_error]))
        print("Average error:")
        print(f"lin: {np.mean(lin_error):0.2f}% bez: {np.mean(bez_error):0.2f}%")
        print(f"Linear better anywhere than bezier: {lin_anywhere_better}")
        print("----------------------------------------------------------")
        print()


HK_HB = gun_obj.Hk419()
HK_HB.swap_attach("barrel", gun_obj.HeavyBarrel)
AK_HB = gun_obj.Ak74()
AK_HB.swap_attach("barrel", gun_obj.HeavyBarrel)
MP5 = gun_obj.Mp5()

# there should be 26 measurements for all the weapons featured here.
# this is all real data, recorded in game.
dist = [i for i in range(50, 301, 10)]
ak74_hb = [36.30, 36.18, 35.84, 35.32, 34.68,
           33.81, 32.78, 31.74, 30.54, 29.25,
           27.99, 26.49, 25.13, 23.69, 22.35,
           20.91, 19.63, 18.34, 17.15, 16.06,
           15.11, 14.25, 13.59, 13.12, 12.81,
           12.71]
hk_hb = [34.10, 33.98, 33.67, 33.17, 32.51,
         31.76, 30.88, 29.80, 28.70, 27.49,
         26.27, 24.96, 23.60, 22.26, 21.02,
         19.62, 18.47, 17.39, 16.11, 15.13,
         14.23, 13.45, 12.82, 12.33, 12.04,
         11.94]
mp5 = [26.00, 25.73, 24.97, 23.96, 22.57,
       20.87, 19.02, 17.09, 15.27, 13.27,
       11.54, 9.88, 8.67, 7.41, 6.73,
       6.5, 6.5, 6.5, 6.5, 6.5,
       6.5, 6.5, 6.5, 6.5, 6.5,
       6.5]

# sanity checking recorded data
exact_check(ak74_hb, "ak74")
exact_check(hk_hb, "hk")
exact_check(mp5, "mp5")

ret = {}
ret["HK_HB"] = {}
ret["HK_HB"]["lin_dam"] = [HK_HB.shot_dam(i, "bod_dam") for i in dist]
ret["HK_HB"]["bez_dam"] = [HK_HB.bez_shot_dam(i, "bod_dam") for i in dist]
ret["HK_HB"]["exact"] = hk_hb
ret["AK_HB"] = {}
ret["AK_HB"]["lin_dam"] = [AK_HB.shot_dam(i, "bod_dam") for i in dist]
ret["AK_HB"]["bez_dam"] = [AK_HB.bez_shot_dam(i, "bod_dam") for i in dist]
ret["AK_HB"]["exact"] = ak74_hb
ret["MP5"] = {}
ret["MP5"]["lin_dam"] = [MP5.shot_dam(i, "bod_dam") for i in dist]
ret["MP5"]["bez_dam"] = [MP5.bez_shot_dam(i, "bod_dam") for i in dist]
ret["MP5"]["exact"] = mp5

print_res(dist, ret)

plot = True
if plot:
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)

    ax1.set_title("HK419 Heavy Barrel")
    ax1.plot(dist, [i/HK_HB.bod_dam for i in hk_hb],
             label="Real HK419")
    HK_HB.gen_bez_curve().plot(100, ax=ax1)
    ax1.legend(loc="upper right")

    ax2.set_title("AK74 Heavy Barrel")
    ax2.plot(dist, [i/AK_HB.bod_dam for i in ak74_hb],
             label="Real AK74")
    AK_HB.gen_bez_curve().plot(100, ax=ax2)
    ax2.legend(loc="upper right")

    ax3.set_title("MP5")
    ax3.plot(dist, [i/MP5.bod_dam for i in mp5],
             label="Real MP5")
    MP5.gen_bez_curve().plot(100, ax=ax3)
    ax3.legend(loc="upper right")

    plt.show()
