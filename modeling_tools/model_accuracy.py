"""Report the accuracy of weapon damage models versus real damage values."""


import sys
import os
import matplotlib.pyplot as plt
from gen_realdam_dict import generate_real_damage_dict
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preset_arsenals import ARSENALS


def exit_if_no_gun_objects_returned(gun_objs):
    """Exit if no gun objects are present."""
    if gun_objs == []:
        raise ValueError("Critical Error: The arsenal does not contain any guns.")

def remove_guns_from_damage_dict_without_corresponding_gun_obj(damage_dict,
                                                              gun_objs):
    """Remove real damage data for guns that do not have a corresponding gun object."""
    obj_gun_names = [gun.name for gun in gun_objs]
    names_of_guns_in_damage_dict = list(damage_dict.keys())
    for gun_name in names_of_guns_in_damage_dict:
        if gun_name not in obj_gun_names:
            print(f"Gun object for '{gun_name}' was not retrieved, skipping.",
                  file=sys.stderr)
            damage_dict.pop(gun_name)

def add_modelled_damage_to_dict(damage_dict, gun_objs, model_name="model_damage"):
    """Add calculated damage to the real damage dict."""
    for gun in gun_objs:
        damage_dict[gun.name][model_name] = ([gun.shot_dam_at_range(d)
                                              for d in
                                              damage_dict[gun.name]["dist"]])

def plot_model_vs_real_damage(damage_dict, MODEL_NAME):
    """Plot the model damage versus the real damage."""
    gun_names = list(damage_dict.keys())
    fig, ax = plt.subplots(1, len(gun_names))
    for ind, gun_name in enumerate(gun_names):
        ax[ind].plot(damage_dict[gun_name]["dist"],
                     damage_dict[gun_name]["real_damage"],
                     label="Real Damage")
        ax[ind].plot(damage_dict[gun_name]["dist"],
                     damage_dict[gun_name][MODEL_NAME],
                     label="Model Damage")
        ax[ind].set_title(gun_name)
        ax[ind].set(xlabel="Distance (m)", ylabel="Damage")
        ax[ind].legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    # TODO: make a unittest version of this or something that will check the
    # accuracy of the model.
    damage_dict = generate_real_damage_dict()
    names_of_guns = list(damage_dict.keys())
    arsenal = ARSENALS["ttk_dat"]()
    gun_objs, valid_names = arsenal.get_guns_or_types_and_return_valid_names(names_of_guns)

    exit_if_no_gun_objects_returned(gun_objs)
    remove_guns_from_damage_dict_without_corresponding_gun_obj(damage_dict,
                                                               gun_objs)
    MODEL_NAME = "model_damage"
    add_modelled_damage_to_dict(damage_dict, gun_objs,
                                model_name=MODEL_NAME)
    plot_model_vs_real_damage(damage_dict, MODEL_NAME)
