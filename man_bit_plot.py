"""
    Module containing formatting for battlebit weapon plots.
"""


def ttk_plot_title(title_list, dam_type, fig_name=None, ads_time=False):
    # Return the plot title
    if fig_name is None:
        return ("Time to Kill " + ' '.join(title_list)
                + f" {str_ads(ads_time)}{dam_type}")
    else:
        return ("Time to Kill " + fig_name
                + f" {str_ads(ads_time)}{dam_type}")


def str_ads(x):
    if x:
        return "+ ads "
    else:
        return ""


def inc_ads_time(x, ads_time):
    # Return weap ads time on True
    if x:
        return ads_time
    else:
        return 0
