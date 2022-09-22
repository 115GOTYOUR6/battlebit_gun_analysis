"""
    Contains class definitions for each weapon in the game and functions that
    calculate various things including shot damage at a given range, ttk etc.
"""

import numpy as np
from math import ceil


def dp3(x):
    temp = int(x*10000)
    if temp % 10 >= 5:
        return (int(temp/10)+1) / 1000
    else:
        return int(temp/10) / 1000


###################################################
# attachments
# additions to these require the val_x arrays (list of valid attatchments for
# weapons) in the weapon type classes to be updated if they are to be attached.
class Attachment():
    BOD_DAM = 1
    AR_DAM = 1
    VELOCITY = 1
    ROF = 1
    AIM_DOWN = 1

    def __str__(self):
        return self.NAME


# Barrels
class Barrel(Attachment):
    TYPE = "barrel"


class HeavyBarrel(Barrel):
    """Provides multiplyers for gun stats as per the Heavy Barrel in game"""
    NAME = "HeavyBarrel"
    BOD_DAM = 1.1
    AR_DAM = 1.1
    VELOCITY = 1.1


class LongBarrel(Barrel):
    """Provides multiplyers for gun stats as per the Long Barrel in game"""
    NAME = "LongBarrel"
    BOD_DAM = 1.05
    AR_DAM = 1.1
    VELOCITY = 1.1


class Ranger(Barrel):
    """Provides multiplyers for gun stats as per the Ranger Barrel in game"""
    NAME = "Ranger"
    BOD_DAM = 1.1
    AR_DAM = 1.1
    VELOCITY = 1.1


class EmptyBarrel(Barrel):
    """Provides multiplyers for gun stats as per the Empty Barrel in game"""
    NAME = "Empty"


# Sights
class Sight(Attachment):
    TYPE = "sight"


class EmptySight(Sight):
    NAME = "Empty"


# Canted Sights
class CSight(Attachment):
    TYPE = "c_sight"


class EmptyCSight(CSight):
    NAME = "Empty"


# Magazines
class Mag(Attachment):
    TYPE = "mag"


class EmptyMag(Mag):
    NAME = "Empty"


# Underbarrel
class URail(Attachment):
    TYPE = "u_rail"


class EmptyURail(URail):
    NAME = "Empty"


# Side rail
class SRail(Attachment):
    TYPE = "s_rail"


class EmptySRail(SRail):
    NAME = "Empty"


