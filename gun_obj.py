"""
    Contains class definitions for each weapon in the game and functions that
    calculate various things including shot damage at a given range, ttk etc.

    Classes:
        Ak74
        M4a1
        Ak15
        ScarH
        Acr
        AugA3
        Sg550
        Fal
        G36c
        Famas
        Hk419
        L86a1
        M249
        Mp7
        Ump-45
        Pp2000
        KrissVector
        Mp5
        Pp19
        HoneyBadger
        P90
        Groza
        AsVal
"""

import numpy as np
from math import ceil

import bezier
import sympy

import gen_arsenal


def offset_oneax(x1, x2, offset):
    # find the midpoint along one dimension
    return x1 + (x2 - x1)/2 + (x2 - x1)*offset


def dp3(x):
    temp = int(x*10000)
    if temp % 10 >= 5:
        return (int(temp/10)+1) / 1000
    else:
        return int(temp/10) / 1000


###################################################
# attachments
# additions to these require the val_x arrays (list of valid attatchments for
# weapons) in the weapon type classes to be updated if they are able to be
# attached.
class Attachment():
    # Contains multipliers that modify a weapons corresponding base stat. This
    # is an abstract class
    _BOD_DAM = 1
    _AR_DAM = 1
    _VELOCITY = 1
    _ROF = 1
    _AIM_DOWN = 1

    def __str__(self):
        return self.NAME


# Barrels
class Barrel(Attachment):
    TYPE = "barrel"


class HeavyBarrel(Barrel):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "HeavyBarrel"
    _BOD_DAM = 1.1
    _AR_DAM = 1.1
    _VELOCITY = 1.1


class LongBarrel(Barrel):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "LongBarrel"
    _BOD_DAM = 1.05
    _AR_DAM = 1.1
    _VELOCITY = 1.1


class Ranger(Barrel):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Ranger"
    _BOD_DAM = 1.1
    _AR_DAM = 1.1
    _VELOCITY = 1.1


class EmptyBarrel(Barrel):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


# Sights
class Sight(Attachment):
    TYPE = "sight"


class EmptySight(Sight):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


# Canted Sights
class CSight(Attachment):
    TYPE = "c_sight"


class EmptyCSight(CSight):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


# Magazines
class Mag(Attachment):
    TYPE = "mag"


class EmptyMag(Mag):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


# Underbarrel
class URail(Attachment):
    TYPE = "u_rail"


class EmptyURail(URail):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


# Side rail
class SRail(Attachment):
    TYPE = "s_rail"


class EmptySRail(SRail):
    """
    Data class that contains multipliers used in manipulating gun stats when
    attached.
    """
    NAME = "Empty"


