"""This module provides testing of the ttk_plot_title function in man_bit_plot.py."""

import sys
import os
import unittest
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import man_bit_plot


class PlotTitleTest(unittest.TestCase):
    def test_weap_names(self):
        title_list = ["AK", "M4"]
        dam_type = "bod_dam"
        fig_name = None
        ads_time = False
        ret = man_bit_plot.ttk_plot_title(title_list, dam_type,
                                          fig_name=fig_name, ads_time=ads_time)
        exp = "Time to Kill AK M4 bod_dam"
        self.assertEqual(exp, ret)

    def test_weap_names_and_ads(self):
        title_list = ["AK", "M4"]
        dam_type = "bod_dam"
        fig_name = None
        ads_time = True
        ret = man_bit_plot.ttk_plot_title(title_list, dam_type,
                                          fig_name=fig_name, ads_time=ads_time)
        exp = "Time to Kill AK M4 + ads bod_dam"
        self.assertEqual(exp, ret)

    def test_fig_name(self):
        title_list = ["AK", "M4"]
        dam_type = "bod_dam"
        fig_name = "ARs and stuff"
        ads_time = False
        ret = man_bit_plot.ttk_plot_title(title_list, dam_type,
                                          fig_name=fig_name, ads_time=ads_time)
        exp = "Time to Kill ARs and stuff bod_dam"
        self.assertEqual(exp, ret)

    def test_fig_name_and_ads(self):
        title_list = ["AK", "M4"]
        dam_type = "bod_dam"
        fig_name = "ARs and stuff"
        ads_time = True
        ret = man_bit_plot.ttk_plot_title(title_list, dam_type,
                                          fig_name=fig_name, ads_time=ads_time)
        exp = "Time to Kill ARs and stuff + ads bod_dam"
        self.assertEqual(exp, ret)

if __name__=="__main__":
    unittest.main()