###################################################
# weapons
class Gun(object):
    def __init__(self):
        self.sight = EmptySight
        self.c_sight = EmptyCSight
        self.mag = EmptyMag
        self.s_rail = EmptySRail
        self.u_rail = EmptyURail
        self.barrel = EmptyBarrel

    def get_dam(self, dam_type):
        if dam_type == "bod_dam":
            return self.bod_dam
        elif dam_type == "ar_dam":
            return self.ar_dam
        else:
            return None

    def shot_dam(self, dist, dam_type):
        """
        Returns the damage a bullet will do at the given distance.
        """
        dam = self.get_dam(dam_type)
        if dist <= self.dam_prof[0][1]:
            return dam
        elif dist >= self.dam_prof[1][1]:
            return self.dam_prof[1][0] * dam
        else:
            grad = ((self.dam_prof[1][0] - self.dam_prof[0][0])
                    / (self.dam_prof[1][1] - self.dam_prof[0][1]))
            return dam * (grad * (dist - self.dam_prof[0][1]) + 1)

    def btk(self, dist, dam_type):
        """
        Return the number of hits needed to kill a target at the given
        distance.
        """
        return ceil(100/self.shot_dam(dist, dam_type))

    def ttk(self, dist, dam_type):
        """
        Returns the time to kill a full health opponent.
        """
        # minus 1 to btk because the first shot is in the air at t = 0
        # thus, there are btk - 1 times the rof delays the kill
        shoot_time = 1/self.rof*60000 * (self.btk(dist, dam_type) - 1)
        tof = dist/self.velocity*1000
        return shoot_time + tof

    def get_attachments(self):
        """
        Return the attachments on the gun as a dictionary.
        """
        return {"sight": self.sight.NAME, "c_sight": self.c_sight.NAME,
                "mag": self.mag.NAME, "s_rail": self.s_rail.NAME,
                "u_rail": self.u_rail.NAME, "barrel": self.barrel.NAME}

    def apply_attach(self, attachment):
        self.bod_dam = dp3(self.bod_dam * attachment.BOD_DAM)
        self.ar_dam = dp3(self.ar_dam * attachment.AR_DAM)
        self.velocity = dp3(self.velocity * attachment.VELOCITY)
        self.rof = dp3(self.rof * attachment.ROF)
        self.aim_down = dp3(self.aim_down * attachment.AIM_DOWN)

    def remove_attach(self, attachment):
        self.bod_dam = dp3(self.bod_dam / attachment.BOD_DAM)
        self.ar_dam = dp3(self.ar_dam / attachment.AR_DAM)
        self.velocity = dp3(self.velocity / attachment.VELOCITY)
        self.rof = dp3(self.rof / attachment.ROF)
        self.aim_down = dp3(self.aim_down / attachment.AIM_DOWN)

    def swap_sight(self, attachment):
        if attachment not in self.val_sights:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.sight != attachment:
            self.remove_attach(self.sight)
            self.apply_attach(attachment)
            self.sight = attachment

    def swap_c_sight(self, attachment):
        if attachment not in self.val_c_sights:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.c_sight != attachment:
            self.remove_attach(self.c_sight)
            self.apply_attach(attachment)
            self.c_sight = attachment

    def swap_mag(self, attachment):
        if attachment not in self.val_mags:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.mag != attachment:
            self.remove_attach(self.mag)
            self.apply_attach(attachment)
            self.mag = attachment

    def swap_s_rail(self, attachment):
        if attachment not in self.val_s_rails:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.s_rail != attachment:
            self.remove_attach(self.s_rail)
            self.apply_attach(attachment)
            self.s_rail = attachment

    def swap_u_rail(self, attachment):
        if attachment not in self.val_u_rails:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.u_rail != attachment:
            self.remove_attach(self.u_rail)
            self.apply_attach(attachment)
            self.u_rail = attachment

    def swap_barrel(self, attachment):
        if attachment not in self.val_barrels:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.barrel != attachment:
            self.remove_attach(self.barrel)
            self.apply_attach(attachment)
            self.barrel = attachment

    def swap_attach(self, slot, attachment):
        """
        Add an attachment to the given slot.

        Input:
            - slot: str, the part of the gun the attachment is to go on.
            - attachment: cust obj
        """
        if slot == "barrel":
            self.swap_barrel(attachment)
        elif slot == "u_rail":
            self.swap_u_rail(attachment)
        elif slot == "s_rail":
            self.swap_s_rail(attachment)
        elif slot == "mag":
            self.swap_mag(attachment)
        elif slot == "c_sight":
            self.swap_c_sight(attachment)
        elif slot == "sight":
            self.swap_sight(attachment)


################################################################
# weapon classes
class Ar(Gun):
    HEAD_MULT = 1.5
    MIN_CO = 0.35

    def __init__(self):
        Gun.__init__(self)
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Lmg(Gun):
    HEAD_MULT = 1.5
    MIN_CO = 0.3

    def __init__(self):
        Gun.__init__(self)
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Smg(Gun):
    HEAD_MULT = 1.2
    MIN_CO = 0.25

    def __init__(self):
        Gun.__init__(self)
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Pdw(Gun):
    HEAD_MULT = 1.5
    MIN_CO = 0.25

    def __init__(self):
        Gun.__init__(self)
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Carbine(Gun):
    HEAD_MULT = 1.5
    MIN_CO = 0.25

    def __init__(self):
        Gun.__init__(self)
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


###############################################################
# Weapon definitions
# additions here need to be added to the data generation functions too.

