# Contains functions that generate dictionaries of gun objects


import gun_obj


def naked():
    g_types = {}
    g_types["AR"] = ["ACR", "AK15", "AK74", "G36C", "M4A1", "SCAR-H", "AUG_A3",
                     "FAL", "FAMAS"]
    g_types["CARBINE"] = ["AS_VAL"]
    g_types["PDW"] = ["HONEY_BADGER"]
    g_types["LMG"] = ["L86A1", "M249"]
    g_types["SMG"] = ["KRISS_VECTOR", "MP7", "PP2000", "UMP-45", "MP5"]

    guns = {}
    for i in g_types.keys():
        guns[i] = {}
        for j in g_types[i]:
            guns[i][j] = {}

    guns["AR"]["AK74"] = gun_obj.Ak74()
    guns["AR"]["M4A1"] = gun_obj.M4a1()
    guns["AR"]["AK15"] = gun_obj.Ak15()
    guns["AR"]["SCAR-H"] = gun_obj.ScarH()
    guns["AR"]["ACR"] = gun_obj.Acr()
    guns["AR"]["AUG_A3"] = gun_obj.AugA3()
    guns["AR"]["SG550"] = gun_obj.Sg550()
    guns["AR"]["FAL"] = gun_obj.Fal()
    guns["AR"]["PP19"] = gun_obj.Pp19()
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

    guns["LMG"]["L86A1"] = gun_obj.L86a1()
    guns["LMG"]["L86A1_LB"] = gun_obj.L86a1()
    guns["LMG"]["L86A1_HB"] = gun_obj.L86a1()

    guns["AR"]["AUG_A3"] = gun_obj.AugA3()
    guns["AR"]["AUG_A3_HB"] = gun_obj.AugA3()

    guns["AR"]["AK74_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["AR"]["AK74_HB"].swap_barrel(gun_obj.HeavyBarrel)

    guns["AR"]["AUG_A3_HB"].swap_barrel(gun_obj.HeavyBarrel)

    guns["LMG"]["L86A1_LB"].swap_barrel(gun_obj.LongBarrel)
    guns["LMG"]["L86A1_HB"].swap_barrel(gun_obj.HeavyBarrel)

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
