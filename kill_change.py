"""Script to test if a given attachment will change the btk of a weapon."""


import argparse
from pprint import pprint
import preset_arsenals
import gun_obj


def return_synonymous_attachments(attachment):
    """Return a list of attachments that are synonymous with the given name."""
    if attachment == "HeavyBarrel":
        return [gun_obj.HeavyBarrel, gun_obj.Ranger]
    if attachment == "LongBarrel":
        return [gun_obj.LongBarrel]
    return None

def report_btk_change_for_guns(attachments, all_guns):
    """Return a dictionary of bools that is True if btk for the gun changes."""
    ret = {}
    for gun in all_guns:
        before = gun.btk(0, "bod_dam")
        for attach in attachments:
            if attach in gun.val_barrels:
                gun.swap_attach(attach.TYPE, attach)

        after = gun.btk(0, "bod_dam")
        ret[gun.name] = (before != after)
    return ret


parser = argparse.ArgumentParser(description="Determine if the given"
                                 " attachment will change the number of"
                                 " bullets required to kill a target.")
parser.add_argument('attach', type=str, choices=["HeavyBarrel", "LongBarrel"],
                    help="Check if the given attachment will change the ttk"
                    " on any of the guns contained in the file given. Note"
                    " that selecting 'HeavyBarrel' will put the 'Ranger' on"
                    " on those weapons that don't take the heavy.")
args = parser.parse_args()

arsenal = preset_arsenals.ARSENALS["naked"]()
attachments = return_synonymous_attachments(args.attach)

all_guns = arsenal.get_all_guns()
ret = report_btk_change_for_guns(attachments, all_guns)

pprint(ret)
