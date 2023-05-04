"""
    Contains class definitions for each weapon in the game and functions that
    calculate various things including shot damage at a given range, ttk etc.

    The following gun objects are defined:
        ARs:
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
        LMGs:
            L86a1
            M249
        SMGs:
            Mp7
            Ump-45
            Pp2000
            KrissVector
            Mp5
            Pp19
        PDWs:
            HoneyBadger
            P90
            Groza
        Carbines:
            AsVal
"""


from math import ceil
import numpy as np


# additions to these require the val_x arrays (list of valid attatchments for
# weapons) in the weapon type classes to be updated if they are able to be
# attached.
class AttachmentBaseClass():
    """Base class for all attachments."""
    _DAM = 1
    _VELOCITY = 1
    _ROF = 1
    _AIM_DOWN = 1

    def __str__(self):
        return self.NAME


class BarrelBaseClass(AttachmentBaseClass):
    """Base class for barrel attachments."""
    TYPE = "barrel"


class HeavyBarrel(BarrelBaseClass):
    """Heavy barrel attachment."""
    NAME = "HeavyBarrel"
    _DAM = 1.1
    _VELOCITY = 1.1


class LongBarrel(BarrelBaseClass):
    """
    Long barrel attachment.
    """
    NAME = "LongBarrel"
    _DAM = 1.05
    _VELOCITY = 1.1


class Ranger(BarrelBaseClass):
    """Ranger barrel attachment."""
    NAME = "Ranger"
    _DAM = 1.1
    _VELOCITY = 1.1


class EmptyBarrel(BarrelBaseClass):
    """Empty barrel attachment."""
    NAME = "Empty"


class SightBaseClass(AttachmentBaseClass):
    """Base class for sight attachments."""
    TYPE = "sight"


class EmptySight(SightBaseClass):
    """Empty sight attachment."""
    NAME = "Empty"


class CSightBaseClass(AttachmentBaseClass):
    """Base class for canted sight attachments."""
    TYPE = "c_sight"


class EmptyCSight(CSightBaseClass):
    """Empty canted sight attachment."""
    NAME = "Empty"


class MagBaseClass(AttachmentBaseClass):
    """Base class for magazine attachments."""
    TYPE = "mag"


class EmptyMag(MagBaseClass):
    """Empty magazine attachment."""
    NAME = "Empty"


class URailBaseClass(AttachmentBaseClass):
    """Base class for under rail attachments."""
    TYPE = "u_rail"


class EmptyURail(URailBaseClass):
    """Empty under rail attachment."""
    NAME = "Empty"


class SRailBaseClass(AttachmentBaseClass):
    """Base class for side rail attachments."""
    TYPE = "s_rail"


class EmptySRail(SRailBaseClass):
    """Empty side rail attachment."""
    NAME = "Empty"


