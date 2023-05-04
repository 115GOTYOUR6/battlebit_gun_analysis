"""Module containing formatting for battlebit matplotlib weapon figures."""

def ttk_plot_title(title_list, fig_name=None, ads_time=False):
    """Return the ttk plot title.

    Inputs:
    -------
    title_list  -- list of strings of weapon names or weapon class names

    Keyword Arguments:
    ------------------
    fig_name    -- figure name string, default None. This is automatically
                   prefixed by 'Time to Kill'
    ads_time    -- boolean, determines whether or not a string, indicating that
                   ads times have factored into the ttk calculations, will be
                   included in the plot title.
    """
    ads_string = " + ADS Time" if ads_time else ""
    if fig_name is None:
        return ("Time to Kill " + ' '.join(title_list)
                + f"{ads_string}")
    return ("Time to Kill " + fig_name
            + f"{ads_string}")