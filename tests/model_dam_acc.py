# testing to make the bezier modelling accurate to the game data.

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from json import load
# hack to import from previous directory
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_arsenal import get_arsenal, find_gclass


def perc_error(approx, exact):
    return abs(approx - exact)/exact*100


def calc_g_perc_errors(dist, g_dict, models):
    """
    Calculate the error each gun in the dict 'g_dict' has relative to the
    exact damage values
    """
    for gun in g_dict.keys():
        for mod in models:
            # skip the first model (exact) as this won't have any error
            # Or like, don't give 'exact' to this function???
            if mod == models[0]:
                continue
            g_dict[gun][f"{mod}_error"] = [
                    perc_error(g_dict[gun][f"{mod}_dam"][i],
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
#   - go to gen_realdam_json.py and add them there. The gun objects will be
#     found and added by this script
# IF you want to include an additional damage model
#   - simply add it to the existing list 'models'

try:
    with open("./realgundam.csv", 'r') as fp:
        realgundict = load(fp)
except FileNotFoundError as e:
    raise FileNotFoundError("Make sure to run gen_realdam_json.py first! \n"
                            f"{e}")
gunstoplot = [i for i in realgundict.keys() if i != 'dist']
dist = realgundict['dist']

# the first element must be the name of the exact damage values for the guns
# like those given above!
models = ["exact", 'lin', 'bez']
# offset for bezier modelling.
offset = 0.15
plot_dict = {}
arsn_dict = get_arsenal('ttk_dat')
for g_name in gunstoplot:
    # gun is the gun object
    gun = arsn_dict[find_gclass(arsn_dict, g_name)][g_name]
    add_g_models(plot_dict, g_name, realgundict['dist'], realgundict[g_name],
                 models, gun, offset=offset)

calc_g_perc_errors(dist, plot_dict, models)
print_res(dist, plot_dict, models)

plot = True
if plot:
    fig = plt.figure(figsize=(19.2, 10.8))
    axs = fig.subplots(1, len(plot_dict.keys()))

    mod_num = 0
    for key in plot_dict.keys():
        axs[mod_num] = model_plots(plot_dict, key, models, axs[mod_num])
        mod_num += 1
    plt.show()
