# battlebit_gun_analysis

This is a command line tool to provide visual representation of gun ttk in the steam multiplayer game Battlebit Remastered.

## Notes on Installing
If you are using python 3.10 you may run into an installation error for the
bezier package. One can get around this by installing the 'pure python version'
as seen on the packages github page:

https://github.com/dhermes/bezier/
$ BEZIER_NO_EXTENSION=true \
>   python   -m pip install --upgrade bezier --no-binary=bezier

## Example Usage
Note that there is a shell script that generates the plots for my weapon guide on steam.

python plot_obj_ttk.py {data} weapons...

The 'data' parameter makes the program use certain data sets defined in gen_obj_weap_data.py.
The weapons that are listed afterward are either by name of class type.

There are a number of optional commands that can be viewd on the help page:
"python plot_obj_ttk.py -h"