###################################################
# weapons
class Gun(object):
    # Abstract class that provides methods for calculating various weapon
    # characteristics
    def __init__(self):
        """Initialise all attachment slots with empty attachment classes"""
        self.sight = EmptySight
        self.c_sight = EmptyCSight
        self.mag = EmptyMag
        self.s_rail = EmptySRail
        self.u_rail = EmptyURail
        self.barrel = EmptyBarrel

    def get_dam(self, dam_type):
        """Return the gun's base damage.

        If you want the damage the gun will do at a given range,
        see 'shot_dam'.

        dam_type - string: either 'bod_dam' for body damage or 'ar_dam' for
                   armour damage.
        """
        # This getter exists on account of the potential for the base damage
        # of the weapon to be determined by having the attachments modify the
        # instance damage directly (current) or by having this method determine
        # the damage by checking for attachments that change it and leaving
        # the instance damage alone
        #
        # yes, I dislike getters so much I am justifying making one here
        if dam_type == "bod_dam":
            return self._bod_dam
        elif dam_type == "ar_dam":
            return self._ar_dam
        else:
            return None

    def _gen_bez_curve(self, offset=0.15):
        # Generate a curve that models the damage drop off for guns
        # Input:
        #     - offset, float: parameter determines the offset of the middle
        #                      bezier control points from the center of the
        #                      domain:
        #
        #   |
        #   |                       . P1
        #   |
        #   |
        #   |
        #   |                       . P2
        #   |_______________________ _______________________
        #   |                       |                      |
        # self._dam_prof[0][0]    center           self._dam_prof[1][0]
        #
        #
        #                              |
        #                              |
        #                              V
        #
        #   |
        #   |                   . P1
        #   |
        #   |
        #   |                       ____| offset
        #   |                       |   . P2
        #   |_______________________|_______________________
        #   |                       |                      |
        # self._dam_prof[0][0]    center           self._dam_prof[1][0]
        #

        # x_ax_midpoint = offset_oneax(self._dam_prof[0][0],
        #                              self._dam_prof[1][0],
        #                              0)
        nodes = np.array([
            [self._dam_prof[0][0],
             offset_oneax(self._dam_prof[0][0], self._dam_prof[1][0],
                          -1*offset),
             offset_oneax(self._dam_prof[0][0], self._dam_prof[1][0], offset),
             self._dam_prof[1][0]],
            [self._dam_prof[0][1],
             self._dam_prof[0][1],
             self._dam_prof[1][1],
             self._dam_prof[1][1]]
        ])

        return bezier.Curve(nodes, degree=3)

    def _falloff_coef(self, dist, model='cub',
                      bez_exprs={}, offset=0.15):
        # Return the damage coefficient for a distance within the falloff range
        # of weapons based on the given damage model
        if model == 'lin':
            coef = self._lin_coef(dist)
        elif model == 'bez':
            coef = self._bez_coef(dist, offset=offset, bez_exprs=bez_exprs)
        elif model == 'cub':
            coef = self._cubic_coef(dist)
        else:
            print("Warning! falloff_coef received an unknown model type."
                  " Defaulting to bezier model")
            coef = self._bez_coef(dist, offset=offset, bez_exprs=bez_exprs)
        return coef

    def _lin_coef(self, dist):
        # return the damage coeficient in the drop off range using linear model
        grad = ((self._dam_prof[1][1] - self._dam_prof[0][1])
                / (self._dam_prof[1][0] - self._dam_prof[0][0]))
        return grad * (dist - self._dam_prof[0][0]) + 1

    def _bez_coef(self, dist, bez_exprs={}, offset=0.15):
        # return the damage coeficient in the drop off range using bezier model
        key = gen_arsenal.bez_expr_key(self._dam_prof, offset)
        if key in bez_exprs:
            expr = bez_exprs[key]
        else:
            curve = self._gen_bez_curve(offset)
            expr = curve.implicitize()

        coef, = sympy.solveset(expr.evalf(subs={'x': dist}), 'y',
                               sympy.Interval(0, 1))
        return coef

    def _cubic_coef(self, dist):
        # The damage coefficient function here runs from x=0 to x=250. Thus,
        # we must offset the falloff distance to x=0 for the gun by subtracting
        # its starting falloff value
        dist -= self._dam_prof[0][0]

        # because we go from 0 to 250, any guns that have a shorter falloff
        # interval will require the domain of the cubic func to be scaled
        xcalcedrange = [50, 300]  # this is the domain of the cubic regression
        xrange = [m for m, n in self._dam_prof]  # falloff interval for gun
        xscale = (xcalcedrange[1] - xcalcedrange[0])/(xrange[1] - xrange[0])

        # the y axis may also need scaling depending on _MIN_CO
        ycalcedrange = 0.35
        yrange = self._MIN_CO  # 0.25 for smgs
        # this is derived from a simultanous equation:
        # f(250)*m + c = 0.25
        # f(0)*m + c = 1
        yscale = (yrange - 1)/(ycalcedrange - 1)  # this is m
        coef = (8.353*10**(-8)*(xscale*dist)**3
                - 3.119*10**(-5)*(xscale*dist)**2
                - 2.281*10**(-5)*(xscale*dist)
                + 1)
        #        m    * f(x) + (   c    )
        return yscale * coef + 1 - yscale

    def shot_dam(self, dist, dam_type, model='cub', bez_exprs={}, offset=0.15):
        """
        Returns the damage a bullet will do at the given distance.

        dist - distance to the target, positive value
        dam_type - string, the damage type 'bod_dam' for body damage, 'ar_dam'
                   for armour damage

        Keyword Arguments:
        model -- the damage model type to use, 'bez' or 'lin'. (default 'bez')
        bez_exprs -- dictionary of previously generated bezier model curves.
                     Only used for bezier model. (default {})
        offset -- offset for the bezier damage model. (default 0.15)
        """
        dam = self.get_dam(dam_type)
        if dist <= self._dam_prof[0][0]:
            return dam * self._dam_prof[0][1]
        elif dist >= self._dam_prof[1][0]:
            return self._dam_prof[1][1] * dam
        else:
            dam_coef = self._falloff_coef(dist, model=model,
                                          bez_exprs=bez_exprs, offset=offset)
            return dam * dam_coef

    def btk(self, dist, dam_type, model='cub', bez_exprs={}, offset=0.15):
        """
        Return the number of hits needed to kill a target from full health at
        the given distance.

        dist - distance to the target, positive value
        dam_type - string, the damage type 'bod_dam' for body damage, 'ar_dam'
                   for armour damage

        Keyword Arguments:
        model -- the damage model type to use, 'bez' or 'lin'. (default 'bez')
        bez_exprs -- dictionary of previously generated bezier model curves.
                     Only used for bezier model. (default {})
        offset -- offset for the bezier damage model. (default 0.15)
        """
        return ceil(100/self.shot_dam(dist, dam_type, model=model,
                    bez_exprs=bez_exprs, offset=offset))

    def ttk(self, dist, dam_type, model='cub', bez_exprs={}, offset=0.15,
            inc_ads=False):
        """
        Returns the time to kill a full health opponent.

        dist - distance to the target, positive value
        dam_type - string, the damage type 'bod_dam' for body damage, 'ar_dam'
                   for armour damage

        Keyword Arguments:
        model -- the damage model type to use, 'bez' or 'lin'. (default 'bez')
        bez_exprs -- dictionary of previously generated bezier model curves.
                     Only used for bezier model. (default {})
        offset -- offset for the bezier damage model. (default 0.15)
        inc_ads -- Whether to include ads time in the calculation or not
                   (default False)
        """
        # minus 1 to btk because the first shot is in the air at t = 0
        # thus, there are btk - 1 times the rof delays the kill
        shoot_time = (1/self.rof * 60000
                      * (self.btk(dist,
                                  dam_type,
                                  model=model,
                                  bez_exprs=bez_exprs) - 1))
        tof = dist/self.velocity*1000
        ads_time = self.aim_down if inc_ads else 0

        return shoot_time + tof + ads_time*1000

    def get_attachments(self):
        """
        Return the name of each attachments on the gun as a dictionary.
        """
        return {"sight": self.sight.NAME, "c_sight": self.c_sight.NAME,
                "mag": self.mag.NAME, "s_rail": self.s_rail.NAME,
                "u_rail": self.u_rail.NAME, "barrel": self.barrel.NAME}

    def _apply_attach(self, attachment):
        # apply the attachment to the weapon
        self._bod_dam = dp3(self._bod_dam * attachment._BOD_DAM)
        self._ar_dam = dp3(self._ar_dam * attachment._AR_DAM)
        self.velocity = dp3(self.velocity * attachment._VELOCITY)
        self.rof = dp3(self.rof * attachment._ROF)
        self.aim_down = dp3(self.aim_down * attachment._AIM_DOWN)

    def _remove_attach(self, attachment):
        # removes the attachment from the weapon
        self._bod_dam = dp3(self._bod_dam / attachment._BOD_DAM)
        self._ar_dam = dp3(self._ar_dam / attachment._AR_DAM)
        self.velocity = dp3(self.velocity / attachment._VELOCITY)
        self.rof = dp3(self.rof / attachment._ROF)
        self.aim_down = dp3(self.aim_down / attachment._AIM_DOWN)

    def swap_sight(self, attachment):
        """Swap the gun's current sight out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptySight'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_sights
                     class variable
        """
        if attachment not in self.val_sights:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.sight != attachment:
            self._remove_attach(self.sight)
            self._apply_attach(attachment)
            self.sight = attachment

    def swap_c_sight(self, attachment):
        """Swap the gun's current canted sight out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyCSight'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_c_sights
                     class variable
        """
        if attachment not in self.val_c_sights:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.c_sight != attachment:
            self._remove_attach(self.c_sight)
            self._apply_attach(attachment)
            self.c_sight = attachment

    def swap_mag(self, attachment):
        """Swap the gun's current magazine out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyMag'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_mags
                     class variable
        """
        if attachment not in self.val_mags:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.mag != attachment:
            self._remove_attach(self.mag)
            self._apply_attach(attachment)
            self.mag = attachment

    def swap_s_rail(self, attachment):
        """Swap the gun's side rail attachment out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptySRail'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_s_rails
                     class variable
        """
        if attachment not in self.val_s_rails:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.s_rail != attachment:
            self._remove_attach(self.s_rail)
            self._apply_attach(attachment)
            self.s_rail = attachment

    def swap_u_rail(self, attachment):
        """Swap the gun's current under rail out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyURail'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_u_rails
                     class variable
        """
        if attachment not in self.val_u_rails:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.u_rail != attachment:
            self._remove_attach(self.u_rail)
            self._apply_attach(attachment)
            self.u_rail = attachment

    def swap_barrel(self, attachment):
        """Swap the gun's current barrel out for the given one.

        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyBarrel'.

        Raises:
        ValueError - if the given attachment isn't in the gun's val_barrels
                     class variable
        """
        if attachment not in self.val_barrels:
            raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.barrel != attachment:
            self._remove_attach(self.barrel)
            self._apply_attach(attachment)
            self.barrel = attachment

    def swap_attach(self, slot, attachment):
        """Change the attachment in the slot given to the one given.

        slot       - str, the part of the gun the attachment is to go on.
        attachment - attachment class object eg: 'EmptyBarrel'
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
    # AR Weapon category to be inherited by weapon classes
    _HEAD_MULT = 1.5
    # this is the minimum damage co-efficient ie: mindamage/basedamage
    _MIN_CO = 0.35

    def __init__(self):
        # carry over all instance variables that will appear in weapon objects
        # that inherit from this class
        super().__init__()
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Lmg(Gun):
    # LMG Weapon category to be inherited by weapon classes
    _HEAD_MULT = 1.5
    _MIN_CO = 0.3

    def __init__(self):
        # carry over all instance variables that will appear in weapon objects
        # that inherit from this class
        super().__init__()
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Smg(Gun):
    # SMG Weapon category to be inherited by weapon classes
    _HEAD_MULT = 1.2
    _MIN_CO = 0.25

    def __init__(self):
        # carry over all instance variables that will appear in weapon objects
        # that inherit from this class
        super().__init__()
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Pdw(Gun):
    # PDW Weapon category to be inherited by weapon classes
    _HEAD_MULT = 1.5
    _MIN_CO = 0.25

    def __init__(self):
        # carry over all instance variables that will appear in weapon objects
        # that inherit from this class
        super().__init__()
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Carbine(Gun):
    # CARBINE Weapon category to be inherited by weapon classes
    _HEAD_MULT = 1.5
    _MIN_CO = 0.25

    def __init__(self):
        # carry over all instance variables that will appear in weapon objects
        # that inherit from this class
        super().__init__()
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


###############################################################
# Weapon definitions
# additions here need to be added to the arsenal generation functions too if
# they are to be used in the main scripts.

class Ak74(Ar):
    """Simulates AK74 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 33
        self._ar_dam = 33
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 670
        self.velocity = 700
        self.aim_down = 0.25


