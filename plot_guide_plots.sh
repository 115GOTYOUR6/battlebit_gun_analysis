#!/bin/bash

source vir_bat/bin/activate
python plot_obj_ttk.py hb_lb_dat AK15 AK74_HB AUG_A3_HB SG550 G36C M4A1 FAL SCAR-H HK419_HB --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "AR"
python plot_obj_ttk.py hb_lb_dat AK15 AK74_HB AUG_A3_HB SG550 G36C M4A1 FAL SCAR-H HK419_HB --y_lim 0 1100 --save ./plots/ --fig_name "AR"
# decluttered AR plot
python plot_obj_ttk.py ttk_dat M4A1 ACR G36C FAMAS SCAR-H SG550 --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "Mid Performance ARs"
python plot_obj_ttk.py ttk_dat M4A1 ACR G36C FAMAS SCAR-H SG550 --y_lim 0 1100 --save ./plots/ --fig_name "Mid Performance ARs"

# SMG
python plot_obj_ttk.py ttk_dat MP7 MP5 PDW M4A1 PP19 PP2000 UMP-45 --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "SMGs PDWs"
python plot_obj_ttk.py ttk_dat MP7 MP5 PDW M4A1 PP19 PP2000 UMP-45 --y_lim 0 1100 --save ./plots/ --fig_name "SMGs PDWs"

# best short range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB HONEY_BADGER L86A1_LB MP5 MP7 FAL HK419_HB P90 GROZA --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "Best Short Range Guns"
python plot_obj_ttk.py ttk_dat AK74_HB HONEY_BADGER L86A1_LB MP5 MP7 FAL HK419_HB P90 GROZA --y_lim 0 1100 --save ./plots/ --fig_name "Best Short Range Guns"

# best long range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB M4A1 AUG_A3_HB M249 SG550 HK419_HB --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "Best Long Range Guns"
python plot_obj_ttk.py ttk_dat AK74_HB M4A1 AUG_A3_HB M249 SG550 HK419_HB --y_lim 0 1100 --save ./plots/ --fig_name "Best Long Range Guns"

# starter
python plot_obj_ttk.py ttk_dat M4A1 AK74 AK74_HB AK15 SCAR-H ACR --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "Best Starter Guns"
python plot_obj_ttk.py ttk_dat M4A1 AK74 AK74_HB AK15 SCAR-H ACR --y_lim 0 1100 --save ./plots/ --fig_name "Best Starter Guns"

# long and heavy barrel
python plot_obj_ttk.py barrel_compare LMG AR --y_lim 0 1100 --inc_ads True --save ./plots/ --fig_name "Barrel Comparison"
python plot_obj_ttk.py barrel_compare LMG AR --y_lim 0 1100 --save ./plots/ --fig_name "Barrel Comparison"
deactivate