class Gun():
    """
    Abstract class that provides methods for calculating weapon damage etc.

    Instance Variables:
    -------------------
    sight   - SightBaseClass: the sight attached to the gun
    c_sight - CSightBaseClass: the canted sight attached to the gun
    mag     - MagBaseClass: the magazine attached to the gun
    s_rail  - SRailBaseClass: the side rail attached to the gun
    u_rail  - URailBaseClass: the under rail attached to the gun
    barrel  - BarrelBaseClass: the barrel attached to the gun

    Functions:
    ----------
    - get_dam: returns the base damage of the weapon for the given damage type
    - shot_dam: returns the damage the gun will do at a given range
    - btk: returns the number of shots required to kill a target
    - ttk: returns the time it takes to kill a target
    - get_attachments: returns a dict of all attachments attached to the gun
    """
    def __init__(self):
        """Initialise all attachment slots with empty attachment classes"""
        # TODO: make the attachments a set of objects. We can then initialise
        # here with at single parameter.
        self.sight = EmptySight
        self.c_sight = EmptyCSight
        self.mag = EmptyMag
        self.s_rail = EmptySRail
        self.u_rail = EmptyURail
        self.barrel = EmptyBarrel

    def __eq__(self, other):
        """Return True if gun attachments and stats are the same."""
        if (self.sight == other.sight and self.c_sight == other.c_sight
            and self.mag == other.mag and self.s_rail == other.s_rail
            and self.u_rail == other.u_rail and self.barrel == other.barrel
            and self._dam == other._dam
            and self.rof and self._dam_prof == other._dam_prof and self.velocity
            and self.aim_down):
            return True
        return False

    def __str__(self):
        return self.name

    def get_max_dam(self, dec_places=3):
        """Return the gun's highest damage, regardless of the range this occurs at.

        If you want the damage the gun will do at a given range, see 'shot_dam'.

        Returns:
        --------
        float: the max damage of the gun.
        """
        # This getter exists on account of the potential for the base damage
        # of the weapon to be determined by having the attachments modify the
        # instance damage directly (current) or by having this method determine
        # the damage by checking for attachments that change it and leaving
        # the instance damage alone
        #
        # yes, I dislike getters so much I am justifying making one here
        max_coef = max(self._dam_prof[0][0], self._dam_prof[1][0])
        return round(max_coef * self._dam, dec_places)

    def _calc_falloff_coef(self, dist):
        """Return the falloff range damage coeficient using cubic model.

        Input:
        ------
        dist - float: the distance from the shooter to the target. The value
               given is assumed to be in the guns falloff range.
        """
        if self._dam_prof[1][0] < dist < self._dam_prof[0][0]:
            raise ValueError("_calc_fallof_coef: "
                             "Distance is not in the falloff range of the gun")
        # here is an essay on how this was derived.
        # Guns in the game have a damage falloff curve. The curve is generally
        # cubic and where it is not, this function must be overridden.
        # Observing the curves lead me to discover that the minimum damage a gun
        # does (the bottom point of the curve) is a percentage of the base
        # damage. Thus, we can easily generalise to calculate damage by using
        # a scaling coefficient beginning at 1 for the start of the falloff
        # range, and ending at the minimum coeficient (0.25 for eg).
        # This fuction estimates that coefficient for any given distance inside
        # the falloff range.

        # To get a function we can take some real data from the game
        # (by shooting a gun) and recording the damage values from the start
        # of the falloff to the end. dividing by the guns damage yields a
        # set of coefficients.The problem
        # is that the gun we choose likely has a fallof domain
        # (end dist - start dist) or minimum coefficient that isn't the same
        # for all guns. To make it work for them, the domain and range of the
        # function must be scaled to fit the gun we are estimating for.

        # Gun 1 falloff (master)    Gun 2 falloff (some gun with more range)
        # |                         |
        # |-- . p1                  |-----. p1
        # |  (fancy curve)          |   (fancy curve)
        # |      p2 .-------        |
        # |                         |               p2 .-------
        # ---------------------     -------------------------
        #
        # The equation for gun 1 will not generalise to 2; it has a longer
        # falloff domain and lower minimum coefficient.
        # So we stretch the domain and range of the cubic regression to fit

        # The damage coefficient function here was derived from a cubic regression
        # done from x=0 to x=250. Thus, we must offset the falloff distance to
        # x=0 for the gun by subtracting its starting falloff value
        dist -= self._dam_prof[0][0]

        # because we go from 0 to 250, any guns that have a shorter falloff
        # interval will require the domain of the cubic func to be scaled
        xcalcedrange = [50, 300]  # this is the domain of the cubic regression
        xrange = [m for m, n in self._dam_prof]  # falloff interval for gun
        xscale = (xcalcedrange[1] - xcalcedrange[0])/(xrange[1] - xrange[0])

        # the y axis may also need scaling depending on _MIN_CO
        # So I wrote what follows a while ago, and I can't work out y it works
        # anymore...

        # this is derived from a simultanous equation:
        # f(250)*m + c = 0.25 (250 being the end of regressed gun's donmain and
        #                      0.25 being the gun's minimum coefficient)
        # f(0)*m + c = 1
        ycalcedmin = 0.35
        ymin = self._MIN_CO
        yscale = (ymin - 1)/(ycalcedmin - 1)  # this is m
        # see polyfit_real.py for the derivation of the cubic regression
        coef = (8.353*10**(-8)*(xscale*dist)**3
                - 3.119*10**(-5)*(xscale*dist)**2
                - 2.281*10**(-5)*(xscale*dist)
                + 1)
        #        m    * f(x) + (   c    )
        return yscale * coef + 1 - yscale

    def shot_dam_at_range(self, dist):
        """Returns the damage a bullet will do at the given distance.

        Inputs:
        -------
        dist     - distance to the target, positive value, meters

        Returns:
        --------
        float: the damage the bullet will do at the given distance
        """
        dam = self._dam
        assert dist >= 0
        if dist <= self._dam_prof[0][0]:
            return dam * self._dam_prof[0][1]
        if dist >= self._dam_prof[1][0]:
            return self._dam_prof[1][1] * dam

        dam_coef = self._calc_falloff_coef(dist)
        return dam * dam_coef

    def btk(self, dist):
        """Return the number of hits needed to kill at the given distance."""
        return ceil(100/self.shot_dam_at_range(dist))

    def ttk(self, dist, inc_ads=False):
        """Returns the time to kill a full health opponent in milliseconds (ms).

        Inputs:
        -------
        dist     - distance to the target, positive value, meters
        """
        # Shoot time = milliseconds per round * number of rounds
        #            = milliseconds
        # minus 1 to btk because the first shot is in the air at t = 0
        # thus, there are btk - 1 times the rof delays the kill
        # minute_to_millisec_conv_coeff = 60000
        shoot_time = (1/self.rof * 60000
                      * (self.btk(dist) - 1)
                     )
        tof = dist/self.velocity*1000   # velocity is in m/s, tof in ms
        ads_time = self.aim_down*1000 if inc_ads else 0 # aim down is in s

        return shoot_time + tof + ads_time

    def get_attachments(self):
        """Return the name of each attachment on the gun as a dictionary."""
        return {"sight": self.sight.NAME, "c_sight": self.c_sight.NAME,
                "mag": self.mag.NAME, "s_rail": self.s_rail.NAME,
                "u_rail": self.u_rail.NAME, "barrel": self.barrel.NAME}

    def _apply_attach(self, attachment, dec_places=3):
        """Apply the attachment to the weapon."""
        self._dam = round(self._dam * attachment._DAM, dec_places)
        self.velocity = round(self.velocity * attachment._VELOCITY, dec_places)
        self.rof = round(self.rof * attachment._ROF, dec_places)
        self.aim_down = round(self.aim_down * attachment._AIM_DOWN, dec_places)

    def _remove_attach(self, attachment, dec_places=3):
        """Removes the attachment from the weapon."""
        self._dam = round(self._dam / attachment._DAM, dec_places)
        self.velocity = round(self.velocity / attachment._VELOCITY, dec_places)
        self.rof = round(self.rof / attachment._ROF, dec_places)
        self.aim_down = round(self.aim_down / attachment._AIM_DOWN, dec_places)

    def swap_sight(self, attachment):
        """Swap the gun's current sight out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptySight'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_sights
                     class variable
        """
        # TODO: a composite might allow you to remove all these duplicate
        # functions
        if attachment is not EmptySight:    # ensure empty is allowed
            if attachment not in self.val_sights:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.sight != attachment:
            self._remove_attach(self.sight)
            self._apply_attach(attachment)
            self.sight = attachment

    def swap_c_sight(self, attachment):
        """Swap the gun's current canted sight out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyCSight'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_c_sights
                     class variable
        """
        if attachment is not EmptyCSight:    # ensure empty is allowed
            if attachment not in self.val_c_sights:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.c_sight != attachment:
            self._remove_attach(self.c_sight)
            self._apply_attach(attachment)
            self.c_sight = attachment

    def swap_mag(self, attachment):
        """Swap the gun's current magazine out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyMag'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_mags
                     class variable
        """
        if attachment is not EmptyMag:    # ensure empty is allowed
            if attachment not in self.val_mags:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.mag != attachment:
            self._remove_attach(self.mag)
            self._apply_attach(attachment)
            self.mag = attachment

    def swap_s_rail(self, attachment):
        """Swap the gun's side rail attachment out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptySRail'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_s_rails
                     class variable
        """
        if attachment is not EmptySRail:    # ensure empty is allowed
            if attachment not in self.val_s_rails:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.s_rail != attachment:
            self._remove_attach(self.s_rail)
            self._apply_attach(attachment)
            self.s_rail = attachment

    def swap_u_rail(self, attachment):
        """Swap the gun's current under rail out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyURail'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_u_rails
                     class variable
        """
        if attachment is not EmptyURail:    # ensure empty is allowed
            if attachment not in self.val_u_rails:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.u_rail != attachment:
            self._remove_attach(self.u_rail)
            self._apply_attach(attachment)
            self.u_rail = attachment

    def swap_barrel(self, attachment):
        """Swap the gun's current barrel out for the given one.

        Inputs:
        -------
        attachment - class object, the attachment you want to put on the
                     gun, eg: 'EmptyBarrel'.

        Raises:
        -------
        ValueError - if the given attachment isn't in the gun's val_barrels
                     class variable
        """
        if attachment is not EmptyBarrel:    # ensure empty is allowed
            if attachment not in self.val_barrels:
                raise ValueError(f"This {attachment.TYPE} cannot be put here.")
        if self.barrel != attachment:
            self._remove_attach(self.barrel)
            self._apply_attach(attachment)
            self.barrel = attachment

    def swap_attach(self, attachment):
        """Swap the gun's current attachment out for the given one.

        The slot the attachment goes into is determined by the attachment. If
        it's a barrel, it goes into the barrel slot, etc.

        Inputs:
        -------
        attachment - attachment class object eg: 'EmptyBarrel'

        Raises:
        -------
        ValueError - the given attachment doesn't match a slot name.
        """
        slot = attachment.TYPE
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
        else:
            raise ValueError(f"{slot} is not a valid slot argument.")


