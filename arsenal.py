"""Arsenal Class Module.

Classes:
--------
Arsenal - A collection of gun objects.
"""

import sys


class Arsenal():
    """A collection of gun objects."""

    def __init__(self, guns=None):
        """Initialize the arsenal."""
        self._fill_rack_with_guns_and_set_num_in_storage(guns)

    def _fill_rack_with_guns_and_set_num_in_storage(self, guns):
        """Fill the gun rack with guns and set the number of guns in storage.

        The resulting gun rack is a dictionary with gun types as keys and
        lists of gun objects as the values.

        Input:
        ------
        guns - iterable of gun objects.

        Raises:
        -------
        TypeError: if guns is not an iterable of gun objects.
        """
        self.num_in_storage = 0
        if guns is None:
            self.gun_rack = None
            return
        try:
            self.gun_rack = {}
            for gun in guns:
                self._add_gun_to_gunrack(gun)
            self.num_in_storage += len(guns)
        except (TypeError, AttributeError) as err:
            self.gun_rack = None
            self.num_in_storage = 0
            raise TypeError("Arsenal.__init__(): guns argument must be"
                            " iterable of gun objects.",
                            file=sys.stderr) from err

    def _add_gun_to_gunrack(self, gun):
        """Add a gun to the gun rack."""
        try:
            self.gun_rack[gun.gun_type].append(gun)
        except KeyError:
            self.gun_rack[gun.gun_type] = [gun]

    def add_gun(self, gun):
        """Add a gun to the arsenal."""
        if self.gun_rack is None:
            self.gun_rack = {}
        self._add_gun_to_gunrack(gun)
        self.num_in_storage += 1

    def remove_gun_obj(self, gun):
        """Remove the given gun object from the arsenal."""
        try:
            self.gun_rack[gun.gun_type].remove(gun)
            self.num_in_storage -= 1
        except KeyError:
            pass
        if self.num_in_storage == 0:
            self.gun_rack = None

    def get_all_gun_types(self):
        """Get the gun types in the arsenal."""
        return list(self.gun_rack.keys())

    def get_all_guns(self):
        """Get all the guns in the arsenal."""
        guns = []
        for gun_type in self.gun_rack:
            guns.extend(self.gun_rack[gun_type])
        return guns

    def get_weapon_by_name(self, gun_name, gun_types_to_skip=None):
        """Get a gun from the arsenal by name."""
        if gun_types_to_skip is None:
            gun_types_to_skip = []

        for gun_type in self.gun_rack:
            if gun_type in gun_types_to_skip:
                continue
            for gun in self.gun_rack[gun_type]:
                if gun_name == gun.name:
                    return gun
        return None

    def _is_gun_type(self, gun_type):
        """Check if the given gun type is in the arsenal."""
        return gun_type in self.gun_rack

    def get_guns_or_types_and_return_valid_names(self, gun_or_type_names):
        """Get all guns that match the given weapon or class names.

        Input:
        ------
        gun_or_class_names - list of str, the names of the guns or gun classes

        Returns:
        --------
        valid_names     - list of str, the names of the guns or gun classes that
                          were found in the arsenal
        guns_to_return  - list of gun objects, the guns that were found in the
                          arsenal
        """
        valid_names = []
        guns_to_return = []
        gun_types_to_skip = []

        for gun_or_type_name in gun_or_type_names:
            if gun_or_type_name in valid_names:
                continue
            if self._is_gun_type(gun_or_type_name):
                guns_to_return.extend(self.gun_rack[gun_or_type_name])
                valid_names.append(gun_or_type_name)
                gun_types_to_skip.append(gun_or_type_name)
                continue

            gun = self.get_weapon_by_name(gun_or_type_name,
                                          gun_types_to_skip=gun_types_to_skip)
            if gun is None:
                continue
            guns_to_return.append(gun)
            valid_names.append(gun_or_type_name)

        return guns_to_return, valid_names
