#!/bin/bash

source vir_bat/bin/activate
python plot_obj_ttk.py hb_guns AR --save ./plots/
# decluttered AR plot
python plot_obj_ttk.py ttk_dat M4A1 ACR G36C FAMAS SCAR-H --save ./plots/ --fig_name "Mid Performance ARs"

# SMG
python plot_obj_ttk.py ttk_dat SMG PDW M4A1 --save ./plots/

# best short range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB HONEY_BADGER SCAR-H L86A1_LB MP5 MP7 FAL --save ./plots/ --fig_name "Best Short Range Guns"

# best long range gun in the game
python plot_obj_ttk.py ttk_dat AK74_HB L86A1_LB M4A1 AUG_A3_HB M249 --save ./plots/ --fig_name "Best Long Range Guns"

# starter
python plot_obj_ttk.py ttk_dat M4A1 AK74 AK74_HB AK15 SCAR-H ACR --save ./plots/ --fig_name "Best Starter Guns"

# long and heavy barrel
python plot_obj_ttk.py barrel_compare LMG AR --save ./plots/ --fig_name "Barrel Comparison"
deactivate
