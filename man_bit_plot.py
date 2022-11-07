"""
    Module containing formatting for battlebit weapon plots.
"""


def ttk_plot_title(title_list, dam_type, fig_name=None, ads_time=False):
    # Return the plot title
    if fig_name is None:
        return (f"Time to Kill {str_ads(ads_time)}{dam_type} "
                + ' '.join(title_list))
    else:
        return f"Time to Kill {str_ads(ads_time)}{dam_type} " + fig_name


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
