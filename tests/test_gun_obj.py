"""Test gun_obj.py

Run this from project root via:
python3 -m unittest discover ./tests/ test_gun_obj.py
"""

import unittest
from modeling_tools import gen_realdam_dict
import gun_obj
import arsenal
from preset_arsenals import ARSENALS

class TestGunObj(unittest.TestCase):
    def test_gun__init__(self):
        gun = gun_obj.Ak15()
        self.assertEqual(gun.name, "AK15")
        custom_name = "Custom AK15"
        gun = gun_obj.Ak15(custom_name)
        self.assertEqual(gun.name, custom_name)

    def test_gun__str__(self):
        gun = gun_obj.Ak15()
        self.assertEqual(str(gun), "AK15")

        gun = gun_obj.Ak15("Custom AK15")
        self.assertEqual(str(gun), "Custom AK15")

    def test_swap_attach(self):
        gun = gun_obj.Famas()
        self.assertEqual(gun.barrel, gun_obj.EmptyBarrel)

        gun.swap_attach(gun_obj.LongBarrel)
        self.assertEqual(gun.barrel, gun_obj.LongBarrel)

        with self.assertRaises(ValueError):
            gun.swap_attach(gun_obj.HeavyBarrel) # Famas can't take HeavyBarrel

        gun.swap_attach(gun_obj.EmptyBarrel)
        self.assertEqual(gun.barrel, gun_obj.EmptyBarrel)

    def test_gun_damage_changes_after_attaching_barrel(self):
        gun = gun_obj.Ak15()
        self.assertEqual(gun.barrel, gun_obj.EmptyBarrel)

        gun_damage_with_empty_barrel = gun.shot_dam_at_range(0)
        barrel_to_swap = gun_obj.LongBarrel
        gun.swap_attach(barrel_to_swap)
        # I realise I am digging into the implementation details here
        exp_dam = gun_damage_with_empty_barrel * barrel_to_swap._DAM
        self.assertEqual(gun.shot_dam_at_range(0), exp_dam)

        barrel_to_swap = gun_obj.EmptyBarrel
        gun.swap_attach(barrel_to_swap)
        self.assertEqual(gun.shot_dam_at_range(0), gun_damage_with_empty_barrel)

    def test_gun_eq(self):
        gun = gun_obj.Ak15()
        gun2 = gun_obj.Ak15("Custom AK15")
        self.assertEqual(gun, gun2) # name don't matter

        gun2.swap_attach(gun_obj.LongBarrel)
        self.assertNotEqual(gun, gun2)

        gun2.swap_attach(gun_obj.EmptyBarrel)
        self.assertEqual(gun, gun2)

    def get_max_dam_helper(self, gun):
        assert gun.barrel == gun_obj.EmptyBarrel
        # damage points. These are point that are given on the curves in the
        # game that mark the points where the damage either changes or maxes out
        dp1 = gun._dam_prof[0][0]
        dp2 = gun._dam_prof[1][0]
        max_dam = max(dp1, dp2) * gun._dam
        self.assertEqual(max_dam, gun.get_max_dam())

        try:
            gun.swap_attach(gun_obj.LongBarrel)
            long_barrel_dam_scale = gun_obj.LongBarrel._DAM
            dam_with_long_barrel = max_dam * long_barrel_dam_scale
            self.assertEqual(gun.get_max_dam(), dam_with_long_barrel)
        except ValueError:  # gun can't take long barrel so skip
            pass


    def test_get_max_dam(self):
        gun_list = [gun_obj.Ak15(), gun_obj.Famas(), gun_obj.M4a1(),
                    gun_obj.Groza(), gun_obj.Mp5()]
        for gun in gun_list:
            self.get_max_dam_helper(gun)

    def validate_max_min_plateaus(self, gun):
        before_falloff_range = gun._dam_prof[0][0]
        after_falloff_range = gun._dam_prof[1][0]
        min_dam_coeff = gun._dam_prof[1][1]
        min_dam = gun._dam * min_dam_coeff

        # before fall
        for i in range(0, before_falloff_range, 1):
            self.assertEqual(gun.shot_dam_at_range(i), gun._dam)

        # after fall
        mega_range = 10**3
        for i in range(after_falloff_range, mega_range, 1):
            self.assertEqual(gun.shot_dam_at_range(i), min_dam)

    def test_shot_dam_outside_falloff_range(self):
        max_min_plateau_guns = [gun_obj.Ak15(), gun_obj.Famas(), gun_obj.M4a1(),
                                gun_obj.Groza(), gun_obj.Mp5()]
        for gun in max_min_plateau_guns:
            self.validate_max_min_plateaus(gun)

    def test_shot_dam_inside_falloff_range(self):
        real_data = gen_realdam_dict.generate_real_damage_dict()
        arsenal = ARSENALS["ttk_dat"]()
        valid_weaps, title_list = (
            arsenal.get_guns_or_types_and_return_valid_names(list(real_data.keys())))

        # check the predicted damage is acceptably close to the real data
        percentage_error_margin = 0.05
        for gun in valid_weaps:
            for ind, dist in enumerate(real_data[gun.name]["dist"]):
                pred_dam = gun.shot_dam_at_range(dist)
                real_dam = real_data[gun.name]["real_damage"][ind]
                error_margin = percentage_error_margin * real_dam
                if abs(pred_dam - real_dam) > error_margin:
                    raise ValueError(f"Predicted damage {pred_dam} is too far"
                                     f" from real damage {real_dam} for"
                                     f" {gun.name} at range {dist}")


if __name__ == "__main__":
    unittest.main()