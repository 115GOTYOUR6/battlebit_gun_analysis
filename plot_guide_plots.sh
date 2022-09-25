#!/bin/bash

source vir_bat/bin/activate
python plot_obj_ttk.py hb_lb_dat AR --save ./plots/
# decluttered AR plot
python plot_obj_ttk.py ttk_dat M4A1 ACR G36C FAMAS SCAR-H --save ./plots/ --fig_name "Mid Performance ARs"

# SMG
python plot_obj_ttk.py ttk_dat MP7 MP5 PDW M4A1 PP19 --save ./plots/ --fig_name "SMGs PDWs"

# best short range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB HONEY_BADGER L86A1_LB MP5 MP7 FAL HK419 P90 GROZA --save ./plots/ --fig_name "Best Short Range Guns"

# best long range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB L86A1_LB M4A1 AUG_A3_HB M249 SG550 HK419_HB --save ./plots/ --fig_name "Best Long Range Guns"

# starter
python plot_obj_ttk.py ttk_dat M4A1 AK74 AK74_HB AK15 SCAR-H ACR --save ./plots/ --fig_name "Best Starter Guns"

# long and heavy barrel
python plot_obj_ttk.py barrel_compare LMG AR --save ./plots/ --fig_name "Barrel Comparison"
deactivate
