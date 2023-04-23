"""Premade arsenals for use in the main program.

Functions:
----------
make_naked_arsenal()                    - return arsenal with no attachments.
make_ttk_plot_arsenal()                 - return arsenal with guns that are used
                                          in the TTK plots.
make_heavy_barrel_long_barrel_arsenal() - return arsenal with only one of each
                                          weapon with weapons that
                                          benifit from having a heavy or long
                                          barrel equipped.
make_barrel_compare_arsenal() - return arsenal only with guns that are affected
                                heavy or long barrel. All possible combinations
                                that result in different TTKs are included.
"""


from arsenal import Arsenal
import gun_obj

def make_naked_arsenal():
    """Return an arsenal with all guns with no attachments."""
    gun_list = []

    gun_list.append(gun_obj.Ak74())
    gun_list.append(gun_obj.M4a1())
    gun_list.append(gun_obj.Ak15())
    gun_list.append(gun_obj.ScarH())
    gun_list.append(gun_obj.Acr())
    gun_list.append(gun_obj.AugA3())
    gun_list.append(gun_obj.Sg550())
    gun_list.append(gun_obj.Fal())
    gun_list.append(gun_obj.G36c())
    gun_list.append(gun_obj.Famas())
    gun_list.append(gun_obj.Hk419())

    gun_list.append(gun_obj.L86a1())
    gun_list.append(gun_obj.M249())

    gun_list.append(gun_obj.Mp7())
    gun_list.append(gun_obj.Ump45())
    gun_list.append(gun_obj.Pp2000())
    gun_list.append(gun_obj.KrissVector())
    gun_list.append(gun_obj.Mp5())
    gun_list.append(gun_obj.Pp19())

    gun_list.append(gun_obj.HoneyBadger())
    gun_list.append(gun_obj.P90())
    gun_list.append(gun_obj.Groza())

    gun_list.append(gun_obj.AsVal())

    return Arsenal(guns=gun_list)

def make_ttk_plot_arsenal():
    """Return an arsenal with guns that are used in the TTK plots."""
    a = make_naked_arsenal()

    # TODO: function...
    weap = gun_obj.Ak74(gun_name="AK74_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.AugA3(gun_name="AUG_A3_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.Hk419(gun_name="HK419_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.L86a1(gun_name="L86A1_LB")
    weap.swap_barrel(gun_obj.LongBarrel)
    a.add_gun(weap)

    return a

def make_heavy_barrel_long_barrel_arsenal():
    """Return an arsenal with naked or barrel swapped guns."""

    a = make_naked_arsenal()

    a.remove_gun_obj(gun_obj.Ak74())
    a.remove_gun_obj(gun_obj.AugA3())
    a.remove_gun_obj(gun_obj.L86a1())
    a.remove_gun_obj(gun_obj.Hk419())

    weap = gun_obj.Ak74(gun_name="AK74_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.AugA3(gun_name="AUG_A3_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.Hk419(gun_name="HK419_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    a.add_gun(weap)
    weap = gun_obj.L86a1(gun_name="L86A1_LB")
    weap.swap_barrel(gun_obj.LongBarrel)
    a.add_gun(weap)

    return a

def make_barrel_compare_arsenal():
    """Return an arsenal only of the guns that are affected by heavy or long barrel."""

    gun_list = []

    gun_list.append(gun_obj.Ak74())
    weap = gun_obj.Ak74(gun_name="AK74_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    gun_list.append(weap)
    weap = gun_obj.Ak74(gun_name="AK74_LB")
    weap.swap_barrel(gun_obj.LongBarrel)
    gun_list.append(weap)

    gun_list.append(gun_obj.AugA3())
    weap = gun_obj.AugA3(gun_name="AUG_A3_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    gun_list.append(weap)

    gun_list.append(gun_obj.L86a1())
    weap = gun_obj.L86a1(gun_name="L86A1_LB")
    weap.swap_barrel(gun_obj.LongBarrel)
    gun_list.append(weap)
    weap = gun_obj.L86a1(gun_name="L86A1_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    gun_list.append(weap)

    gun_list.append(gun_obj.Hk419())
    weap = gun_obj.Hk419(gun_name="HK419_HB")
    weap.swap_barrel(gun_obj.HeavyBarrel)
    gun_list.append(weap)

    return Arsenal(guns=gun_list)

ARSENALS = {"naked": make_naked_arsenal,
            "ttk_dat": make_ttk_plot_arsenal,
            "hb_lb_dat": make_heavy_barrel_long_barrel_arsenal,
            "barrel_compare": make_barrel_compare_arsenal}
