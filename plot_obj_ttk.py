import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import arsenal
import file_sys
import man_bit_plot
from preset_arsenals import ARSENALS

parser = argparse.ArgumentParser(description="Generate ttk plots for the"
                                 " given weapon and damage types.")
parser.add_argument('data', type=str,
                    choices=list(ARSENALS.keys()),
                    help="The data to use in the plots.")
parser.add_argument('weapons', type=str, nargs='+',
                    help="The names of weapons or the class of weapons to"
                    " include in the figure. See the file 'gen_arsenal' for"
                    " the names of things or to create your own set of guns!")

# data configuration
parser.add_argument('--dam_type', type=list, nargs='*',
                    default=["ar_dam", "bod_dam"],
                    choices=["ar_dam", "bod_type"],
                    help="The damage type to generate ttk charts for."
                    " 'bod_dam'(body damage) and 'ar_dam'(armour damage) are"
                    " currently supported.")
parser.add_argument('--range', type=int, default=[0, 150], nargs='+',
                    help="The range of distance to target values used for the"
                    " charts. Give 2 values with the first being min. Note"
                    " that this will also set the x axis range.")
parser.add_argument("--inc_ads", type=bool, default=False,
                    help="Bool: Include the ads time in the ttk calculation")

# figure customisation
parser.add_argument('--y_lim', type=int, default=[0, 900], nargs='+',
                    help="Sets the y axis limits (min and max). Set this to"
                    " None if you want matplotlib to do it for you")
parser.add_argument('--fig_size', type=float, default=[19.2, 10.8],
                    help="The width and height of the figure. This is inches"
                    " by default. Note that multiplying the numbers here by"
                    " 100 gives an image resolution.")
parser.add_argument('--fig_name', type=str, default=None,
                    help="Set a custom name for the plot(s) generated. Note"
                    " that 'Time to kill [dam_type]' is always suffixed")
parser.add_argument('--dark_mode', type=bool, default=True,
                    help="Use matplotlib dark mode.")
parser.add_argument('--f_size', type=int, default=20,
                    help="This determines the font size used for the figure"
                    " title and axis labels.")
parser.add_argument('--tick_size', type=float, default=0.8,
                    help="The relative axis tick font size compared to the"
                    " given 'f_size'.")
parser.add_argument('--num_points', type=int, default=150,
                    help="The number of points to use on the charts. A higher"
                    " value will increase the resolution of the lines, so"
                    " increase this if the plot isn't smooth where it should"
                    " curve.")

parser.add_argument('--save', type=str, default=None,
                    help="Where to save the figure. If left empty matplotlib"
                    " will display the graphs in interactive mode.")
args = parser.parse_args()

double_val_args = {"fig_size": args.fig_size, "y_lim": args.y_lim,
                   "range": args.range}
for arg_name in double_val_args:
    arg_len = len(double_val_args[arg_name])
    if arg_len != 2:
        raise ValueError(f"argument {arg_name} has {arg_len} values instead of"
                         # TODO magic constant
                         " 2. Please ensure only two values (a min and max)"
                         " are given.")
    if arg_name != "fig_size":
        if double_val_args[arg_name][0] > double_val_args[arg_name][1]:
            raise ValueError(f"argument {arg_name} has a minimum larger than"
                             " or equal to the maximum value. Please ensure"
                             " the second value given to this parameter is"
                             " larger than the first")

arsenal = ARSENALS[args.data]()
valid_weaps, title_list = arsenal.get_guns_or_types_and_return_valid_names(args.weapons)

mpl.rcParams['lines.linewidth'] = 2.5
mpl.rcParams['figure.figsize'] = args.fig_size
mpl.rcParams['xtick.labelsize'] = args.f_size*args.tick_size
mpl.rcParams['ytick.labelsize'] = args.f_size*args.tick_size
mpl.rcParams['axes.titlesize'] = args.f_size
mpl.rcParams['axes.labelsize'] = args.f_size
mpl.rcParams['legend.loc'] = "lower right"
mpl.rcParams['legend.fontsize'] = args.f_size
if args.dark_mode:
    plt.style.use('dark_background')

figs = []
x = np.linspace(args.range[0], args.range[1], args.num_points)
# TODO: Remove dam_type
for dam_type in args.dam_type:
    fig = plt.figure(tight_layout=True)
    for gun in valid_weaps:
        y = np.array(
            [gun.ttk(j, dam_type,
                     inc_ads=args.inc_ads) for j in x])
        plt.plot(x, y, label=gun.name)
    plt.legend()
    if args.y_lim is not None:
        plt.ylim(args.y_lim)
    plt.xlabel("Distance to Target (m)")
    plt.ylabel("Time to Kill (ms)")
    fig_title = man_bit_plot.ttk_plot_title(title_list,
                                            dam_type,
                                            fig_name=args.fig_name,
                                            ads_time=args.inc_ads
                                            )
    plt.title(fig_title)
    figs.append((fig, fig_title))

if args.save is not None:
    path = file_sys.create_path(args.save)
    for figure, title in figs:
        figure.savefig(path + title)
else:
    for figure, title in figs:
        figure.show()
    input()  # hacky way of keeping multiple plots open
