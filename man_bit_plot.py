"""
    Module containing matplotlib formatting for battlebit weapon plots.
"""

import numpy as np
import bezier


def ttk_plot_title(title_list, dam_type, fig_name=None):
    # Return the plot title
    if fig_name is None:
        fig_title = ' '.join(title_list) + f" Time to Kill {dam_type}"
    else:
        fig_title = fig_name + f" Time to Kill {dam_type}"
    return fig_title


def mid_oneax(x1, x2):
    # find the midpoint along one dimension
    return x1 + (x2 - x1)/2


def gun_bezier(dam_prof):
    # Derive a curve that models the damage drop off for guns
    x_ax_midpoint = mid_oneax(dam_prof[0][0], dam_prof[1][0])
    nodes = np.array([
        [dam_prof[0][0], x_ax_midpoint, x_ax_midpoint, dam_prof[1][0]],
        [dam_prof[0][1], dam_prof[0][1], dam_prof[1][1], dam_prof[1][1]]
    ])

    return bezier.Curve(nodes, degree=3)
