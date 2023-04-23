"""Tests for model_accuracy.py

Run this from the root directory of the project with:
python -m unittest discover -s modeling_tools/tests -p "test_model_accuracy_functions.py"""

import unittest
import sys
import os
# hack to import from the previous directory
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import model_accuracy
import gun_obj


class TestingModelAccuracy(unittest.TestCase):
    def test_remove_guns_from_damage_dict_without_corresponding_gun_obj(self):
        dummy_real_data = {"dist": [1, 2, 3], "real_damage": [1, 2, 3]}
        real_damage_dict = {"AK15": dummy_real_data, "SCAR-H": dummy_real_data}
        gun_objs = [gun_obj.Ak15(), gun_obj.ScarH()]

        guns_that_should_be_present = ["AK15", "SCAR-H"]
        model_accuracy.remove_guns_from_damage_dict_without_corresponding_gun_obj(real_damage_dict, gun_objs)
        self.assertEqual(list(real_damage_dict.keys()), guns_that_should_be_present)
        self.assertEqual([gun.name for gun in gun_objs], guns_that_should_be_present)

        guns_that_should_be_present = ["AK15"]
        gun_objs.pop(1)
        model_accuracy.remove_guns_from_damage_dict_without_corresponding_gun_obj(real_damage_dict, gun_objs)
        self.assertEqual(list(real_damage_dict.keys()), guns_that_should_be_present)
        self.assertEqual([gun.name for gun in gun_objs], guns_that_should_be_present)

        real_damage_dict = {"AK15": dummy_real_data, "SCAR-H": dummy_real_data}
        gun_objs = []
        guns_that_should_be_present = []
        model_accuracy.remove_guns_from_damage_dict_without_corresponding_gun_obj(real_damage_dict, gun_objs)
        self.assertEqual(list(real_damage_dict.keys()), guns_that_should_be_present)
        self.assertEqual([gun.name for gun in gun_objs], guns_that_should_be_present)

    def test_add_modelled_damage_to_dict(self):
        dummy_real_data = {"dist": [1, 2, 3], "real_damage": [1, 2, 3]}
        real_damage_dict = {"AK15": dummy_real_data, "SCAR-H": dummy_real_data}
        gun_objs = [gun_obj.Ak15(), gun_obj.ScarH()]
        model_accuracy.add_modelled_damage_to_dict(real_damage_dict, gun_objs,
                                                     model_name="yes")
        self.assertEqual(list(real_damage_dict.keys()), ["AK15", "SCAR-H"])
        self.assertEqual(list(real_damage_dict["AK15"].keys()),
                         ["dist", "real_damage", "yes"])
        self.assertEqual(list(real_damage_dict["SCAR-H"].keys()),
                         ["dist", "real_damage", "yes"])
        self.assertEqual(len(real_damage_dict["AK15"]["yes"]), 3)
        self.assertEqual(len(real_damage_dict["SCAR-H"]["yes"]), 3)


if __name__ == "__main__":
    unittest.main()