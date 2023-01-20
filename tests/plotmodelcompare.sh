#!/bin/bash

cd ./../
plotsdir=./tests/mod_compare
source vir_bat/bin/activate

# bez
echo bez AR
 time python plot_obj_ttk.py hb_lb_dat AK15 AK74_HB AUG_A3_HB SG550 G36C M4A1 FAL SCAR-H HK419_HB --y_lim 0 1100 --inc_ads True --save $plotsdir/bez/ --fig_name "AR" --model "bez"
 echo bez SMG PDW
 time python plot_obj_ttk.py ttk_dat MP7 MP5 PDW M4A1 PP19 PP2000 UMP-45 --y_lim 0 1100 --inc_ads True --save $plotsdir/bez/ --fig_name "SMGs PDWs" --model "bez"

# cub
echo cub AR
time python plot_obj_ttk.py hb_lb_dat AK15 AK74_HB AUG_A3_HB SG550 G36C M4A1 FAL SCAR-H HK419_HB --y_lim 0 1100 --inc_ads True --save $plotsdir/cub/ --fig_name "AR" --model "cub"
echo cub SMG PDW
time python plot_obj_ttk.py ttk_dat MP7 MP5 PDW M4A1 PP19 PP2000 UMP-45 --y_lim 0 1100 --inc_ads True --save $plotsdir/cub/ --fig_name "SMGs PDWs" --model "cub"
