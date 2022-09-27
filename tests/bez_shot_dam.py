import sys
import os
import numpy as np
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gun_obj


def perc_error(approx, exact):
    return (approx - exact)/exact*100


def print_res(dist, exp, ret, ret2):
    lin_error = []
    bez_error = []
    for i in range(len(dist)):
        lin_error.append(perc_error(ret[i], exp[i]))
        bez_error.append(perc_error(ret2[i], exp[i]))
        print()
        print(f"dist: {dist[i]}")
        print(f"exp: {exp[i]}")
        print(f"lin: {ret[i]:0.2f} error: {lin_error[i]:0.2f}%")
        print(f"bez: {ret2[i]:0.2f} error: {bez_error[i]:0.2f}%")

    print()
    print("Average error:")
    print(f"lin: {np.mean(lin_error):0.2f}% bez: {np.mean(bez_error):0.2f}%")
    print("----------------------------------------------------------")
    print()


gun = gun_obj.Hk419()
gun.swap_attach("barrel", gun_obj.HeavyBarrel)
dist = [30, 80, 100, 150, 200]
exp = [34.10, 33.21, 31.75, 28.28, 19.62]
ret = [gun.shot_dam(i, "bod_dam") for i in dist]
ret2 = [gun.bez_shot_dam(i, "bod_dam") for i in dist]
print_res(dist, exp, ret, ret2)