class M4a1(Ar):
    """Simulates M4A1 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 30
        self._ar_dam = 30
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 700
        self.aim_down = 0.24


class Ak15(Ar):
    """Simulates AK15 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 40
        self._ar_dam = 40
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 540
        self.velocity = 750
        self.aim_down = 0.3


class ScarH(Ar):
    """Simulates SCARH weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 42
        self._ar_dam = 42
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 500
        self.velocity = 750
        self.aim_down = 0.2


class Acr(Ar):
    """Simulates ACR weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 25
        self._ar_dam = 30
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 650
        self.aim_down = 0.25


class AugA3(Ar):
    """Simulates AUGA3 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 31
        self._ar_dam = 35
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 500
        self.velocity = 600
        self.aim_down = 0.15


class Sg550(Ar):
    """Simulates SG550 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 27
        self._ar_dam = 27
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 640
        self.aim_down = 0.14


class Fal(Ar):
    """Simulates FAL weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 40
        self._ar_dam = 30
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 650
        self.velocity = 600
        self.aim_down = 0.22


class G36c(Ar):
    """Simulates G36C weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self.val_barrels = np.array([Ranger, LongBarrel])
        self._bod_dam = 30
        self._ar_dam = 25
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 750
        self.velocity = 600
        self.aim_down = 0.25


