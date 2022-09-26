import sys
import os
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gun_obj


def print_res(dist, exp, ret):
    for i in range(len(dist)):
        print(f"dist: {dist[i]} exp: {exp[i]} ret: {ret[i]}")


print()
gun = gun_obj.Hk419()
gun.swap_attach("barrel", gun_obj.HeavyBarrel)
dist = [30, 80, 100, 150, 200]
exp = ['a', 'b', 'b', 'h', 'j']
ret = [gun.bez_shot_dam(i, "bod_dam") for i in dist]
print_res(dist, exp, ret)
