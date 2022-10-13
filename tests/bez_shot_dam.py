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


def calc_error(dist, ret):
    # calculate error the model damage calculations have compared to
    # the real game data
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
            lin_error.append(lin_e)
            bez_error.append(bez_e)
            if lin_e < bez_e:
                lin_anywhere_better = True
                lin_bet_indicators.append("V")
            else:
                lin_bet_indicators.append(" ")

        ret[gun]["lin_error"] = lin_error
        ret[gun]["bez_error"] = bez_error
        ret[gun]["lin_bet_indicators"] = lin_bet_indicators
        ret[gun]["lin_anywhere_better"] = lin_anywhere_better


def calc_dam(dist, gun, offset=0.15):
    lin_dam = [gun.shot_dam(i, "bod_dam") for i in dist]
    bez_dam = [gun.bez_shot_dam(i, "bod_dam", offset=offset) for i in dist]

    return lin_dam, bez_dam


def bisect_error(dist, gun, loweroff, upperoff):
    pass


def print_res(dist, ret):
    # print a table on stdout showing the error each model has at various
    # points to the damage values recorded from the game.
    for gun in ret.keys():
        print()
        print(f"{gun}")
        print("      " + ' '.join([f"{i:>5}"
                                   for i
                                   in ret[gun]["lin_bet_indicators"]]))
        print("dist: " + ' '.join([f"{i:>5}" for i in dist]))
        print("lin:  " + ' '.join([f"{i:>5.2f}"
                                   for i in ret[gun]["lin_error"]]))
        print("bez:  " + ' '.join([f"{i:>5.2f}"
                                   for i in ret[gun]["bez_error"]]))
        print("Average error:")
        print(f"lin: {np.mean(ret[gun]['lin_error']):0.2f}%"
              f" bez: {np.mean(ret[gun]['bez_error']):0.2f}%")
        print("Linear better anywhere than bezier:"
              f" {ret[gun]['lin_anywhere_better']}")
        print("----------------------------------------------------------")
        print()


###################################################
# TODO: this has been written like shit mate. It isn't going to scale if you
# add another weapon here. Why would you do this :(
HK_HB = gun_obj.Hk419()
HK_HB.swap_attach("barrel", gun_obj.HeavyBarrel)
AK_HB = gun_obj.Ak74()
AK_HB.swap_attach("barrel", gun_obj.HeavyBarrel)
MP5 = gun_obj.Mp5()

# there should be 26 measurements for all the weapons featured here.
# this is all real data, recorded in game.
dist = [i for i in range(50, 301, 10)]
ak74_rdam = [36.30, 36.18, 35.84, 35.32, 34.68,
             33.81, 32.78, 31.74, 30.54, 29.25,
             27.99, 26.49, 25.13, 23.69, 22.35,
             20.91, 19.63, 18.34, 17.15, 16.06,
             15.11, 14.25, 13.59, 13.12, 12.81,
             12.71]
hk419_rdam = [34.10, 33.98, 33.67, 33.17, 32.51,
              31.76, 30.88, 29.80, 28.70, 27.49,
              26.27, 24.96, 23.60, 22.26, 21.02,
              19.62, 18.47, 17.39, 16.11, 15.13,
              14.23, 13.45, 12.82, 12.33, 12.04,
              11.94]
mp5_rdam = [26.00, 25.73, 24.97, 23.96, 22.57,
            20.87, 19.02, 17.09, 15.27, 13.27,
            11.54, 9.88, 8.67, 7.41, 6.73,
            6.5, 6.5, 6.5, 6.5, 6.5,
            6.5, 6.5, 6.5, 6.5, 6.5,
            6.5]

# sanity checking recorded data
exact_check(ak74_rdam, "ak74")
exact_check(hk419_rdam, "hk")
exact_check(mp5_rdam, "mp5")

ret = {}
ret["HK_HB"] = {}
ret["HK_HB"]["exact"] = hk419_rdam
ret["HK_HB"]["lin_dam"], ret["HK_HB"]["bez_dam"] = calc_dam(dist, HK_HB)
# error calc
ret["AK_HB"] = {}
ret["AK_HB"]["exact"] = ak74_rdam
ret["AK_HB"]["lin_dam"], ret["AK_HB"]["bez_dam"] = calc_dam(dist, AK_HB)
# error calc
ret["MP5"] = {}
ret["MP5"]["exact"] = mp5_rdam
ret["MP5"]["lin_dam"], ret["MP5"]["bez_dam"] = calc_dam(dist, MP5)
# error calc

error = calc_error(dist, ret)
print_res(dist, ret)

plot = True
if plot:
    offset = 0.15
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)

    ax1.set_title("HK419 Heavy Barrel")
    ax1.plot(dist, [i/HK_HB.bod_dam for i in hk419_rdam],
             label="Real HK419")
    HK_HB.gen_bez_curve(offset).plot(100, ax=ax1)
    ax1.legend(loc="upper right")

    ax2.set_title("AK74 Heavy Barrel")
    ax2.plot(dist, [i/AK_HB.bod_dam for i in ak74_rdam],
             label="Real AK74")
    AK_HB.gen_bez_curve(offset).plot(100, ax=ax2)
    ax2.legend(loc="upper right")

    ax3.set_title("MP5")
    ax3.plot(dist, [i/MP5.bod_dam for i in mp5_rdam],
             label="Real MP5")
    MP5.gen_bez_curve(offset).plot(100, ax=ax3)
    ax3.legend(loc="upper right")

    plt.show()