class Famas(Ar):
    """Simulates FAMAS weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self.val_barrels = np.array([Ranger, LongBarrel])
        self._bod_dam = 23
        self._ar_dam = 23
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 900
        self.velocity = 600
        self.aim_down = 0.25


class Hk419(Ar):
    """Simulates HK419 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 31
        self._ar_dam = 31
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 660
        self.velocity = 700
        self.aim_down = 0.25


########################################################################
# LMG
class L86a1(Lmg):
    """Simulates L86A1 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 32
        self._ar_dam = 36
        self._dam_prof = [(100, 1), (300, self._MIN_CO)]
        self.rof = 775
        self.velocity = 600
        self.aim_down = 0.3


class M249(Lmg):
    """Simulates M249 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 30
        self._ar_dam = 50
        self._dam_prof = [(100, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 600
        self.aim_down = 0.35


########################################################################
# SMG
class Mp7(Smg):
    """Simulates MP7 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 25
        self._ar_dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 950
        self.velocity = 350
        self.aim_down = 0.15


class Ump45(Smg):
    """Simulates UMP45 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 25
        self._ar_dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 700
        self.velocity = 500
        self.aim_down = 0.2


class Pp2000(Smg):
    """Simulates PP2000 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 23
        self._ar_dam = 23
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 900
        self.velocity = 350
        self.aim_down = 0.2


class KrissVector(Smg):
    """Simulates KRISSVECTOR weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 24
        self._ar_dam = 24
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 1200
        self.velocity = 400
        self.aim_down = 0.25


class Mp5(Smg):
    """Simulates MP5 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 26
        self._ar_dam = 26
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 400
        self.aim_down = 0.2


class Pp19(Smg):
    """Simulates PP19 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self.val_barrels = np.array([])
        self._bod_dam = 25
        self._ar_dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 750
        self.velocity = 400
        self.aim_down = 0.20


###################################################################
# PDW
class HoneyBadger(Pdw):
    """Simulates HONEYBADGER weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 35
        self._ar_dam = 35
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2


class P90(Pdw):
    """Simulates P90 weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 28
        self._ar_dam = 28
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 390
        self.aim_down = 0.2


class Groza(Pdw):
    """Simulates GROZA weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 27
        self._ar_dam = 34
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 700
        self.velocity = 390
        self.aim_down = 0.2


######################################################################
# Carbine
class AsVal(Carbine):
    """Simulates ASVAL weapon characteristics.

    Instance Variables:
        sight   - sight attachment the gun has
        c_sight - the canted sight attachment the gun has
        mag     - magazine attachment the gun has
        s_rail  - side rail attachment the gun has
        u_rail  - under rail attachment the gun has
        barrel  - barrel attachment the gun has
        val_barrels  - valid barrel attachments
        val_sights   - valid sight attachments
        val_c_sights - valid canted sight attachments
        val_mags     - valid magazine attachments
        val_s_rails  - valid side rail attachments
        val_u_rails  - valid under rail attachments
        self.rof      - rate of fire
        self.velocity - bullet velocity
        self.aim_down - time it takes to ads

    Functions:
        get_dam - return the damage
        shot_dam - return the damage the gun does at the given range
        btk - return the bullets to kill a full health target at a given range
        ttk - return the time to kill a full health target at the given range
        get_attachments - return a dictionary containing the names of the
            attachments in each slot
        swap_attach - swap the the attachment in the given slot to the one
            given
        swap_barrel - swap the barrel to the given one
        swap_c_sight - swap the canted sight to the given one
        swap_mag - swap the magazine to the given one
        swap_s_rail - swap the side rail to the given one
        swap_sight - swap the sight to the given one
        swap_u_rail - swap the under rail to the given one
    """
    def __init__(self):
        super().__init__()
        self._bod_dam = 35
        self._ar_dam = 35
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2
