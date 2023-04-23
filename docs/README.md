# battlebit_gun_analysis

This is a command line tool to provide a visual representation of weapon time to kill (ttk) at various ranges for the steam multiplayer game Battlebit Remastered.

# Installing

Pip install the required modules from command line.
```
pip install -r requirements.txt
```

# Example Output

![Weapon Time To Kill Plot](./Time%20to%20Kill%20Best%20Short%20Range%20Guns%20%2B%20ads%20bod_dam.png)

# Usage

Note that I wrote a steam guide that uses this project as a means of finding the
best gun in the game. As such I have included the shell script that generates
those plots. It should be called plot_guide_plots.sh or something.

Alternatively if you would like to run the python scripts yourself there is currently:
- plot_obj_ttk.py (Main Script)
- kill_change.py (Tool)
<br>
<br>

## plot_obj_ttk.py (Main Script)

This will plot all smgs and the M4A1 from the ttk_dat data set and include the
ads time in the ttk calculation
```
python plot_obj_ttk.py ttk_dat SMG M4A1 --inc_ads True
```
The weapon class names should be:
- AR
- SMG
- LMG
- PDW
- CARBINE

### Explanation
```
python plot_obj_ttk.py {data} weap1 weap2...
```
[preset_arsenal.py]: ../preset_arsenals.py
The 'data' parameter refers to weapon data sets defined in [preset_arsenal.py].
The data sets themselves consist of the weapons from the game, the attachtments on
them (heavy barrel etc.) and the name the weapon is to be called by when using the
second command line parameter.

The second parameter is either the name of the weapon, or the
name of the weapon class. The weapon class names are hardcoded and can be found
in the [gun_obj.py](../gun_obj.py) module along with the default weapon names.
The weapon names can be, and in some cases are, overwridden when instancing them
in the [preset_arsenal.py] module.

If you want to add your own preset arsenal just make a new function and instance
the gun objects. Don't forget to add it to the ARSENALS constant at the bottom
of the module.
<br>
<br>

## kill_change.py (Tool)

This is a simple list printing of all the weapons giving true or false if the
designated barrel attatchment changes the number of rounds required to kill a
full hp player.
```
python kill_change.py HeavyBarrel
```