class Acr(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 25
        self.ar_dam = 30
        self.dam_prof = [(1, 50), (self.MIN_CO, 300)]
        self.rof = 700
        self.velocity = 650
        self.aim_down = 0.25


class Ak15(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 40
        self.ar_dam = 40
        self.dam_prof = [(1, 150), (self.MIN_CO, 300)]
        self.rof = 540
        self.velocity = 750
        self.aim_down = 0.3


class Ak74(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 33
        self.ar_dam = 33
        self.dam_prof = [(1, 50), (self.MIN_CO, 300)]
        self.rof = 670
        self.velocity = 700
        self.aim_down = 0.25


class G36c(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.val_barrels = np.array([Ranger, LongBarrel])
        self.bod_dam = 30
        self.ar_dam = 25
        self.dam_prof = [(1, 50), (self.MIN_CO, 300)]
        self.rof = 750
        self.velocity = 600
        self.aim_down = 0.25


class M4a1(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 30
        self.ar_dam = 30
        self.dam_prof = [(1, 50), (self.MIN_CO, 300)]
        self.rof = 700
        self.velocity = 700
        self.aim_down = 0.24


class ScarH(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 42
        self.ar_dam = 42
        self.dam_prof = [(1, 150), (self.MIN_CO, 300)]
        self.rof = 500
        self.velocity = 750
        self.aim_down = 0.2


class AugA3(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 31
        self.ar_dam = 35
        self.dam_prof = [(1, 150), (self.MIN_CO, 300)]
        self.rof = 500
        self.velocity = 600
        self.aim_down = 0.15


class Fal(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.bod_dam = 40
        self.ar_dam = 30
        self.dam_prof = [(1, 150), (self.MIN_CO, 300)]
        self.rof = 650
        self.velocity = 600
        self.aim_down = 0.22


class Famas(Ar):
    def __init__(self):
        Ar.__init__(self)
        self.val_barrels = np.array([Ranger, LongBarrel])
        self.bod_dam = 23
        self.ar_dam = 23
        self.dam_prof = [(1, 50), (self.MIN_CO, 300)]
        self.rof = 900
        self.velocity = 600
        self.aim_down = 0.25


########################################################################
# LMG
class L86a1(Lmg):
    def __init__(self):
        Lmg.__init__(self)
        self.bod_dam = 32
        self.ar_dam = 36
        self.dam_prof = [(1, 100), (self.MIN_CO, 300)]
        self.rof = 775
        self.velocity = 600
        self.aim_down = 0.3


class M249(Lmg):
    def __init__(self):
        Lmg.__init__(self)
        self.bod_dam = 30
        self.ar_dam = 50
        self.dam_prof = [(1, 100), (self.MIN_CO, 300)]
        self.rof = 700
        self.velocity = 600
        self.aim_down = 0.35


########################################################################
# SMG
class KrissVector(Smg):
    def __init__(self):
        Smg.__init__(self)
        self.bod_dam = 24
        self.ar_dam = 24
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 1200
        self.velocity = 400
        self.aim_down = 0.25


class Mp7(Smg):
    def __init__(self):
        Smg.__init__(self)
        self.bod_dam = 25
        self.ar_dam = 25
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 950
        self.velocity = 350
        self.aim_down = 0.15


class Pp2000(Smg):
    def __init__(self):
        Smg.__init__(self)
        self.bod_dam = 23
        self.ar_dam = 23
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 900
        self.velocity = 350
        self.aim_down = 0.2


class Ump45(Smg):
    def __init__(self):
        Smg.__init__(self)
        self.bod_dam = 25
        self.ar_dam = 25
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 700
        self.velocity = 500
        self.aim_down = 0.2


class Mp5(Smg):
    def __init__(self):
        Smg.__init__(self)
        self.bod_dam = 26
        self.ar_dam = 26
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 800
        self.velocity = 400
        self.aim_down = 0.2


###################################################################
# PDW

class HoneyBadger(Pdw):
    def __init__(self):
        Pdw.__init__(self)
        self.bod_dam = 35
        self.ar_dam = 35
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2


class P90(Pdw):
    def __init__(self):
        Pdw.__init__(self)
        self.bod_dam = 28
        self.ar_dam = 28
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 800
        self.velocity = 390
        self.aim_down = 0.2


######################################################################
# Carbine
class AsVal(Carbine):
    def __init__(self):
        Carbine.__init__(self)
        self.bod_dam = 35
        self.ar_dam = 35
        self.dam_prof = [(1, 50), (self.MIN_CO, 200)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2
