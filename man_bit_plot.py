"""
    Module containing matplotlib formatting for battlebit weapon plots.
"""


def ttk_plot_title(title_list, dam_type, fig_name=None):
    if fig_name is None:
        fig_title = ' '.join(title_list) + f" Time to Kill {dam_type}"
    else:
        fig_title = fig_name + f" Time to Kill {dam_type}"
    return fig_title