class Ar(Gun):
    """AR Weapon category that extends Gun; to be subclassed by weapons."""
    _HEAD_MULT = 1.5
    _MIN_CO = 0.35

    def __init__(self, gun_type="AR"):
        super().__init__()
        self.gun_type = gun_type
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Lmg(Gun):
    """Lmg Weapon category that extends Gun; to be subclassed by weapons."""
    _HEAD_MULT = 1.5
    _MIN_CO = 0.3

    def __init__(self, gun_type="LMG"):
        super().__init__()
        self.gun_type = gun_type
        self.val_barrels = np.array([HeavyBarrel, LongBarrel])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Smg(Gun):
    """Smg Weapon category that extends Gun; to be subclassed by weapons."""
    _HEAD_MULT = 1.2
    _MIN_CO = 0.25

    def __init__(self, gun_type="SMG"):
        super().__init__()
        self.gun_type = gun_type
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Pdw(Gun):
    """Pdw Weapon category that extends Gun; to be subclassed by weapons."""
    _HEAD_MULT = 1.5
    _MIN_CO = 0.25

    def __init__(self, gun_type="PDW"):
        super().__init__()
        self.gun_type = gun_type
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


class Carbine(Gun):
    """Carbine Weapon category that extends Gun; to be subclassed by weapons."""
    _HEAD_MULT = 1.5
    _MIN_CO = 0.25

    def __init__(self, gun_type="CARBINE"):
        super().__init__()
        self.gun_type = gun_type
        self.val_barrels = np.array([])
        self.val_sights = np.array([])
        self.val_c_sights = np.array([])
        self.val_mags = np.array([])
        self.val_s_rails = np.array([])
        self.val_u_rails = np.array([])


