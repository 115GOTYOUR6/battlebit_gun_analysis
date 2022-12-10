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


def calc_g_per_errors(dist, g_dict, models):
    """
    Calculate the error each gun in the dict 'g_dict' has relative to the
    exact damage values
    """
    for gun in g_dict.keys():
        for mod in models:
            # don't judge me, I didn't want to indent the long ass line....
            if mod == models[0]:
                continue
            g_dict[gun][f"{mod}_error"] = [perc_error(g_dict[gun][f"{mod}_dam"][i],
                                                      g_dict[gun][f"{models[0]}_dam"][i])
                                           for i in range(len(dist))]


def add_g_models(g_dict, g_name, dist, real_dams, models, gun_obj,
                 offset=0.15):
    """Add the damage values inplace for each model for the given weapon"""
    g_dict[g_name] = {}
    for mod in models:
        if mod == models[0]:
            g_dict[g_name][f"{models[0]}_dam"] = real_dams
        else:
            g_dict[g_name][f"{mod}_dam"] = calc_dam(dist, mod, gun_obj,
                                                    offset=offset)


def calc_dam(dist, model, gun, offset=0.15):
    dam_vals = [gun.shot_dam(i, "bod_dam", model=model, offset=offset)
                for i in dist]
    return dam_vals


# yet to be implemented
def bisect_error(dist, gun, loweroff, upperoff):
    pass


def print_res(dist, ret, models, spacing=8):
    """
    print a table on stdout showing the error each model has at various
    points to the damage values recorded from the game.
    """
    # the first element of the models array is the exact damage values.
    # we dont want to print the errors for these cuz they are 0.
    calced_models = models[1:]

    # print table headings
    for gun in ret.keys():
        print(f"{gun}")
        print(f"{'dist':>{spacing}}"
              + " ".join([f"{mod:>{spacing}}" for mod in calced_models]))

        # print each row of data
        for i in range(len(dist)):
            model_errs = [f"{ret[gun][f'{mod}_error'][i]:>{spacing}.2f}"
                          for mod in calced_models]
            print(f"{dist[i]:>{spacing}}" + " ".join(model_errs))

        print()
        print("Average error:")
        for mod in calced_models:
            mean_err = np.mean(ret[gun][f'{mod}_error'])
            print(f"{mod}: {mean_err:.2f}%")
        print("----------------------------------------------------------")
        print()


def model_plots(gun_dict, gun_name, models, ax):
    ax.set_title(gun_name)
    for mod in models:
        ax.plot(dist, gun_dict[gun_name][f"{mod}_dam"],
                label=f"{mod} " + gun_name)
    ax.legend(loc="upper right")

    return ax


################################################################
# IF your would like to add another weapon here you must:
#   - add the weapon object as bellow
#   - add a list of real damage values
#   - ensure you add a call for add_g_models
# IF you want to include an additional damage model
#   - simply add it to the existing list 'models'

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

# the first element must be the name of the exact damage values for the guns
# like those given above!
models = ["exact", 'lin', 'bez']
# offset for bezier modelling.
offset = 0.15

g_dict = {}
add_g_models(g_dict, "HK_HB", dist, hk419_rdam, models, HK_HB, offset=offset)
add_g_models(g_dict, "AK_HB", dist, ak74_rdam, models, AK_HB, offset=offset)
add_g_models(g_dict, "MP5", dist, mp5_rdam, models, MP5, offset=offset)

calc_g_per_errors(dist, g_dict, models)
print_res(dist, g_dict, models)

plot = True
if plot:
    fig = plt.figure(figsize=(19.2, 10.8))
    axs = fig.subplots(1, len(g_dict.keys()))

    mod_num = 0
    for key in g_dict.keys():
        axs[mod_num] = model_plots(g_dict, key, models, axs[mod_num])
        mod_num += 1
    plt.show()
