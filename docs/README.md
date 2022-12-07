# battlebit_gun_analysis

This is a command line tool to provide visual representation of weapon ttk at various ranges for the steam multiplayer game Battlebit Remastered.

# Notes on Installing
If you are using python 3.10 you may run into an installation error for the
bezier package. One can get around this by installing the 'pure python version'
as seen on the packages github page:

https://github.com/dhermes/bezier/
$ BEZIER_NO_EXTENSION=true \
>   python   -m pip install --upgrade bezier --no-binary=bezier

# Example Output
![Weapon Time To Kill Plot](./Time%20to%20Kill%20Best%20Short%20Range%20Guns%20%2B%20ads%20bod_dam.png)

# How to Use
Note that there is a shell script that generates the plots for my weapon guide
on steam. If you would like to run the python scripts yourself there is currently:
- plot_obj_ttk.py
- kill_change.py

<br>
<br>

## plot_obj_ttk.py
```
python plot_obj_ttk.py {data} weap1 weap2...
```

The 'data' parameter makes the program use certain weapon data sets defined in gen_obj_weap_data.py.
The data sets themselves consist of the weapons from the game, the attachtments on
them (heavy barrel etc.) and the name the weapon is to be called by when using the
second command line parameter.

The second parameter is either the name of the weapon class type, or the
name of the weapon itself. (again, refer to gen_obj_weap_data.py or the
shell script for the names)

### Example
This will plot all smgs and the M4A1 from the ttk_dat data set and include the ads time in the
ttk calculation 
```
python plot_obj_ttk.py ttk_dat SMG M4A1 --inc_ads True
```

<br>
<br>

## kill_change.py
This is a simple list printing of all the weapons giving true or false if the
designated barrel attatchment changes the number of rounds required to kill a
full hp player.
### Example
```
python kill_change.py HeavyBarrel
```