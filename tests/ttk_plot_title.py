import sys
import os
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import man_bit_plot


def test_check(exp, ret):
    if exp != ret:
        print("Failure")
        print(exp)
        print(ret)
    else:
        print("Success")
        print(exp)

    print("---------------------------------------------")
    print()


title_list = ["AK", "M4"]
dam_type = "bod_dam"
fig_name = None
ads_time = False
ret = man_bit_plot.ttk_plot_title(title_list, dam_type, fig_name=fig_name,
                                  ads_time=ads_time)
exp = "Time to Kill bod_dam AK M4"
test_check(exp, ret)
# -------------------------------------------------------------
title_list = ["AK", "M4"]
dam_type = "bod_dam"
fig_name = None
ads_time = True
ret = man_bit_plot.ttk_plot_title(title_list, dam_type, fig_name=fig_name,
                                  ads_time=ads_time)
exp = "Time to Kill + ads bod_dam AK M4"
test_check(exp, ret)
# -------------------------------------------------------------
title_list = ["AK", "M4"]
dam_type = "bod_dam"
fig_name = "AR"
ads_time = False
ret = man_bit_plot.ttk_plot_title(title_list, dam_type, fig_name=fig_name,
                                  ads_time=ads_time)
exp = "Time to Kill bod_dam AR"
test_check(exp, ret)
# -------------------------------------------------------------
title_list = ["AK", "M4"]
dam_type = "bod_dam"
fig_name = "AR"
ads_time = True
ret = man_bit_plot.ttk_plot_title(title_list, dam_type, fig_name=fig_name,
                                  ads_time=ads_time)
exp = "Time to Kill + ads bod_dam AR"
test_check(exp, ret)
# -------------------------------------------------------------
