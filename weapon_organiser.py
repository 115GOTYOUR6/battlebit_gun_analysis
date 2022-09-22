# Contains all functions that involve the reading in or manipulation of a
# dictionary containing gun objects.

import gen_obj_weap_dat


def get_arsenal(data_type):
    """"""
    if data_type == "naked":
        return gen_obj_weap_dat.naked()
    elif data_type == "ttk_dat":
        return gen_obj_weap_dat.ttk_plot_guns()
    elif data_type == "hb_guns":
        return gen_obj_weap_dat.hb_guns()
    elif data_type == "barrel_compare":
        return gen_obj_weap_dat.barrel_compare()
    else:
        raise ValueError


def plot_info(names, weaps, type_excl=[], name_excl=[]):
    """
    Given the list of names, determine the ones that exist in the weapon data
    and returns the keys to access each of them, along with an appropriate
    string for the plot title.

    Input:
        - names: list of str, either a weapon name or type
        - weaps: nested dict,
                 {{'weapon_type': {'weapon_name':........}},
                  {'weapon_type': {'weapon_name':........}},
                  ...
                 }
    Returns:
        - valid_weaps: list of tuples, each element is (type, name)
        - title_list: list of str, the names given in 'names' that were in the
                      weapon data.
    """
    weap_t_n = tup_2keys(weaps, first_excl=type_excl, sec_excl=name_excl)
    val_weaps = []
    title_list = []
    for name in names:
        if name in weaps.keys():
            val_weaps.extend([j for j in weap_t_n if j[0] == name])
            title_list.append(name)
        elif name in [j[1] for j in weap_t_n]:
            val_weaps.extend([j for j in weap_t_n if j[1] == name])
            title_list.append(name)
        else:
            print(f"Warning, weapon or weapon type '{name}' was not found in"
                  " the data set!")
    return val_weaps, title_list


def tup_2keys(in_dict, first_excl=[], sec_excl=[]):
    """
    Return a list of tuples of 2 keys from a 2 level dictionary (nested dict)

    Input:
        - in_dict: dict of dict
        - first_excl: list, fist level keys to be excluded
        - sec_excl: list, any keys of the nested dictionary to exclude
    Returns:
        - ret: list of tuples
    """
    ret = []
    for first in in_dict.keys():
        for sec in in_dict[first].keys():
            if first not in first_excl and sec not in sec_excl:
                ret.append((first, sec))
    return ret
