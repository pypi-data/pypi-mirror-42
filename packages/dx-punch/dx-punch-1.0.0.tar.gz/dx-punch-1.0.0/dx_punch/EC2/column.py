# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
import numpy as np
import matplotlib.pyplot as plt
import os

from collections import defaultdict
from math import isclose, atan, asin, tan, sqrt, pi, sin, ceil
from shapely.affinity import translate
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import linemerge

from dx_utilities.decorators import tolerate_input
from dx_utilities.geometry import PlanarShape, LinearShape
from dx_utilities.geometry.operations import reflect
from dx_utilities.vectors import mean as vmean
from dx_utilities.units import (inverse_transform_value, transform_units)
from dx_utilities.pretty_print import print_dict
from dx_utilities.exceptions import CodedValueError

from dx_base.elements import RCColumn2D, ColumnDropPanel
from dx_base.exceptions import ReinforcementError, ImplementationError

from dx_eurocode.EC2.formulas import k647
from .exceptions import ImpossibleShearCages
from .shear_reinforcement import ShearCage
from .perimeters import *
from .forces import InternalForces


class ColumnGeometry(RCColumn2D):
    """Represents the geometry of the column, that is
    dependent with respect to the parent slab.

    :param Slab slab:
    :param _id: A discrete id for the column. If none
        is given, one is automatically generated.
    :type _id: str or None
    :param bool floating: Flag column as a floating column.
        This affects the evaluation of eccentricities.
    """

    def __init__(self, slab=None, _id=None, floating=False, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.slab = slab
        if _id is None:
            self._id = 'C' + str(id(self))[-4:]
        else:
            self._id = _id
        self.floating = floating
        self._offset = None
        self._oxmin = None
        self._oxmax = None
        self._oymin = None
        self._oymax = None
        self._kx = None
        self._ky = None
        self._truncate_point = None
        self._relative_centroid = None
        self._rebar = None

    @property
    def rebar(self):
        """Container of tensile-reinforcement fields
        on the slab, in the vicinity of the column.

        :rtype: list(dx_utilities.fields.fields.UniformPlanarField)
        """
        if self._rebar is None:
            self._rebar = self.slab.resolve_rebar(self.less)
        return self._rebar

    @rebar.setter
    def rebar(self, value):
        """
        :param list value:
        """
        self._rebar = value

    @staticmethod
    def k639(breadth_ratio):
        """Evaluate the k-factor for Eq. (6.39), as implied by
        Table 6.1, on the basis of the ratio of the breadth of
        the side parallel to the eccentricity over the breadth of
        the other side.

        The k-factor represents the portion of unbalanced moment
        that is balanced by an additional shear-stress distribution
        along the critical perimeter.

        :param float breadth_ratio:
        :rtype: float
        :return: The value of the k-factor.
        """
        if breadth_ratio <= 0.5:
            return 0.45
        elif breadth_ratio <= 1.:
            return 0.45 + 0.30*(breadth_ratio - 0.5)
        elif breadth_ratio <= 3.:
            return 0.60 + 0.10*(breadth_ratio - 1.0)
        else:
            return 0.80

    @property
    def relative_centroid(self):
        """Relative vector of column's centroid with
        reference to the parent slab centroid.

        :rtype: `numpy.array`
        """
        if self._relative_centroid is None:
            self._relative_centroid = (np.array(self.centroid) -
                                       np.array(self.slab.centroid))
        return self._relative_centroid

    @property
    def kx(self):
        """Value of `k639` in case of eccentric loading
        along the x-direction.

        :rtype: float
        """
        if self._kx is None:
            self._kx = self.k639(self.by/self.bx)
        return self._kx

    @property
    def ky(self):
        """Value of `k639` in case of eccentric loading
        along the y-direction.

        :rtype: float
        """
        if self._ky is None:
            self._ky = self.k639(self.bx/self.by)
        return self._ky

    @property
    def oxmin(self):
        """Minimum offset distance from the parent slab along
        'x' axis.

        :rtype: float
        """
        if self._oxmin is None:
            self._oxmin = min(self.offset[:3:2])
        return self._oxmin

    @property
    def oymin(self):
        """Minimum offset distance from the parent slab along
        'y' axis.

        :rtype: float
        """
        if self._oymin is None:
            self._oymin = min(self.offset[1:4:2])
        return self._oymin

    @property
    def oxmax(self):
        """Maximum offset distance from the parent slab along
        'x' axis.

        ``[m]``

        :rtype: float
        """
        if self._oxmax is None:
            self._oxmax = max(self.offset[:3:2])
        return self._oxmax

    @property
    def oymax(self):
        """Maximum offset distance from the parent slab along
        'y' axis.

        ``[m]``

        :rtype: float
        """
        if self._oymax is None:
            self._oymax = min(self.offset[1:4:2])
        return self._oymax

    @property
    def offset(self):
        """Offset distances of the boundary of the column from
        the boundary of the slab.

        ``[m]``

        :rtype: tuple(float)
        :return: ``(dxlower, dylower, dxupper, dyupper)``
        """
        if self._offset is None:
            self._offset = self.distance_between_bounds(self.slab)
        return self._offset

    def _evaluate_truncate_point(self):
        """Evaluate the coordinate of the truncate-point. See the
        description in the ``truncate_point`` method.

        :rtype: `numpy.array`
        :return: The coordinates ``np.array(Tx, Ty)`` in the coordinate system
            that defines the slab.
        """
        # Local origin
        oxy = np.array(self.bounds[:2])
        cxy = np.array(self.centroid) - oxy
        cx, cy = cxy

        xleft, ylower, xright, yupper = self.offset

        if xleft < xright:
            tx = max(cx, self.bx - 1.5*self.deff)
        else:
            tx = min(cx, 1.5*self.deff)

        if ylower < yupper:
            ty = max(cy, self.by - 1.5*self.deff)
        else:
            ty = min(cy, 1.5*self.deff)

        return oxy + np.array([tx, ty])

    @property
    def truncate_point(self):
        """For each column we define a point within the column's
        bounding rectangle that will enable the calculation of
        the truncated control perimeter according to the provisions
        of §6.4.3(4) in EC2.

        With reference to Fig. 6.20(a) and (b), the truncated
        point ``(Tx, Ty)`` may assume one of the following
        realizations with respect to a *local* coordinate system
        that has its origin on the lower-left vertice of the
        column:

            * ``Tx = max(cx, bx - 1.5d)`` for columns close to the
              left boundary of the slab
            * ``Tx = min(cx, 1.5d)`` for columns close to the
              right boundary of the slab
            * ``Ty = max(cy, by - 1.5d)`` for columns close to the
              lower boundary of the slab
            * ``Ty = min(cy, 1.5d)`` for columns close to the
              upper boundary of the slab

        where ``(cx, cy)`` are the coordinates of the column's centroid,
        ``d`` is the effective depth of the slab in the vicinity of
        the column, and ``bx, by`` denote the breadth of the bounding
        rectangle of the column along the local axes.

        This definition is consistent with the provisions of §6.4.3(4)
        and allows for the generalization of the methodology for
        constructing the truncated perimeter ``u1*`` for column-shapes
        other than rectangles and circles. Nevertheless, this should
        be subject to scrutiny from anyone using this function,
        and to revision upon associated revisions in EC2.

        :rtype: tuple
        :return: The coordinates ``(Tx, Ty)`` in the coordinate system
            that defines the slab.
        """
        if self._truncate_point is None:
            self._truncate_point = self._evaluate_truncate_point()
        return self._truncate_point


class TensileReinforcement(object):
    """Represent the tensile reinforcement of a slab in the vicinity
    of a given column.

    This class provides an interface between `Slab` instances and their
    dependent `Column` instances. It wraps certain derived properties
    of the tensile reinforcement.

    :param Slab slab:
    :param ColumnGeometry column:
    """

    def __init__(self, slab, column):
        self.slab = slab
        self.column = column
        self._Ast = None
        self._phix = None
        self._phiy = None
        self._rhox = None
        self._rhoy = None
        self._rhol = None
        self._depth = None
        self._k647 = None
        self._effective_region = None
        self._rebar = None

    @property
    def rebar(self):
        """Container of reinforcement fields on the slab
        that intersect the effective region.

        :rtype: list(dx_utilities.fields.fields.UniformPlanarField)
        """
        if self._rebar is None:
            self._rebar = self.slab.resolve_rebar(self.effective_region.less,
                                                  contains=False)
        return self._rebar

    @rebar.setter
    def rebar(self, value):
        """
        :param list value:
        """
        self._rebar = value

    @property
    def phix(self):
        """Representation of the tensile reinforcement
        along the x-axis in more friendly format of the type
        ``T<diameter [mm]>@<spacing [mm]>"``, e.g. ``T20@100``.

        :rtype: str
        """
        if self._phix is None:
           self._phix =  ' + '.join(
                [str(f.value[1]) for f in self.rebar]
                )
        return self._phix

    @property
    def phiy(self):
        """Representation of the tensile reinforcement
        along the y-axis in more friendly format of the type
        ``T<diameter [mm]>@<spacing [mm]>"``, e.g. ``T20@100``.

        :rtype: str
        """
        if self._phiy is None:
           self._phiy =  ' + '.join(
                [str(f.value[1]) for f in self.rebar]
                )
        return self._phiy

    @property
    def Ast(self):
        """Get total area of tensile reinforcement
        in the vicinity of the column, in the two
        horizontal dimensions. The vicinity is quantified
        according to the provisions of §6.4.4.

        ``[m2]``

        :rtype: `numpy.array`\ ``(dtype='float64')``
        """
        if self._Ast is None:
            self._Ast = self._evaluate_Ast()
        return self._Ast

    @property
    def Asx(self):
        """Total area of tensile reinforcement in the vicinity
        of the column, along the x-direction.

        ``[m2]``

        :rtype: float
        """
        return self.Ast[0]

    @property
    def Asy(self):
        """Total area of tensile reinforcement in the vicinity
        of the column, along the y-direction.

        ``[m2]``

        :rtype: float
        """
        return self.Ast[1]

    @property
    def rhox(self):
        """Reinforcement ratio along the x-direction
        averaged over the effective tensile reinforcement
        region of the column.

        :rtype: float
        """
        if self._rhox is None:
            self._rhox = self.Asx / self.effective_region.by / self.depth
        return self._rhox

    @property
    def rhoy(self):
        """Reinforcement ratio along the y-direction
        averaged over the effective tensile reinforcement
        region of the column.

        :rtype: float
        """
        if self._rhoy is None:
            self._rhoy = self.Asy / self.effective_region.bx / self.depth
        return self._rhoy

    @property
    def rhol(self):
        """Total longitudinal reinforcement ratio on the
        effective tensile reinforcement region in the
        vicinity of the column.

        Calculated according to §6.4.4.

        :rtype: float
        """
        if self._rhol is None:
            self._rhol = min(sqrt(self.rhox*self.rhoy), 0.02)
            if isclose(self._rhol, 0.):
                self._rhol = max(self.rhox, self.rhoy)
        return self._rhol

    @property
    def effective_region(self):
        """Region of effective tensile reinforcement in the
        vicinity of the slab. According to §6.4.4, this is
        defined as a region bounded by a rectangular offset
        of the column at distance ``3*deff``.

        :rtype: dx_utilities.geometry.planar.PlanarShape
        """
        if self._effective_region is None:
            self._update_effective_region()
        return self._effective_region

    def _update_effective_region(self):
        """Update the effective region."""
        bx = self.column.bx + 6*self.depth
        by = self.column.by + 6*self.depth
        unbounded_region = PlanarShape.create_rectangle_by_dimensions(
            bx=bx, by=by, origin=np.array(self.column.centroid)
            )
        self._effective_region = PlanarShape(
            shell=unbounded_region.intersection(self.slab)
            )

    @property
    def depth(self):
        """Effective depth of the slab in the vicinity
        of the column.

        ``[m]``

        :rtype: float
        """
        if self._depth is None:
            self._depth = self._resolve_depth()
        return self._depth

    @depth.setter
    def depth(self, value):
        """Allowing customizing the effective depth in the
        vicinity of the column, for the purposes of parametric
        analysis.

        :param float value:
        :rtype: float
        """
        self._depth = value
        self._k647 = None

    def _resolve_depth(self):
        """Resolve the effective depth of the parent slab
        in the vicinity of the column.

        The algorithm finds all reinforcement fields that
        contain the column and averages the effective depth
        among the fields.

        :rtype: float
        :raise ReinforcementError: If no tension reinforcement
            defined on the slab, or in the vicinity of the
            column.
        """
        containers = self.column.rebar

        average_rebar = sum([c.value for c in containers])
        d = [r.d for r in filter(None, average_rebar)]
        return vmean(d)

    def _evaluate_Ast(self):
        """Get data about the reinforcement of the parent slab
        in the effective tensile region of the column.

        :rtype: `numpy.array`\ ``(dtype=SteelReinforcement)``
        :raise ReinforcementError: If no tension reinforcement
            defined on the slab, or in the vicinity of the
            column.
        """
        containers = self.slab.resolve_rebar(self.effective_region,
                                             contains=False)

        As = np.zeros(3)
        for container in containers:
            domain = PlanarShape(
                container.geometry.intersection(self.effective_region)
                )
            weights = np.array([domain.by, domain.bx, 1.])
            Asbr = []
            for r in container.value:
                try:
                    Asbr.append(r.Asbr)
                except AttributeError:
                    Asbr.append(r)
            As += np.array(Asbr) * weights

        if not any(As[:2]):
            raise ReinforcementError(4000, ("No tension-reinforcement "
                                            "found in the vicinity of "
                                            "the column."))

        return As[:2]

    @property
    def k647(self):
        """Factor used in Eq. (6.47). It depends on the effective
        depth in the vicinity of the column.

        :rtype: float
        """
        if self._k647 is None:
            self._k647 = k647(self.depth)
        return self._k647

    def __repr__(self):
        return ' + '.join(map(str, self.rebar))

    def update_depth(self):
        """Re-evaluate effective depth and effective tensile
        region.
        """
        self.column.rebar = None
        self._depth = self._resolve_depth()
        self._update_effective_region()


class ColumnReinforcement(ColumnGeometry):
    """Representation of a column-geometry with
    reinforcement.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tensile = TensileReinforcement(self.slab, self)
        self._shear = None
        self._fywdef = None
        self._deff = None
        self._k647 = None

    @property
    def k647(self):
        """Factor used in Eq. (6.47). It depends on the effective
        depth in the vicinity of the column.

        :rtype: float
        """
        return self.tensile.k647

    @property
    def deff(self):
        """Effective depth of the slab in the vicinity
        of the column.

        ``[m]``

        :rtype: float
        """
        return self.tensile.depth

    @deff.setter
    def deff(self, value):
        """Allowing customizing the effective depth in the
        vicinity of the column, for the purposes of parametric
        analysis.

        :param float value:
        """
        self.set_deff(value)

    def set_deff(self, value):
        """Override value of `deff`, and reset `k647`.

        :param float value:
        """
        self.tensile.depth = value
        self._k647 = None

    @property
    @transform_units()
    def fywdef(self):
        """Effective design yield strength of
        shear reinforcement bars.

        ``[Pa]``

        :rtype: float
        """
        if self._fywdef is None:
            self._fywdef = min(250 + 0.25*self.deff*1e+03, self.slab.fywd*1e-06)
        return self._fywdef

    @property
    def shear(self):
        """Shear reinforcement in the vicinity of the slab.

        :rtype: ShearCage
        """
        if self._shear is None:
            self._shear = ShearCage()
        return self._shear

    def set_shear_reinforcement(self, *args, **kwargs):
        """Set shear reinforcement in the vicinity
        of the column.

        :param \*args: Any positional arguments used
            for the instantiation of `ShearCage`.
        :param \*\*kwargs: Any keyword arguments used
            for the instantiation of `ShearCage`.
        """
        self._shear = ShearCage(*args, **kwargs)

    def evaluate_shear_cage_uouteff(self, perimeter, rtol=1e-03,
                                    maxcsx=None, maxcsy=None,
                                    mincsx=None, mincsy=None):
        """Evaluate the effective outer perimeter in which no shear
        reinforcement is required, when shear cages are used
        for the reinforcement, in accordance with the provisions
        of §6.4.5(4).

        The evaluation is iterative and stops when the resulting length
        converges to the length of the ``uout`` length of the ``perimeter``.

        :param BasicControlPerimeter perimeter: The perimeter where
            the basic checks have failed.
        :param float rtol: Relative tolerance of the length of the
            effective perimeter with respect to the theoretical
            length.
        :param maxcsx: Upper bound for the **half**-breadh
            of the shear cage along y.
        :type maxcsx: float or None
        :param maxcsy: Upper bound for the **half**-breadh
            of the shear cage along x.
        :type maxcsy: float or None
        :param mincsx: Lower bound for the **half**-breadh
            of the shear cage along y.
        :type mincsx: float or None
        :param mincsy: Lower bound for the **half**-breadh
            of the shear cage along x.
        :type mincsy: float or None
        :rtype: LineString or MultiLineString
        """
        constructor = self.construct_shear_cage_symmetric_uouteff
        uout = perimeter.uout
        # Iteration parameters
        inc = 0.1
        # Initialize the values of interest
        uouteff = constructor()
        ri, csx, csy = uouteff.r, uouteff.csx, uouteff.csy
        # Start iterations until convergence is attained
        maxcsx = maxcsx or 0.5*self.bx
        maxcsy = maxcsy or 0.5*self.by
        mincsx = mincsx or 0.4*self.bx
        mincsy = mincsy or 0.4*self.by
        while (uouteff.length < uout or uouteff.length - uout > rtol * uout):
            if uouteff.length > uout:
                if csx < mincsx or csy < mincsy:
                    break
                if uouteff.ad < 2 * self.deff:
                    ri *= (1. - inc)
                    csx *= (1. - 2*inc)
                    csy *= (1. - 2*inc)
                else:
                    csx *= (1. - inc)
                    csy *= (1. - inc)
            else:
                if (uouteff.ad < 2 * self.deff
                        or (isclose(csx, maxcsx) and isclose(csy, maxcsy))):
                    ri *= (1. + inc)
                else:
                    csx = min((1. + inc)*csx, maxcsx)
                    csy = min((1. + inc)*csy, maxcsy)

            uouteff = constructor(ri, csx, csy)
            ri, csx, csy = uouteff.r, uouteff.csx, uouteff.csy

        diag = None
        if uouteff.ad > 2*self.deff:
            stmax = 10
            for st in range(stmax, 1, -1):
                try:
                    diag = self.resolve_diagonal_shear_cages(uouteff,
                                                             st=st*1e-02)
                    break
                except ImpossibleShearCages:
                    continue
        return uouteff, diag

    def construct_shear_cage_symmetric_uouteff(self, r=None, csx=None, csy=None,
                                               diagonals=True):
        """Construct the outer perimeter in which no shear reinforcement
        is required, for a given configuration of shear cages reinforcing
        the slab agains punching shear. This is in consistency with §6.4.5(3).

        This geometric construction of the perimeter assumes
        a symmetric distribution of the shear cages with respect to the
        envelope of the column, along the two principal axes.

        :param r: The distance of the farthest perimeter of the shear
            reinforcement from the faces of the column.
        :type r: float or None
        :param csx: The breadth of the shear cages that are distributed
            along the **y-axis**.
        :type csx: float or None
        :param csy: The breadth of the shear cages that are distributed
            along the **x-axis**.
        :type csy: float or None
        :param bool diagonals: If `True`, the calculation
            assumes a continuous perimeter, even in the case when
            ``ad > 2*self.deff``. This assumption holds true, if
            there can be defined a geometrically compatible
            diagonal layout of cages, so that the maximum distance
            between any two cages in the full set does not
            exceed ``2*self.deff``.
        :rtype: ShearCagePerimeter
        """
        # Base vectors
        ix = np.array([1., 0.])
        iy = np.array([0., 1.])
        # Swallow exception for the moment
        # TODO: Handle non-symmetric cases
        # if not np.allclose(self.centroid, self.envelope.centroid):
        #     raise Exception(('Not a symmetric section. Can\'t '
        #                      'calculate perimeter'))
        r = r or 0.5 * self.deff
        csx = csx or self.shear.csx or 0.5*self.bx + 2*self.deff/5
        csy = csy or self.shear.csy or 0.5*self.by + 2*self.deff/5

        # Basic reference point
        origin = np.array([self.centroid.x, self.centroid.y])
        # Distance of farthest perimeter of shear-reinforcement
        # along 'x' and 'y'
        rx0 = self.bx/2 + r
        ry0 = self.by/2 + r
        # Angles and distances between the external bars
        # of the cage along x and the cage along y
        ax = rx0 - csx/2
        ay = ry0 - csy/2
        ad = sqrt(ax**2 + ay**2)
        sinthx = ax / ad
        sinthy = ay / ad
        thx = asin(sinthx)
        thy = -asin(sinthy)
        # Center point along the two axes for outer-perimeter
        # arcs
        Cx = origin + ix*(rx0 - csy/2*ay/ax)
        Cy = origin + iy*(ry0 - csx/2*ax/ay)

        # Distances of outer perimeter from the external
        # bars of the shear cage
        k = 1.5
        rx = csy/2/sinthx + k*self.deff
        ry = csx/2/sinthy + k*self.deff

        # Construct outer-perimeter arcs
        arcx = LinearShape.create_arc(Cx, rx, end_angle=thx)
        arcy = LinearShape.create_arc(Cy, ry, end_angle=pi/2+thy,
                                      start_angle=pi/2.)

        if diagonals or ad <= 2*self.deff:
            shell = arcx.merge(arcy)
        else:
            dx = (Cx + (rx*sinthy - self.deff*sinthx)*ix +
                       (rx*sinthx + self.deff*sinthy)*iy)
            dy = (Cy + (ry*sinthy + self.deff*sinthx)*ix +
                       (ry*sinthx - self.deff*sinthy)*iy)
            arcx = arcx.add_point(dx)
            arcy = arcy.add_point(dy)
            shell = arcx.union(arcy)
        shell = reflect(shell, origin=np.array(self.centroid))
        shell = reflect(shell, normal=(0., 1.), origin=np.array(self.centroid))
        return ShearCagePerimeter(shell.intersection(self.slab), ad, r,
                                  csx, csy)

    def resolve_diagonal_shear_cages(self, uouteff, st=0.1, cs=None):
        """Evaluate minimum number of diagonal shear
        cages to fill the layout of the punching-shear
        reinforcement, so that no two cages are placed
        at a distance greater than ``2*self.deff``.

        The distance of the first perimeter of these
        diagonal cages may vary between a minimum value
        and a maximum value from the sides
        of the column. These are also evaluated.

        :param float st: The distance between shear cages.
        :param cs: The breadth of the shear cage. If `None`,
            it is considered equal to ``st``.
        :type cs: float or None
        :return:
            A tuple ``(nmin, r0, rmax, st, cs)``, where::

                cs: The number of diagonal shear cages,
                r0, rmax: the minimum and maximum values for the distance
                          of the first perimeter of shear cages from the
                          column sides.
                st: The resulting distance between diagonal shear
                    cages,
                cs: The resulting breadth of the shear cage.

        :rtype: tuple
        :raise ImpossibleShearCages: If layout cannot be constructed.
        """
        cs = cs or st
        rout = uouteff.r
        ad = uouteff.ad
        nmin = ceil((ad + cs) / (2*self.deff + cs))
        s = (nmin - 1)*cs + nmin*st
        r = 1.01 * s / pi * 2
        thcs = asin(cs/2/r) * 2
        thst = asin(st/2/r) * 2
        while (nmin - 1)*thcs + nmin*thst > pi/2:
            r *= 1.01
            thcs = asin(cs/2/r) * 2
            thst = asin(st/2/r) * 2
        r0 = st / 2 / sin(thst/2)
        rmax = 1.5*self.deff / ad * rout
        if r0 > rmax:
            raise ImpossibleShearCages(4003, (f"Impossible shear cage layout "
                                              f"for st={st:.1f} and "
                                              f"cs={cs:.1f}"))
        return nmin, r0, rmax, st, cs


class ColumnForces(ColumnReinforcement):
    """Class representing columns acting on a slab.

    :param Slab slab: The slab to be designed.
    :param float N: The axial force on the column.
    :param float Mex: The moment acting about the x-axis (↠).
    :param float Mey: The moment acting about the y-axis (↟).
    :param \*args: Positional arguments in parent class.
    :param \*\*kwargs: Key-word arguments in parent class.
    """

    def __init__(self, N=1., Mex=0., Mey=0., LC='LC0',
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lc_index = dict()
        self.load_cases = []
        self.reactions = dict()
        self.add_new_lc(LC, N=N, Mex=Mex, Mey=Mey)
        # Caching properties (see respective functions for description)
        self._forces = None
        self._soil_pressure = None
        self._bMomenti = None
        self._vmin = None
        self._vrdc = None
        self._uouteff = None
        self._Ri = None

    @property
    def Ri(self):
        """Array of pile reactions.

        ``[N]``

        :rtype: `numpy.array`
        """
        if self._Ri is None:
            if self.reactions:
                self._Ri = np.fromiter(self.reactions.values(), dtype=np.float64)
            else:
                self._Ri = np.zeros(self.nlc)
        return self._Ri

    @property
    def nlc(self):
        """Number of load-cases specified for this instance.

        :rtype: int
        """
        return len(self.load_cases)

    @property
    def forces(self):
        """The array of internal-forces.

        :rtype: list(InternalForces)
        """
        if self._forces is None:
            self._repopulate_forces()
        return self._forces

    def _repopulate_forces(self):
        """Repopulate array of internal forces."""

        self._forces = np.concatenate(self.load_cases)

    @property
    def Ni(self):
        """Array of axial forces with respect to the load-cases
        specified.

        ``[N]``

        :rtype: `numpy.array`
        """
        return self.forces[:, 0]

    @property
    def Vedi(self):
        """Array of design axial forces with respect to the load-cases
        specified. They are evaluated by subtracting any pile reaction
        might be acting on the base of the column, for each load-case
        separately.

        ``[N]``

        :rtype: `numpy.array`
        """
        return self.Ni - self.Ri

    @property
    def Mexi(self):
        """Array of moments about the x-axis with respect to the load-cases
        specified.

        ``[N.m]``

        :rtype: `numpy.array`
        """
        return self.forces[:, 1]

    @property
    def Meyi(self):
        """Array of moments about the y-axis with respect to the load-cases
        specified.

        ``[N.m]``

        :rtype: `numpy.array`
        """
        return self.forces[:, 2]

    @tolerate_input('N', 'Mex', 'Mey')
    def add_new_lc(self, name=None, N=0., Mex=0., Mey=0):
        """Add new case of internal forces in the respective
        container and index.

        In addition update the respective container.

        :param str name: The name of the case.
        :param float N: The axial force on the column.
        :param float Mex: The moment acting about the x-axis (↠).
        :param float Mey: The moment acting about the y-axis (↟).
        """
        if name is None:
            name = 'LC' + str(id(self))[:2:-2]
        new_lc = InternalForces(LC=name, N=N, Mex=Mex, Mey=Mey)
        self.load_cases.append(new_lc)
        self.lc_index[name] = new_lc
        self._forces = None

    def set_lc(self, name, **kwargs):
        """Override components of an existing load-case. Useful
        for testing purposes, and for parametric analyses.

        :param str name: The name of the load-case to set.
        :param \*\*kwargs: Component-name and value pairs (e.g. 'N=13.').
        """
        lc = self.lc_index[name]
        for component, value in kwargs.items():
            setattr(lc, component, value)
        self._forces = None
        self._bMomenti = None

    def add_pile_reaction(self, lc, R):
        """Add any present pile reaction, in case of foundation slabs.

        :param str lc: The name of the load-combination
        :param float R: The value of the pile reaction
        """
        self.reactions[lc] = R
        self._Ri = None

    @property
    def phix(self):
        """Representation of the tensile reinforcement
        along the x-axis in more friendly format of the type
        ``T<diameter [mm]>@<spacing [mm]>"``, e.g. ``T20@100``.

        :rtype: str
        """
        return self.tensile.phix

    @property
    def phiy(self):
        """Representation of the tensile reinforcement
        along the y-axis in more friendly format of the type
        ``T<diameter [mm]>@<spacing [mm]>"``, e.g. ``T20@100``.

        :rtype: str
        """
        return self.tensile.phiy
        return ' + '.join([str(f.value[1]) for f in self.tensile.rebar])

    @property
    def Ast(self):
        """The total area of tensile reinforcement
        in the vicinity of the column in the two
        horizontal dimensions. The vicinity is quantified
        according to the provisions of §6.4.4.

        ``[m2]``

        :rtype: `numpy.array`\ ``(dtype='float64')``
        """
        return self.tensile.Ast

    @property
    def Asy(self):
        """Total area of tensile reinforcement in the vicinity
        of the column, along the x-direction.

        ``[m2]``

        :rtype: float
        """
        return self.tensile.Asy

    @property
    def Asx(self):
        """Total area of tensile reinforcement in the vicinity
        of the column, along the x-direction.

        ``[m2]``

        :rtype: float
        """
        return self.tensile.Asx

    @property
    def rhox(self):
        """Reinforcement ratio along the x-direction
        averaged over the effective tensile reinforcement
        region of the column.

        :rtype: float
        """
        return self.tensile.rhox

    @property
    def rhoy(self):
        """Reinforcement ratio along the y-direction
        averaged over the effective tensile reinforcement
        region of the column.

        :rtype: float
        """
        return self.tensile.rhoy

    @property
    def rhol(self):
        """Total longitudinal reinforcement ratio on the
        effective tensile reinforcement region in the
        vicinity of the column.

        Calculated according to §6.4.4.

        :rtype: float
        """
        return self.tensile.rhol

    def set_deff(self, value):
        """Override the effective depth in the
        vicinity of the column, for the purposes of parametric
        analysis.

        :param float value:
        :rtype: float
        """
        super().set_deff(value)
        self._vmin = None

    @property
    @transform_units()
    def vmin(self):
        """Minimum shear stress capacity.

        ``[Pa]``

        :rtype: float
        """
        if self._vmin is None:
            fck = inverse_transform_value(self.slab.material.fck)
            self._vmin = 0.035 * self.k647**1.5 * fck**0.5
        return self._vmin

    @property
    def soil_pressure(self):
        """The soil-pressure in the vicinity of the column
        when it is connected to a foundation-slab.

        ``[Pa]``

        :rtype: float
        """
        if self._soil_pressure is None:
            self._soil_pressure = self._resolve_soil_pressure()
        return self._soil_pressure

    @soil_pressure.setter
    def soil_pressure(self, value):
        """The soil pressure acts on the slab, and hence it should
        be set while configuring the parent slab.

        Nevertheless, it might be the case that for analysis purposes
        the designer wants to force a different value.

        :param float value:
        :rtype: float
        """
        self._soil_pressure = value

    @property
    def bMomenti(self):
        """Array of 2-bit classifiers of direction of
        bending for all specified loadcases.

        The classifiers can be interpreted
        according to the following map:

            * 00: No bending
            * 01: Unidirectional (x-axis)
            * 10: Unidirectional (y-axis)
            * 11: Bidirectional

        Helps in performing logical checks with
        binary operators.

        :rtype: `numpy.array`
        """
        if self._bMomenti is None:
            zeros = np.zeros(self.nlc)
            xbending = np.ones(self.nlc, dtype=np.int8)
            xbending[np.isclose(self.Mexi, zeros)] = 0
            ybending = np.ones(self.nlc, dtype=np.int8) * 2
            ybending[np.isclose(self.Meyi, zeros)] = 0
            self._bMomenti = xbending + ybending
        return self._bMomenti

    @property
    @transform_units()
    def vrdc(self):
        """Shear capacity of the slab in the region
        of the effective tensile reinforcement in
        the vicinity of the column.

        ``[Pa]``

        It is evaluated from Eq. (6.47) ignoring
        the effect of axial forces acting on the
        plane of the slab.

        :rtype: float
        """
        if self._vrdc is None:
            CRdc = self.slab.CRdc
            fck = inverse_transform_value(self.slab.material.fck, 'M')
            vmin = inverse_transform_value(self.vmin)
            self._vrdc = max(CRdc * self.k647 * (100*self.rhol*fck)**(1/3),
                             vmin)
        return self._vrdc

    def update_effective_depth(self):
        """Re-evaluate effective depth and effective tensile
        region.
        """
        self.tensile.update_depth()

    def _resolve_soil_pressure(self):
        """Find the soil pressure in the vicinity of the column.
        Applies only to foundation elements.

        :rtype: float
        """
        if not self.slab.foundation:
            return 0.

        container = None
        for field in self.slab.soil_pressure:
            if field.geometry.contains(self):
                container = field
                break

        if container is None:
            return 0.

        try:
            value = container.value
        except AttributeError:
            value = container.query_avg(self)

        return value


class Column(ColumnForces):
    """Representation of a column with reinforcement
    and its derived control perimeters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = None
        self._control_perimeters = None
        self._basic_control_perimeters = None
        self._uouteff = None
        self._ui = None
        self._u0 = None
        self._dcr0 = None
        self._dcri = None
        self._output = None

    @property
    def output(self):
        """Aggregated data and results from the design
        procedure

        :rtype: dict
        """
        if self._output is None:
            self._output = self.to_json()
        return self._output

    @property
    def position(self):
        """The position of the column as inferred by
        the construction of the most-adverse
        basic control perimeter `ui`.

        :rtype: str
        """
        return self.ui.position

    def set_lc(self, name, **kwargs):
        """Set components of an existing load-case. Useful
        for testing purposes, and for parametric analyses.

        :param str name: The name of the load-case to set.
        :param \*\*kwargs: Component-name and value pairs (e.g. 'N=13.').
        """
        super().set_lc(name, **kwargs)
        self.recalculate_control_perimeters()
        self.ui = None

    @property
    def u0(self):
        """The control perimeter at the sides of the column.

        :rtype: ControlPerimeter
        """
        d = self.deff
        if self.drop_panel:
            d += self.drop_panel.height
        return ColumnPerimeter(self, shell=self, deff=d)

    @property
    def ui(self):
        """Most adverse basic control perimeter as defined in §6.4.2.

        Adversity is measured throuth the demand-to-capacity ration
        of the shear stress on the perimeter.

        :rtype: BasicControlPerimeter
        """
        if self._ui is None:
            self._ui = max(self.basic_control_perimeters, key=lambda u: u.dcr)
        return self._ui

    @ui.setter
    def ui(self, perimeter):
        """Set the value of the basic control perimeter.

        :param BasicControlPerimeter perimeter:
        """
        self._ui = perimeter

    @property
    def basic_control_perimeters(self):
        """The traces of slab-sections in the vicinity of the
        column, where a check between punching shear capacity
        and design-value should be made.

        The perimeter of the column itself is not included
        in this container.

        :rtype: tuple
        :return: A tuple of control perimeters.
        """
        if self._basic_control_perimeters is None:
            perimeters = self._calculate_control_perimeters()
            self._basic_control_perimeters = perimeters
        return self._basic_control_perimeters

    def _calculate_control_perimeters(self):
        """Calculate the control perimeters on the slab
        according to the provisions of §6.4.2.

        :rtype: list
        """
        control_perimeters = []
        if self.drop_panel is None:
            # No column-head or drop-panel.
            u1 = self.construct_minimum_perimeter(
                self.slab.control_distance_factor*self.deff
                )
            control_perimeters.append(u1)
        else:
            # With column head or drop-panel.
            inparams, extparams = (self.drop_panel
                                       .resolve_control_perimeter_parameters())
            if inparams is None and extparams is None:
                raise ImplementationError(
                    4001, ("No control perimeters could be resolved from "
                           "the column's head.")
                )
            if inparams:
                control_perimeters.append(
                        self.construct_minimum_perimeter(distance=inparams[1],
                                                         shape=inparams[0],
                                                         deff=inparams[2])
                        )
            if extparams:
                control_perimeters.append(
                        self.construct_minimum_perimeter(distance=extparams[1],
                                                         shape=extparams[0])
                        )
        return control_perimeters

    def construct_minimum_perimeter(self, distance=1., shape=None, deff=None):
        """Calculate a control perimeter on the slab
        according to the provisions of §6.4.2. A control
        perimeter is defined in the vicinity of a column, at
        distances prescribed by the code. At any case, it
        should be constructed in a way that minimizes its length.
        See §6.4.2(1) for further details.

        :param float distance: The characteristic offset from
            the loading area that the column creates.
        :param shape: An explicit shape to use as the source
            geometry for the construction of the offset perimeter.
        :param deff: The effective depth at the control perimeter.
        :type deff: float or None
        :rtype: BasicControlPerimeter
        :raises ValueError: If the source shape of the perimeter
            is not contained within the slab.
        """
        source = shape or self
        if not self.slab.more.contains(source):
            raise CodedValueError(4002, "Source shape is not within the slab.")

        u1 = BasicControlPerimeter(
                self, shell=source.offset_convex_hull(
                    distance=distance
                    ), deff=deff
                )

        px, py = source.stretch_to_container(self.slab)
        pxy = PlanarShape(shell=px.union(py))

        # Control perimeter, in the case that the column
        # is classified as 'corner'
        u1xy = BasicControlPerimeter(
                self, position='corner', shell=pxy.offset_convex_hull(
                    distance=distance, intersect_with=self.slab
                    ), deff=deff
                )
        if isclose(pxy.area, self.area, rel_tol=1e-03):
            # Corner-column tangent to the slab-edges
            return u1xy

        # Control perimeters, in the case that the column
        # is classified as 'edge'
        u1x = BasicControlPerimeter(
                self, position='edgex', shell=px.offset_convex_hull(
                    distance=distance, intersect_with=self.slab
                    ), deff=deff
                )
        if isclose(px.area, self.area, rel_tol=1e-03):
            # Edge column tangent to the slab edge along y axis
            return u1x

        u1y = BasicControlPerimeter(
                self, position='edgey', shell=py.offset_convex_hull(
                    distance=distance, intersect_with=self.slab
                    ), deff=deff
                )
        if isclose(py.area, self.area, rel_tol=1e-03):
            # Edge column tangent to the slab edge along x axis
            return u1y

        return min((u1xy, u1x, u1y, u1), key=lambda u: u.length)

    @property
    def control_perimeters(self):
        """The traces of slab-sections in the vicinity of the
        column, where a check between punching shear capacity
        and design-value should be made.

        :rtype: tuple
        :return: A tuple of control perimeters.
        """
        if self._control_perimeters is None:
            self._control_perimeters = [self.u0] + self.basic_control_perimeters
        return self._control_perimeters

    @property
    def dcr0(self):
        """Demand to capacity ratio at perimeter `u0`
        on the sides of the column.

        :rtype: float
        """
        if self._dcr0 is None:
            self._dcr0 = self.u0.dcr
        return self._dcr0

    @property
    def dcri(self):
        """Demand to capacity ratio at perimeter
        `ui`,  i.e. the most-adverse basic control perimeter
        of the column.

        :rtype: float
        """
        if self._dcri is None:
            self._dcri = self.ui.dcr
        return self._dcri

    def recalculate_control_perimeters(self):
        """Update cache of `basic_control_perimeters`."""
        self._basic_control_perimeters = self._calculate_control_perimeters()

    @property
    def uouteff(self):
        """The effective outer perimeter where no
        shear reinforcement is required.

        :rtype: `LineString` or `MultiLineString`
        """
        return self._uouteff

    def set_drop_panel(self, factory=None, *args, **kwargs):
        """Set the value of the `drop_panel
        <dx_base.elements.RCColumn2D.drop_panel>` property to
        a `DropPanel` instance generated through
        the respective |create_as_column_offset| method.

        :param factory: The class that instantiates the drop-panel.
        :param \*args: Positional arguments of the wrapped method.
        :param \*\*kwargs: Keyword arguments of the wrapped method.
        """
        if factory is None:
            factory = DropPanel
        super().set_drop_panel(factory=factory, *args, **kwargs)

    def evaluate_min_Aswr(self, perimeter):
        """Evaluate the minimum required shear reinforcement per
        unit of length, according to Eq. (6.52).

        ``[m2/m]``

        :param BasicControlPerimeter perimeter:
        :rtype: float
        """
        vrdcs = perimeter.vrdcs * 1e-06
        vrdc = 0.75 * self.vrdc * 1e-06
        fywd = self.slab.fywd * 1e-06
        ui = perimeter.length
        alpha = self.shear.angle
        return (vrdcs - vrdc) / 1.5 / fywd / sin(alpha) * ui

    def to_json(self):
        """Create a json serializable output of the design results.

        :rtype: dict
        """
        warning = " (Maximum reinforcement ratio exceeded)"
        rhol = f'{self.rhol:.4f}'
        if self.rhol >= 0.02:
            rhol = f'{self.rhol:.4f}' + warning

        json_output = {
            'Position': self.ui.position,
            'Geometry': {
                'Centroid': {
                    'x [m]': float(f'{self.centroid.x:.3f}'),
                    'y [m]': float(f'{self.centroid.y:.3f}'),
                    },
                'Bounding box': {
                    'bx [mm]': float(f'{self.bx*1e+03:.1f}'),
                    'by [mm]': float(f'{self.by*1e+03:.1f}'),
                    }
                },
            'Effective depth [mm]': float(f'{self.deff*1e+03:.1f}'),
            'Tensile Reinforcement': {
                'Effective tensile region': {
                    'bx [mm]': float(
                        f'{self.tensile.effective_region.bx*1e+03:.1f}'
                        ),
                    'by [mm]': float(
                        f'{self.tensile.effective_region.bx*1e+03:.1f}'
                        ),
                    },
                'x-axis': f'{self.phix}',
                'y-axis': f'{self.phiy}',
                'ρx': f'{self.rhox:.4f}',
                'ρy': f'{self.rhoy:.4f}',
                'ρl': rhol,
                },
            }
        if self.tensile.effective_region.centroid != self.centroid:
            dx, dy = (np.array(self.tensile.effective_region.centroid) -
                     np.array(self.centroid))
            output = (json_output['Tensile Reinforcement']
                                 ['Effective tensile region'])
            output['Centroid (offset)'] = {
                'dx [mm]': f'{dx*1e+03:.1f}', 'dy [mm]': f'{dy*1e+03:.1f}'
                }
        if self.drop_panel:
            json_output['Drop panel'] = {
                'lx [mm]': float(f'{self.drop_panel.lx*1e+03:.1f}'),
                'ly [mm]': float(f'{self.drop_panel.ly*1e+03:.1f}'),
                'H [mm]': float(f'{self.drop_panel.height*1e+03:.1f}'),
                }
        json_output['Design'] = {**self.design()}
        return json_output

    def design(self):
        """Perform all the necessary design checks
        in the control perimeters of the column and
        collect results in a dictionary than can be
        easily transformed into json.

        :rtype: dict
        :return: A concise report with the results.
        """
        design_output = {}
        for i, ui in enumerate(self.control_perimeters):
            if i == 0:
                vrd = self.slab.vrdmax
            else:
                vrd = ui.vrdc

            perimeter_output = {
                'Most adverse loadcase': {
                    'name': ui.maxlc.LC,
                    'Ved [kN]': float(f'{ui.Ved*1e-03:.1f}'),
                    'Mex [kN.m]': float(f'{ui.maxlc.Mex*1e-03:.1f}'),
                    'Mey [kN.m]': float(f'{ui.maxlc.Mey*1e-03:.1f}'),
                    'ex [mm]': float(f'{ui.ex*1e+03:.1f}'),
                    'ey [mm]': float(f'{ui.ey*1e+03:.1f}'),
                    },
                'β': float(f'{ui.beta:.3f}'),
                'ved [kPa]': float(f'{ui.ved*1e-03:.1f}'),
                'vrd [kPa]': float(f'{vrd*1e-03:.1f}'),
                'DCR (ved/vrd)': f'{ui.dcr:.3f}'
                }
            if vrd < ui.ved:
                try:
                    self._uouteff, diag = self.evaluate_shear_cage_uouteff(
                        perimeter=ui
                        )
                    Aswrmin = self.evaluate_min_Aswr(ui)
                    self.set_shear_reinforcement(Aswrmin, self.uouteff.csx,
                                                 self.uouteff.csy)
                    reinforcement_data = {
                        'Basic': {
                            'Asw/sr [mm2@100mm]': float(
                                f'{self.shear.Aswr*1e+05:.1f}'
                                ),
                            'uout [mm]': float(f'{ui.uout*1e+03:.1f}'),
                            'uouteff [mm]': float(
                                f'{self.uouteff.length*1e+03:.1f}'
                                ),
                            'rout [mm]': float(f'{self.uouteff.r*1e+03:.1f}'),
                            'csx [mm]': float(
                                f'{2*self.uouteff.csx*1e+03:.1f}'
                                ),
                            'csy [mm]': float(
                                f'{2*self.uouteff.csy*1e+03:.1f}'
                                ),
                            }
                        }
                    if diag:
                        nmin, rmin, rmax, st, cs = diag
                        diag_cages = {}
                        diag_cages['nmin'] = f'{nmin:d}'
                        diag_cages['rmin0 [mm]'] = float(f"{rmin*1e+03:.1f}")
                        diag_cages['rmax0 [mm]'] = float(f"{rmax*1e+03:.1f}")
                        diag_cages['cs [mm]'] = float(f'{cs*1e+03:.1f}')
                        diag_cages['st [mm]'] = float(f'{st*1e+03:.1f}')
                        reinforcement_data['Diagonal'] = diag_cages

                except Exception as e:
                    reinforcement_data = str(e)

                perimeter_output['Shear Reinforcement'] = reinforcement_data
            design_output[f'Perimeter u{i}'] = perimeter_output

        return design_output

    def print(self, to_file=False):
        """Pretty print design output.

        :param bool to_file: If ``True`` prepare
            printout for saving in file.
        :rtype: str or None
        """
        printout = {
            f'Column "{self._id}"': {
                'Results': self.to_json()
                }
            }
        return print_dict(printout, to_file=to_file)


class DropPanel(ColumnDropPanel):

    @property
    def l1(self):
        """Maximum total breadth of the projection of the column head.

        ``[m]``

        :rtype: float
        """
        if self._l1 is None:
            self._l1 = max(2*self.lx+self.column.bx, 2*self.ly+self.column.by)
        return self._l1

    @property
    def l2(self):
        """Minimum total breadth of the projection of the column head.

        ``[m]``

        :rtype: float
        """
        if self._l2 is None:
            self._l2 = min(2*self.lx+self.column.bx, 2*self.ly+self.column.by)
        return self._l2

    def resolve_control_perimeter_parameters(self):
        """Drop panels affect the calculation of the control
        perimeters around the column. Depending on the relation
        between the height of the drop-panel and its offset distances
        from the column, the source-shape of the control perimeter may
        change, and the same applies for its distance from the
        source-shape.

        This method determines the source-shape of the control perimeter,
        and the distance of the latter from the source-shape, both
        for any possible internal (i.e. within the limits of the
        column's head) control section, and for an external
        control section.

        :rtype: tuple
        :return: ``((shape, distance)_internal, (shape, distance)_external)``
        """
        dH = self.height + self.column.deff
        factor = self.column.slab.control_distance_factor
        if self.lx < factor*self.height or self.ly < factor*self.height:
            external = (self.column,
                        min(self.lx, self.ly)+factor*self.column.deff)
            internal = None
        else:
            external = (self.column,
                        min(self.lx, self.ly)+factor*self.column.deff)
            internal = (self.column, factor*dH, dH)
        return internal, external

    @property
    def annotation_text(self):
        """Text to be used for the annotation
        of drop-panels on a plot.

        :rtype: str
        """
        return ("$l_x$ = %.3f\n$l_y$ = %.3f\n$h_H$ = %.3f" %
                (self.lx, self.ly, self.height))
