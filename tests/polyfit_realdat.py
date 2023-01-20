import os
import sys
from json import load
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_arsenal import get_arsenal


def cubic_func(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d


def quad_func(x, a, b, c):
    return a*x**2 + b*x + c


def perc_error(approx, exact):
    return abs(approx - exact)/exact*100


def print_coeffs(popt, dec=5):
    ret = " ".join([f"{chr(ord('a')+i)}: {popt[i]:.{dec}f}"
                    for i in range(len(popt))])
    print(ret)
    print(popt)


def print_p_errs(y, y_r, spaces=12, dec=2):
    print("Percentage Error")
    head_str = f"{'i':>{spaces}} {'y':>{spaces}}"
    reg_names = " ".join([f"{key:>{spaces}}" for key in y_r])
    reg_errnames = " ".join([f"{key:>{spaces}}" for key in y_r])
    print(head_str + reg_names + reg_errnames)
    for i in range(len(y)):
        bod_str = f"{i:{spaces}} {y[i]:{spaces}.{dec}f}"
        reg_vals = " ".join([f"{y_r[key][i]:{spaces}.{dec}f}" for key in y_r])
        # space-1 because the percentage signs throw the columns out otherwise
        reg_perrs = " ".join(
                [f"{perc_error(y_r[key][i], y[i]):{spaces-1}.{dec}f}%"
                 for key in y_r])
        print(bod_str + reg_vals + reg_perrs)


#############################################################################
# FIXME: you need to ensure that the polynomial function has been calculated
# against, say, the y axis because a function in x cannot just be moved around.
# you need to scale the functions output based on x.
try:
    with open("./realgundam.csv", 'r') as fp:
        realgundict = load(fp)
except FileNotFoundError as e:
    raise FileNotFoundError("Make sure to run gen_realdam_json.py first! \n"
                            f"{e}")

x = np.array(realgundict['dist'])
# make x vary from 0 to the min damage value. This will aid in scaling the
# function for weapons that don't have the same total falloff range ie: MP5
normx = x - x[0]
# convert the damage array into one that provides a falloff coeficient
arsn_dict = get_arsenal('ttk_dat')
gun = arsn_dict["AR"]["AK74_HB"]
y = np.array([i/gun.get_dam("bod_dam") for i in realgundict["AK74_HB"]])

# add moar here
y_r = {}
pops = {}  # coefficeints go in here
pops["cub reg"] = curve_fit(cubic_func, normx, y)
y_r["cub reg"] = cubic_func(normx, *pops["cub reg"][0])  # predicted y value
pops["quad reg"] = curve_fit(quad_func, normx, y)
y_r["quad reg"] = quad_func(normx, *pops["quad reg"][0])  # predicted y value

# show the coefficeints we got for each regression
for key in pops:
    print(key)
    print_coeffs(pops[key][0])
print_p_errs(y, y_r)

plt.plot(normx, y, label="real")
for key in y_r:
    plt.plot(normx, y_r[key], label=key)
plt.legend(loc="upper right")
plt.ylabel("Damage Scaling Coefficient")
plt.xlabel("Falloff Range (m)")
plt.show()
