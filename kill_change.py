import gun_obj
import gen_obj_weap_dat
import argparse
from pprint import pprint


parser = argparse.ArgumentParser(description="Determine if the given"
                                 " attachment will change the number of"
                                 " bullets required to kill a target.")
# parser.add_argument('file', type=str,
#                     help="The path to the file containing a dictionary. This"
#                     " dictionary should contain all the weapon property"
#                     " values. Point to the file containing the weapons with"
#                     " no attachments pls.")
parser.add_argument('data', type=str,
                    choices=["naked", "ttk_dat", "hb_guns", "barrel_compare"],
                    help="The data to use in the plots.")
parser.add_argument('attach', type=str, choices=["HeavyBarrel", "LongBarrel"],
                    help="Check if the given attachment will change the ttk"
                    " on any of the guns contained in the file given. Note"
                    " that selecting 'HeavyBarrel' will put the 'Ranger' on"
                    " on those weapons that don't take the heavy.")
args = parser.parse_args()

# with open(args.file, 'br') as f:
#     arsenal = pickle.load(f)

if args.data == "naked":
    arsenal = gen_obj_weap_dat.naked()
elif args.data == "ttk_dat":
    arsenal = gen_obj_weap_dat.ttk_plot_guns()
elif args.data == "hb_guns":
    arsenal = gen_obj_weap_dat.hb_guns()
elif args.data == "barrel_compare":
    arsenal = gen_obj_weap_dat.barrel_compare()
else:
    raise ValueError

if args.attach == "HeavyBarrel":
    attachments = [gun_obj.HeavyBarrel, gun_obj.Ranger]
elif args.attach == "LongBarrel":
    attachments = [gun_obj.LongBarrel]

ret = {}
for g_type in arsenal:
    for g_name in arsenal[g_type].keys():
        before = arsenal[g_type][g_name].btk(0, "bod_dam")
        for attach in attachments:
            if attach in arsenal[g_type][g_name].val_barrels:
                arsenal[g_type][g_name].swap_attach(attach.TYPE, attach)

        after = arsenal[g_type][g_name].btk(0, "bod_dam")
        ret[g_name] = (before != after)

pprint(ret)
