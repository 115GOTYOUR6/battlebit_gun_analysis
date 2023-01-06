from json import load
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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


def print_p_errs(y, y_r, spaces=12, dec=2):
    print("Percentage Error")
    head_str = f"{'i':>{spaces}} {'y':>{spaces}}"
    reg_names = " ".join([f"{key:>{spaces}}" for key in y_r])
    reg_errnames = " ".join([f"{key:>{spaces}}" for key in y_r])
    print(head_str + reg_names + reg_errnames)
    for i in range(len(y)):
        bod_str = f"{i:{spaces}} {y[i]:{spaces}.{dec}f}"
        reg_vals = " ".join([f"{y_r[key][i]:{spaces}.{dec}f}" for key in y_r])
        # FIXME: the percent signs in this string are throwing the alingment
        # of the following ones out.
        reg_perrs = " ".join(
                [f"{perc_error(y_r[key][i], y[i]):{spaces}.{dec}f}%"
                 for key in y_r])
        print(bod_str + reg_vals + reg_perrs)


try:
    with open("./realgundam.csv", 'r') as fp:
        realgundict = load(fp)
except FileNotFoundError as e:
    raise FileNotFoundError("Make sure to run gen_realdam_json.py first! \n"
                            f"{e}")

x = np.array(realgundict['dist'])
y = np.array(realgundict["AK74_HB"])

# add moar here
y_r = {}
pops = {}
pops['cub reg'] = curve_fit(cubic_func, x, y)
y_r["cub reg"] = cubic_func(x, *pops["cub reg"][0])
pops['quad reg'] = curve_fit(quad_func, x, y)
y_r["quad reg"] = quad_func(x, *pops["quad reg"][0])

for key in pops:
    print_coeffs(pops[key][0])
print_p_errs(y, y_r)

plt.plot(x, y, label="real")
for key in y_r:
    plt.plot(x, y_r[key], label=key)
plt.legend(loc="upper right")
plt.show()
