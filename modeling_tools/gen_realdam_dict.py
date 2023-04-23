"""This module contains functions to generate a dictionary of real damage values.

The damage values are hardcoded and derived by shooting at targets in game.

Functions:
----------
- generate_real_damage_dict: returns a dictionary of real damage values for each
    gun.
"""

import sys


def _damage_is_decreasing(damage_values):
    """Return True if damage values are decreasing, False otherwise."""
    for i in range(len(damage_values) - 1):
        current = damage_values[i]
        next_val = damage_values[i+1]
        if current < next_val:
            return False
    return True

def _find_guns_with_invalid_data(guns, real_damage_key):
    """Returns a list of guns that have invalid data.

    Inputs:
    -------
    - guns: a dictionary of guns with real damage values and distances.
    - real_damage_key: the key used to access the real damage values in the
        guns dictionary.
    """
    invalid_guns = []
    for g_name in guns:
        if len(guns[g_name][real_damage_key]) != len(guns[g_name]["dist"]):
            sys.stderr.write("The number of damage values provided for"
                             f" {g_name} is not the same as the number of"
                             " distance values. This gun will be removed from"
                             " the dictionary.\n")
            invalid_guns.append(g_name)
        if not _damage_is_decreasing(guns[g_name][real_damage_key]):
            sys.stderr.write(f"There is a damage value in the {g_name} list"
                             "that violates decending order. This weapon will"
                             " be removed from the dictionary.\n")
            invalid_guns.append(g_name)
    return invalid_guns

def _delete_guns_with_invalid_data(guns, real_damage_key):
    """Deletes guns with invalid data from the guns dictionary.

    Inputs:
    -------
    - guns: a dictionary of guns with real damage values and distances.
    - real_damage_key: the key used to access the real damage values in the
        guns dictionary.
    """
    invalid_guns = _find_guns_with_invalid_data(guns, real_damage_key)
    for invalid_gun in invalid_guns:
        del guns[invalid_gun]

def generate_real_damage_dict():
    """Return a dictionary of real damage values for each gun.

    The damage values returned by this function are hardcoded and derived by
    shooting at targets in the game.

    Returns:
    --------
    guns:
                                {guns}
                               /      |
                              /        |
                             /          |
                            /            |
               {gun_name}                  {gun_name}
                /      |                    /      |
               /        |                  /        |               ....
            {dist}    {real_damage}     {dist}    {real_damage}
             [int]      [float]          [int]      [float]

    The 'dist' key contains a list of integers representing the range at which
    the damage value was measured at.
    The 'real_damage' key contains a list of floats representing the damage
    values.

    Exceptions:
    ----------
    ValueError: if no valid damage data is provided.
    """
    guns = {}
    # please ensure the keys given here match those in the gen_arsenal module
    # TODO: automate the above
    real_damage_key = "real_damage"
    guns["AK74_HB"] = {}
    guns["AK74_HB"]["dist"] = list(range(50, 301, 10))
    guns["AK74_HB"][real_damage_key] = [36.30, 36.18, 35.84, 35.32, 34.68,
                                        33.81, 32.78, 31.74, 30.54, 29.25,
                                        27.99, 26.49, 25.13, 23.69, 22.35,
                                        20.91, 19.63, 18.34, 17.15, 16.06,
                                        15.11, 14.25, 13.59, 13.12, 12.81,
                                        12.71]
    guns["HK419_HB"] = {}
    guns["HK419_HB"]["dist"] = list(range(50, 301, 10))
    guns["HK419_HB"][real_damage_key] = [34.10, 33.98, 33.67, 33.17, 32.51,
                                         31.76, 30.88, 29.80, 28.70, 27.49,
                                         26.27, 24.96, 23.60, 22.26, 21.02,
                                         19.62, 18.47, 17.39, 16.11, 15.13,
                                         14.23, 13.45, 12.82, 12.33, 12.04,
                                         11.94]
    guns["MP5"] = {}
    guns["MP5"]['dist'] = list(range(50, 301, 10))
    guns["MP5"][real_damage_key] = [26.00, 25.73, 24.97, 23.96, 22.57,
                                    20.87, 19.02, 17.09, 15.27, 13.27,
                                    11.54, 9.88,  8.67,  7.41,  6.73,
                                    6.5,   6.5,   6.5,   6.5,   6.5,
                                    6.5,   6.5,   6.5,   6.5,   6.5,
                                    6.5]

    _delete_guns_with_invalid_data(guns, real_damage_key)
    if len(guns.keys()) < 1:
        raise ValueError("No valid damage data has been provided, exiting")
    return guns
