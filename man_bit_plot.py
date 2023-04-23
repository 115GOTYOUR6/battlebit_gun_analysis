"""Module containing formatting for battlebit matplotlib weapon figures."""


def ttk_plot_title(title_list, dam_type, fig_name=None, ads_time=False):
    """Return the ttk plot title.

    Inputs:
    -------
    title_list  -- list of strings of weapon names or weapon class names
    dam_type    -- damage type string, either "bod_dam" or "ar_dam"

    Keyword Arguments:
    ------------------
    fig_name    -- figure name string, default None
    ads_time    -- boolean that include '+ ads' in the title, default False
    """
    if fig_name is None:
        return ("Time to Kill " + ' '.join(title_list)
                + f" {str_ads(ads_time)}{dam_type}")
    return ("Time to Kill " + fig_name
            + f" {str_ads(ads_time)}{dam_type}")


def str_ads(include_ads_string):
    """Return string for ads time on True."""
    return "+ ads " if include_ads_string else ""
