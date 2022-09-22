import argparse
import matplotlib.pyplot as plt
import numpy as np
import weapon_organiser
import file_sys
import man_bit_plot

parser = argparse.ArgumentParser(description="Generate ttk plots for the"
                                 " given weapon and damage types.")
# see note below on why this is commented out
# parser.add_argument('file', type=str,
#                     help="The path to the file containing a dictionary. This"
#                     " dictionary should contain all the weapon property"
#                     " values.")
parser.add_argument('data', type=str,
                    choices=["naked", "ttk_dat", "hb_guns", "barrel_compare"],
                    help="The data to use in the plots.")
parser.add_argument('weapons', type=str, nargs='+',
                    help="The names of weapons or the class of weapons to"
                    " include in the figure.")
parser.add_argument('--dam_type', type=list, nargs='*',
                    default=["ar_dam", "bod_dam"],
                    choices=["ar_dam", "bod_type"],
                    help="The damage type to generate ttk charts for."
                    " 'bod_dam'(body damage) and 'ar_dam'(armour damage) are"
                    " currently supported.")
parser.add_argument('--range', type=tuple, default=(0, 150),
                    help="The range of distance to target values used for the"
                    " charts. This should be a tuple of ints or floats. Note"
                    " that this will also set the x axis range.")
parser.add_argument('--y_lim', type=tuple, default=(100, 900),
                    help="Sets the y axis limits. Set this to None if you want"
                    " matplotlib to do it for you")

parser.add_argument('--fig_size', type=tuple, default=(19.2, 10.8),
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
parser.add_argument('--num_points', type=int, default=200,
                    help="The number of points to use on the charts. A higher"
                    " value will increase the resolution of the lines, so"
                    " increase this if the plot isn't smooth where it should"
                    " curve.")

parser.add_argument('--save', type=str, default=None,
                    help="Where to save the figure. If left empty matplotlib"
                    " will display the graphs in interactive mode.")
args = parser.parse_args()

# pickle is doing weird shit, you will need to work it out
# the values for some weapons were changing, such as the ump45 rof.
# with open(args.file, 'br') as f:
#     arsenal = pickle.load(f)

arsenal = weapon_organiser.get_arsenal(args.data)

valid_weaps, title_list = weapon_organiser.plot_info(args.weapons, arsenal)
if args.dark_mode:
    plt.style.use('dark_background')

figs = []
for dam_type in args.dam_type:
    x = np.linspace(args.range[0], args.range[1], args.num_points)
    y = {}
    fig = plt.figure(tight_layout=True, figsize=args.fig_size)
    for g_type, name in valid_weaps:
        y[name] = np.array([arsenal[g_type][name].ttk(j, dam_type)
                            for j in x])
        plt.plot(x, y[name], label=name, lw=2.5)
    # TODO: put these into rc_params so they aren't being looped over
    plt.legend(loc="lower right", fontsize=args.f_size)
    plt.yticks(fontsize=args.f_size*args.tick_size)
    if args.y_lim is not None:
        plt.ylim(args.y_lim)
    plt.xticks(fontsize=args.f_size*args.tick_size)
    plt.xlabel("Distance to Target (m)", fontsize=args.f_size)
    plt.ylabel("Time to Kill (ms)", fontsize=args.f_size)
    fig_title = man_bit_plot.ttk_plot_title(title_list,
                                            dam_type,
                                            args.fig_name)
    plt.title(fig_title, fontsize=args.f_size)
    figs.append((fig, fig_title))

if args.save is not None:
    path = file_sys.create_path(args.save)
    for figure, title in figs:
        figure.savefig(path + title)
else:
    for figure, title in figs:
        figure.show()
    input()  # hacky way of keeping multiple plots open