# additions here need to be added to the arsenal generation functions too if
# they are to be used in the main scripts.
class Ak74(Ar):
    """Simulates AK74 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="AK74"):
        super().__init__()
        self.name = gun_name
        self._dam = 33
        # TODO: _dam_prof should be an object...
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 670
        self.velocity = 700
        self.aim_down = 0.25


class M4a1(Ar):
    """Simulates M4A1 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="M4A1"):
        super().__init__()
        self.name = gun_name
        self._dam = 30
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 700
        self.aim_down = 0.24


class Ak15(Ar):
    """Simulates AK15 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="AK15"):
        super().__init__()
        self.name = gun_name
        self._dam = 40
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 540
        self.velocity = 750
        self.aim_down = 0.3


class ScarH(Ar):
    """Simulates SCARH weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="SCAR-H"):
        super().__init__()
        self.name = gun_name
        self._dam = 42
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 500
        self.velocity = 750
        self.aim_down = 0.2


class Acr(Ar):
    """Simulates ACR weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="ACR"):
        super().__init__()
        self.name = gun_name
        self._dam = 25
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 650
        self.aim_down = 0.25


class AugA3(Ar):
    """Simulates AUGA3 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="AUG_A3"):
        super().__init__()
        self.name = gun_name
        self._dam = 31
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 500
        self.velocity = 600
        self.aim_down = 0.15


