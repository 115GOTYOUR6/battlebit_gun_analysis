"""Test arsenal.py

Run this from project root via:
python3 -m unittest discover ./tests/ test_arsenal.py
"""

import unittest
import arsenal as ga
import gun_obj


class GenArsenalTesting(unittest.TestCase):
    def test_arsenal__init__(self):
        a = ga.Arsenal()
        self.assertEqual(a.gun_rack, None)
        self.assertEqual(a.num_in_storage, 0)

        gun_list = [gun_obj.Ak15(), gun_obj.ScarH(),
                    gun_obj.Mp5(), gun_obj.Mp7()]
        a = ga.Arsenal(gun_list)
        self.assertEqual(a.gun_rack, {"AR": [gun_obj.Ak15(), gun_obj.ScarH()],
                                      "SMG": [gun_obj.Mp5(), gun_obj.Mp7()]})
        self.assertEqual(a.num_in_storage, len(gun_list))

        with self.assertRaises(TypeError):
            ga.Arsenal(10)

        with self.assertRaises(TypeError):
            ga.Arsenal("not gun objects")

        with self.assertRaises(TypeError):
            ga.Arsenal([gun_obj.Ak15(), 10])

    def test_add_gun(self):
        a = ga.Arsenal()
        a.add_gun(gun_obj.Ak15())
        a.add_gun(gun_obj.ScarH())
        self.assertEqual(a.gun_rack, {"AR": [gun_obj.Ak15(), gun_obj.ScarH()]})
        self.assertEqual(a.num_in_storage, 2)
        a.add_gun(gun_obj.Mp5())
        self.assertEqual(a.gun_rack, {"AR": [gun_obj.Ak15(), gun_obj.ScarH()],
                                      "SMG": [gun_obj.Mp5()]})
        self.assertEqual(a.num_in_storage, 3)

    def test_remove_gun_obj(self):
        gun_list = [gun_obj.Ak15(), gun_obj.ScarH()]
        a = ga.Arsenal(gun_list)
        self.assertEqual(a.gun_rack, {"AR": [gun_list[0], gun_list[1]]})
        self.assertEqual(a.num_in_storage, len(gun_list))
        a.remove_gun_obj(gun_obj.Ak15())
        self.assertEqual(a.gun_rack, {"AR": [gun_list[1]]})
        self.assertEqual(a.num_in_storage, 1)
        a.remove_gun_obj(gun_obj.Mp5())
        self.assertEqual(a.gun_rack, {"AR": [gun_list[1]]})
        self.assertEqual(a.num_in_storage, 1)
        a.remove_gun_obj(gun_obj.ScarH())
        self.assertEqual(a.gun_rack, None)
        self.assertEqual(a.num_in_storage, 0)

    def test_get_weapon_by_name(self):
        gun_list = [gun_obj.Ak15(), gun_obj.ScarH(),
                    gun_obj.Mp5(), gun_obj.Mp7()]
        a = ga.Arsenal(gun_list)
        self.assertEqual(a.get_weapon_by_name("AR"), None)
        self.assertEqual(a.get_weapon_by_name("SCAR-H"), gun_list[1])
        self.assertEqual(a.get_weapon_by_name("MP5"), gun_list[2])
        self.assertEqual(a.get_weapon_by_name("MP5", gun_types_to_skip = ["SMG"]), None)

    def test_get_guns_or_types_and_return_valid_names(self):
        gun_list = [gun_obj.Ak15(), gun_obj.ScarH(),
                    gun_obj.Mp5(), gun_obj.Mp7(),
                    gun_obj.ScarH(gun_name="Patriot")]
        a = ga.Arsenal(gun_list)
        self.assertEqual(a.get_guns_or_types_and_return_valid_names([]), ([], []))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["banana"]), ([], []))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["AR"]), ([gun_list[0], gun_list[1], gun_list[4]], ["AR"]))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["AR", "MP7"]), ([gun_list[0], gun_list[1], gun_list[4], gun_list[3]], ["AR", "MP7"]))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["MP7", "MP7", "SCAR-H"]), ([gun_list[3], gun_list[1]], ["MP7", "SCAR-H"]))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["SMG", "MP7"]), ([gun_list[2], gun_list[3]], ["SMG"]))
        self.assertEqual(a.get_guns_or_types_and_return_valid_names(["Patriot"]), ([gun_list[4]], ["Patriot"]))

if __name__ == "__main__":
    unittest.main()