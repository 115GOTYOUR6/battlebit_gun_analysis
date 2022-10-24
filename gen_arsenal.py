# Contains functions that generate dictionaries of gun objects


import gun_obj


def get_arsenal(data_type):
    """
    Get the arsenal data via string.

    Input:
    data_type -- str, returns an arsenal with the name given. There are only
    certain names that are valid:
    'naked' # no attachments
    'ttk_dat'
    'hb_lb_dat' # includes heavy and long barrel with the naked gun being
    removed
    'barrel_compare' # only has guns affected by long or heavy barrel
    """
    if data_type == "naked":
        return naked()
    elif data_type == "ttk_dat":
        return ttk_plot_guns()
    elif data_type == "hb_lb_dat":
        return hb_lb_dat()
    elif data_type == "barrel_compare":
        return barrel_compare()
    else:
        raise ValueError


def bez_expr_key(dam_prof, offset):
    # make keys for expr_dict from damage profile and offset used in the
    # creation of the expression
    return " ".join([str(dam_prof[0][0]), str(dam_prof[1][0]),
                     str(dam_prof[0][1]), str(offset)])


def bez_expressions(arsenal, weaps, offset):
    """
    Store expressions for the bezier curves used in the weapon damage
    falloff calculations for every unique damage profile in the given
    arsenal.

    Input:
    arsenal -- dict, contains gun objects and is structured like so
    arsenal[gun_type][gun_name]
    weaps -- list of tuples containing the weapon type and name. These should
    match the keys in the arsenal.
    offset -- float, the offset used in the generation of the gun bezier curve

    Return:
    expr_dict -- dict, structed as expr_dict[expr_key]. This holds sympy
    expressions
    """
    expr_dict = {}
    for g_type, g_name in weaps:
        gun = arsenal[g_type][g_name]
        key = bez_expr_key(gun.dam_prof, offset)
        expr_dict[key] = gun.gen_bez_curve(offset).implicitize()

    return expr_dict


def naked():
    g_types = ["AR", "LMG", "SMG", "PDW", "CARBINE"]

    guns = {}
    for gun_type in g_types:
        guns[gun_type] = {}

    guns["AR"]["AK74"] = gun_obj.Ak74()
    guns["AR"]["M4A1"] = gun_obj.M4a1()
    guns["AR"]["AK15"] = gun_obj.Ak15()
    guns["AR"]["SCAR-H"] = gun_obj.ScarH()
    guns["AR"]["ACR"] = gun_obj.Acr()
    guns["AR"]["AUG_A3"] = gun_obj.AugA3()
    guns["AR"]["SG550"] = gun_obj.Sg550()
    guns["AR"]["FAL"] = gun_obj.Fal()
    guns["AR"]["G36C"] = gun_obj.G36c()
    guns["AR"]["FAMAS"] = gun_obj.Famas()
    guns["AR"]["HK419"] = gun_obj.Hk419()

    guns["LMG"]["L86A1"] = gun_obj.L86a1()
    guns["LMG"]["M249"] = gun_obj.M249()

    guns["SMG"]["MP7"] = gun_obj.Mp7()
    guns["SMG"]["UMP-45"] = gun_obj.Ump45()
    guns["SMG"]["PP2000"] = gun_obj.Pp2000()
    guns["SMG"]["KRISS_VECTOR"] = gun_obj.KrissVector()
    guns["SMG"]["MP5"] = gun_obj.Mp5()
    guns["SMG"]["PP19"] = gun_obj.Pp19()

    guns["PDW"]["HONEY_BADGER"] = gun_obj.HoneyBadger()
    guns["PDW"]["P90"] = gun_obj.P90()
    guns["PDW"]["GROZA"] = gun_obj.Groza()

    guns["CARBINE"]["AS_VAL"] = gun_obj.AsVal()
    return guns


def ttk_plot_guns():
    guns = naked()

    guns["AR"]["AUG_A3_HB"] = gun_obj.AugA3()
    guns["AR"]["AK74_HB"] = gun_obj.Ak74()
    guns["AR"]["L86A1_LB"] = gun_obj.L86a1()
    guns["AR"]["HK419_HB"] = gun_obj.Hk419()

    guns["AR"]["AUG_A3_HB"].swap_barrel(gun_obj.HeavyBarrel)
    guns["AR"]["AK74_HB"].swap_barrel(gun_obj.HeavyBarrel)
    guns["AR"]["L86A1_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["AR"]["HK419_HB"].swap_barrel(gun_obj.HeavyBarrel)
    return guns


def hb_lb_dat():
    guns = naked()

    guns["LMG"].pop("L86A1")
    guns["AR"].pop("AUG_A3")
    guns["AR"].pop("AK74")
    guns["AR"].pop("HK419")

    guns["LMG"]["L86A1_LB"] = gun_obj.L86a1()
    guns["AR"]["AUG_A3_HB"] = gun_obj.AugA3()
    guns["AR"]["AK74_HB"] = gun_obj.Ak74()
    guns["AR"]["HK419_HB"] = gun_obj.Hk419()

    guns["LMG"]["L86A1_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["AR"]["AUG_A3_HB"].swap_barrel(gun_obj.HeavyBarrel)
    guns["AR"]["AK74_HB"].swap_barrel(gun_obj.HeavyBarrel)
    guns["AR"]["HK419_HB"].swap_barrel(gun_obj.HeavyBarrel)
    return guns


def barrel_compare():

    # guns = naked()

    # guns["AR"].pop("AK74")
    # guns["LMG"].pop("L86A1")
    guns = {}
    guns["AR"] = {}
    guns["LMG"] = {}

    guns["AR"]["AK74"] = gun_obj.Ak74()
    guns["AR"]["AK74_LB"] = gun_obj.Ak74()
    guns["AR"]["AK74_HB"] = gun_obj.Ak74()
    guns["AR"]["AK74_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["AR"]["AK74_HB"].swap_barrel(gun_obj.HeavyBarrel)

    guns["LMG"]["L86A1"] = gun_obj.L86a1()
    guns["LMG"]["L86A1_LB"] = gun_obj.L86a1()
    guns["LMG"]["L86A1_HB"] = gun_obj.L86a1()
    guns["LMG"]["L86A1_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["LMG"]["L86A1_HB"].swap_barrel(gun_obj.HeavyBarrel)

    guns["AR"]["AUG_A3"] = gun_obj.AugA3()
    guns["AR"]["AUG_A3_HB"] = gun_obj.AugA3()
    guns["AR"]["AUG_A3_HB"].swap_barrel(gun_obj.HeavyBarrel)

    guns["AR"]["HK419"] = gun_obj.Hk419()
    guns["AR"]["HK419_HB"] = gun_obj.Hk419()
    guns["AR"]["HK419_HB"].swap_barrel(gun_obj.HeavyBarrel)

    return guns


# guns = naked()
# with open("./obj_weap_data.txt", 'bw') as f:
#     pickle.dump(guns, f)
#
# guns = ttk_plot_guns()
# with open("./obj_ttk_guide_weap_data.txt", 'bw') as f:
#     pickle.dump(guns, f)
#
# guns = hb_guns()
# with open("./obj_hb_weap_data.txt", 'bw') as f:
#     pickle.dump(guns, f)
#
# guns = barrel_compare()
# with open("./obj_barrel_compare.txt", 'bw') as f:
#     pickle.dump(guns, f)