class Sg550(Ar):
    """Simulates SG550 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="SG550"):
        super().__init__()
        self.name = gun_name
        self._dam = 27
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 640
        self.aim_down = 0.14


class Fal(Ar):
    """Simulates FAL weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="FAL"):
        super().__init__()
        self.name = gun_name
        self._dam = 40
        self._dam_prof = [(150, 1), (300, self._MIN_CO)]
        self.rof = 650
        self.velocity = 600
        self.aim_down = 0.22


class G36c(Ar):
    """Simulates G36C weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="G36C"):
        super().__init__()
        self.name = gun_name
        self.val_barrels = np.array([Ranger, LongBarrel])
        self._dam = 30
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 750
        self.velocity = 600
        self.aim_down = 0.25


class Famas(Ar):
    """Simulates FAMAS weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="FAMAS"):
        super().__init__()
        self.name = gun_name
        self.val_barrels = np.array([Ranger, LongBarrel])
        self._dam = 23
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 900
        self.velocity = 600
        self.aim_down = 0.25


class Hk419(Ar):
    """Simulates HK419 weapon characteristics. Extends Ar class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="HK419"):
        super().__init__()
        self.name = gun_name
        self._dam = 31
        self._dam_prof = [(50, 1), (300, self._MIN_CO)]
        self.rof = 660
        self.velocity = 700
        self.aim_down = 0.25


class L86a1(Lmg):
    """Simulates L86A1 weapon characteristics. Extends Lmg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="L86A1"):
        super().__init__()
        self.name = gun_name
        self._dam = 32
        self._dam_prof = [(100, 1), (300, self._MIN_CO)]
        self.rof = 775
        self.velocity = 600
        self.aim_down = 0.3


class M249(Lmg):
    """Simulates M249 weapon characteristics. Extends Lmg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="M249"):
        super().__init__()
        self.name = gun_name
        self._dam = 30
        self._dam_prof = [(100, 1), (300, self._MIN_CO)]
        self.rof = 700
        self.velocity = 600
        self.aim_down = 0.35


########################################################################
# SMG
class Mp7(Smg):
    """Simulates MP7 weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="MP7"):
        super().__init__()
        self.name = gun_name
        self._dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 950
        self.velocity = 350
        self.aim_down = 0.15


class Ump45(Smg):
    """Simulates UMP45 weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="UMP-45"):
        super().__init__()
        self.name = gun_name
        self._dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 700
        self.velocity = 500
        self.aim_down = 0.2


class Pp2000(Smg):
    """Simulates PP2000 weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="PP2000"):
        super().__init__()
        self.name = gun_name
        self._dam = 23
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 900
        self.velocity = 350
        self.aim_down = 0.2


class KrissVector(Smg):
    """Simulates KRISSVECTOR weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="KRISS_VECTOR"):
        super().__init__()
        self.name = gun_name
        self._dam = 24
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 1200
        self.velocity = 400
        self.aim_down = 0.25


class Mp5(Smg):
    """Simulates MP5 weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="MP5"):
        super().__init__()
        self.name = gun_name
        self._dam = 26
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 400
        self.aim_down = 0.2


class Pp19(Smg):
    """Simulates PP19 weapon characteristics. Extends Smg class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="PP19"):
        super().__init__()
        self.name = gun_name
        self.val_barrels = np.array([])
        self._dam = 25
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 750
        self.velocity = 400
        self.aim_down = 0.20


class HoneyBadger(Pdw):
    """Simulates HONEYBADGER weapon characteristics. Extends Pdw class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="HONEY_BADGER"):
        super().__init__()
        self.name = gun_name
        self._dam = 35
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2


class P90(Pdw):
    """Simulates P90 weapon characteristics. Extends Pdw class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="P90"):
        super().__init__()
        self.name = gun_name
        self._dam = 28
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 390
        self.aim_down = 0.2


class Groza(Pdw):
    """Simulates GROZA weapon characteristics. Extends Pdw class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="GROZA"):
        super().__init__()
        self.name = gun_name
        self._dam = 27
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 700
        self.velocity = 390
        self.aim_down = 0.2


class AsVal(Carbine):
    """Simulates ASVAL weapon characteristics. Extends Carbine class.

    Most of the methods here are inherited from Gun.

    Instance Variables:
    -------------------
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
    ----------
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
    def __init__(self, gun_name="AS_VAL"):
        super().__init__()
        self.name = gun_name
        self._dam = 35
        self._dam_prof = [(50, 1), (200, self._MIN_CO)]
        self.rof = 800
        self.velocity = 560
        self.aim_down = 0.2