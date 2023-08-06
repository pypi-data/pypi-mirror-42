# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
"""Classes and functions to represent control perimeters
that pertain to the design of slabs against punching shear.
"""
import numpy as np

from math import isclose, sqrt
from shapely.ops import linemerge
from shapely.affinity import translate
from shapely.geometry import LineString, Point, Polygon

from dx_utilities.geometry import PlanarShape, LinearShape
from dx_utilities.integrals import line_moment
from dx_utilities.exceptions import CodedValueError, CodedException
from dx_utilities import INF


__all__ = ['ControlPerimeter', 'ColumnPerimeter', 'BasicControlPerimeter',
           'ShearCagePerimeter']


class ControlPerimeter(PlanarShape):
    """A class representing control perimeters of a slab-column.
    The length of the resulting shapes is evaluated as the length
    of the difference of their boundary with the boundary of the
    slab.

    :param Column column: The parent column object.
    :param beta: The design stress factor.
    :type beta: None or float
    :param betai: The design stress factor for each load-case
        considered.
    :type betai: `None` or `numpy.array`
    :param deff: The effective depth of the slab in the vicinity
        of the parent column.
    :type deff: None or float
    :param \*args: Positional arguments in parent class.
    :param \*\*kwargs: Key-word arguments in parent class.
    """
    def __init__(self, column=None, beta=None, betai=None, deff=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._beta = beta
        self._betai = betai
        self.column = column
        self._ex = None
        self._ey = None
        self._exi = None
        self._eyi = None
        self._length = None
        self._path = None
        self._path_local = None
        self._Wx = None
        self._Wy = None
        self._ved = None
        self._Ved = None
        self._sigmacp = None
        self._vrdc = None
        self._dcr = None
        self._dVed = None
        self._dVedi = None
        self._Vedi = None
        self._vedi = None
        self._sigmacpi = None
        self._vrdci = None
        self._maxlci = None
        self._deff = deff

    @property
    def deff(self):
        """Effective depth at the control perimeter. It is inherited
        from the parent column.

        ``[m]``

        :rtype: float
        """
        if self._deff is None:
            self._deff = self.column.deff
        return self._deff

    @property
    def maxlci(self):
        """Return the index of the most adverse loadcase. That is
        the loadcase resulting in the largest effective shear stress.

        :rtype: int
        """
        if self._maxlci is None:
            self._maxlci = np.argmax(self.vedi)
        return self._maxlci

    @property
    def maxlc(self):
        """Return the most adverse load-case.

        :rtype: InternalForces
        """
        return self.column.load_cases[self.maxlci]

    @property
    def dVed(self):
        """Favourable vertical force on account of
        a single-valued, uniform soil-pressure acting on a
        foundation slab or footing.

        ``[N]``

        :rtype: float
        """
        if self._dVed is None:
            self._dVed = self.evaluate_dVed()
        return self._dVed

    @property
    def dVedi(self):
        """Favourable vertical force on account of
        soil pressure acting on a foundation slab
        or footing for all loadcases.

        ``[N]``

        :rtype: `numpy.array`
        """
        if self._dVedi is None:
            self._dVedi = self.evaluate_dVedi()
        return self._dVedi

    @property
    def Vedi(self):
        """Array of effective shear forces,
        with respect to the specified loadcases.

        ``[N]``

        :rtype: `numpy.array`
        """
        if self._Vedi is None:
            self._Vedi = self.evaluate_Vedi()
        return self._Vedi

    @property
    def dcr(self):
        """Demand-to-capacity ratio. That is, the
        ratio between the most adverse design stress
        among the load-cases specified, and the
        shear stress capacity of the concrete slab
        without shear-reinforcement.

        :rtype: float
        """
        if self._dcr is None:
            self._dcr = self.ved / self.vrdc
        return self._dcr

    @property
    def beta(self):
        """The design stress factor corresponding to the most adverse
        load-case.

        :rtype: float
        """
        if self._beta is None:
            self._beta = self.betai[self.maxlci]
        return self._beta

    @beta.setter
    def beta(self, value):
        self._beta = value

    @property
    def betai(self):
        """An array of design stress factors, with respect to
        the specified load-cases.

        :rtype: `numpy.array`
        """
        if self._betai is None:
            self._betai = np.ones(self.column.nlc)
        return self._betai

    @betai.setter
    def betai(self, value):
        self._betai = value

    @property
    def sigmacpi(self):
        """Favourable compressive stresses acting on
        the plane of the parent slab, for
        the specified load-cases.

        Evaluated according to §6.4.4(1).

        ``[Pa]``

        :rtype: float
        """
        if self._sigmacpi is None:
            self._sigmacpi = np.zeros(self.column.nlc)
        return self._sigmacpi

    @property
    def sigmacp(self):
        """Compressive stress acting on
        the plane of the parent slab for the most adverse
        loadcase. This has a favourable effect in the shear
        capacity.

        Evaluated according to §6.4.4(1).

        ``[Pa]``

        :rtype: float
        """
        if self._sigmacp is None:
            self._sigmacp = self.sigmacpi[self.maxlci]
        return self._sigmacp

    @property
    def vrdci(self):
        """Shear capacity on the control perimeter
        for all the load-cases specified.

        ``[Pa]``

        :rtype: `numpy.array`
        """
        if self._vrdci is None:
            self._vrdci = self.sigmacpi + self.column.vrdc
        return self._vrdci

    @property
    def vrdc(self):
        """Shear capacity on the control perimeter.

        ``[Pa]``

        :rtype: float
        """
        if self._vrdc is None:
            self._vrdc = self.vrdci[self.maxlci]
        return self._vrdc

    @property
    def exi(self):
        """Eccentricity of the shear load along the **x**-axis,
        for all the specified load-cases.

        ``[m]``

        :rtype: `numpy.array`
        """
        if self._exi is None:
            self._update_eccentricities()
        return self._exi

    @property
    def eyi(self):
        """Eccentricity of the shear load along the **y**-axis,
        for all the specified load-cases.

        ``[m]``

        :rtype: `numpy.array`
        """
        if self._eyi is None:
            self._update_eccentricities()
        return self._eyi

    @property
    def ex(self):
        """Eccentricity of the most adverse shear-load
        along the **x**-axis.

        ``[m]``

        :rtype: float
        """
        if self._ex is None:
            self._ex = self.exi[self.maxlci]
        return self._ex

    @property
    def ey(self):
        """Eccentricity of the most adverse shear-load
        along the **y**-axis.

        ``[m]``

        :rtype: float
        """
        if self._ey is None:
            self._ey = self.eyi[self.maxlci]
        return self._ey

    @property
    def vedi(self):
        """Design shear stress on the control perimeter,
        for all load-cases specified.

        ``[Pa]``

        :rtype: `numpy.array`
        """
        if self._vedi is None:
            self._vedi = self.evaluate_vedi()
        return self._vedi

    @property
    def ved(self):
        """Design shear stress on the control perimeter.

        ``[Pa]``

        :rtype: float
        """
        if self._ved is None:
            self._ved = self.vedi[self.maxlci]
        return self._ved

    @property
    def Ved(self):
        """Effective shear force transferred from the column
        to the slab along the control perimeter.

        It derives from the most adverse load-case.

        ``[N]``

        :rtype: float
        """
        if self._Ved is None:
            self._Ved = self.Vedi[self.maxlci]
        return self._Ved

    def _update_eccentricities(self):
        self._exi = np.zeros(self.column.nlc)
        self._eyi = np.zeros(self.column.nlc)
        index = self.Vedi > 0.
        self._exi[index] = -self.column.Meyi[index] / self.Vedi[index]
        self._eyi[index] = +self.column.Mexi[index] / self.Vedi[index]
        if self.column.slab.foundation or self.column.floating:
            self._exi *= -1
            self._eyi *= -1
        self._betai = None

    @property
    def path(self):
        """The path of the control perimeter.

        :rtype: dx_utilities.geometry.linear.LinearShape
        """
        if self._path is None:
            self._update_path()
        return self._path

    def _update_path(self):
        """Update the geometric path of the perimeter."""
        self._path = self.boundary.intersection(self.column.slab.less)
        try:
            self._path.geoms
            self._path = linemerge(self._path)
            if self._path.geoms:
                self._path = max(self._path.geoms, key=lambda g: g.length)
        except AttributeError:
            # Keep the first calculation and swallow
            # the exception
            pass
        self._path = LinearShape(coordinates=np.array(self._path))

    @property
    def path_local(self):
        """The path of the control perimeter represented in the
        local coordinate system.

        The origin of the local coordinate system coincides
        by default with the column's centroid.

        :rtype: LineString
        """
        if self._path_local is None:
            self._path_local = self.evaluate_local_path()
        return self._path_local

    @property
    def length(self):
        """The length of the perimeter.

        ``[m]``

        :rtype: float
        """
        if self._length is None:
            self._length = self.path.length
        return self._length

    @property
    def Wx(self):
        """Perimeter modulus about **x**-axis. See Eq. (6.40).

        ``[m2]``

        :rtype: float
        """
        if self._Wx is None:
            self._Wx = self.path_modulus()
        return self._Wx

    @property
    def Wy(self):
        """Perimeter modulus about **y**-axis. See Eq. (6.40)

        :rtype: float
        """
        if self._Wy is None:
            self._Wy = self.path_modulus(axis='y')
        return self._Wy

    def evaluate_local_path(self, origin=None):
        """Represent the path of the control perimeter in a local
        coordinate-system with the column centroid as origin, unless
        otherwise specified.

        :param Point origin: The origin of the
            local coordinate system.
        :rtype: LineString
        """
        if origin is None:
            origin = self.column.centroid
        return translate(self.path, -origin.x, -origin.y)

    def recache_local_path(self, origin=None):
        """Re-evaluate local path with reference to the
        column's centroid, or any other origin point explicitly
        specified. The path moduli `Wx` and `Wy` are also
        re-evaluated.
        """
        self._path_local = self.evaluate_local_path(origin)
        self._Wx = self.path_modulus(axis='x')
        self._Wy = self.path_modulus(axis='y')

    def path_modulus(self, axis='x'):
        """Evaluate the first-order line moment of this control perimeter
        about the specified axis. The reference coordinate system is the
        local coordinate system of the column, with its centroid as the
        system's origin.

        ``[m2]``

        :param str axis: The local axis to use as reference for the
            evaluation of the modulus.
        :rtype: float
        """
        if axis.lower() == 'x':
            ref = (1., 0.)
        elif axis.lower() == 'y':
            ref = (0., 1.)
        else:
            raise CodedValueError(4004, 'Unrecognized axis label %s' % axis)

        return line_moment(self.path_local, ref)

    def evaluate_vedi(self):
        """Evaluate the design value of the punching-shear stress
        along the control-perimeter according to Eq. (6.38), for
        all load-cases specified in the parent column.

        :rtype: `numpy.array`
        """
        betai = self.betai
        ui = self.length
        Vedi = self.Vedi
        d = self.deff
        self._vedi = betai * (Vedi/ui/d)
        return self._vedi

    def evaluate_dVedi(self):
        """Evaluate the favourable vertical forces acting
        on the perimeter due to soil pressure, for all
        load-cases specified in the parent column. Applicable
        to slab foundations, and footings.

        The weight of the concrete material, as well as
        the weight of any panel that might present, are
        subtracted from the force evaluated from the
        soil pressure.

        ``[N]``

        :rtype: `numpy.array`
        """
        column = self.column
        dVedi = np.zeros(column.nlc)
        if column.slab.foundation and column.slab.sp_index:
            for i, lc in enumerate(self.column.load_cases):
                pressure = column.slab.sp_index.get(lc.LC)
                if pressure is None:
                    continue
                else:
                    try:
                        dVedi[i] += pressure.query_avg(self) * self.area
                    except AttributeError:
                        dVedi[i] += pressure.value * self.area
            dVedi -= self.area * column.slab.thickness * column.slab.material.w
        if column.drop_panel:
            panel = column.drop_panel
            area = min(panel.area, self.area)
            dVedi -= area * panel.height * column.slab.material.w
        dVedi[dVedi < 0.] = 0.
        return dVedi

    def evaluate_dVed(self):
        """Evaluate any favourable vertical force on account of
        a single-valued, uniform soil-pressure acts on the
        base of the slab.

        This applies only to foundation slabs, on account
        of the underlying soil pressure.

        :rtype: float
        """
        column = self.column
        dVed = 0.
        if column.slab.foundation and not isclose(column.soil_pressure, 0.):
            dVed += column.soil_pressure * self.area
            dVed -= self.area * column.slab.thickness * column.slab.material.w
            if column.drop_panel:
                panel = column.drop_panel
                area = min(panel.area, self.area)
                dVed -= area * panel.height * column.slab.material.w
        return max(dVed, 0.)

    def evaluate_Vedi(self):
        """Evaluate the effective shear forces acting on the perimeter,
        for all load-cases specified in the parent column. The evaluation
        takes into account any favourable effect of soil pressure.

        ``[N]``

        :rtype: `numpy.array`
        """
        if np.allclose(self.dVedi, np.zeros(self.column.nlc)):
            Vedi = self.column.Vedi - self.dVed
        else:
            Vedi = self.column.Vedi - self.dVedi
        Vedi[Vedi < 0.] = 0.
        return Vedi


class BasicControlPerimeter(ControlPerimeter):
    """A class representing basic control perimeters of a slab-column.
    The length of the resulting shapes is evaluated as the length
    of the difference of their boundary with the boundary of the
    slab.

    :param Column column: The parent column object.
    :param str position: Position of the parent column
        implied by the generation of this control
        perimeter. Valid values are::

            ('internal', 'edgex', 'edgey', 'corner')

    :param \*args: Positional arguments in parent class.
    :param \*\*kwargs: Key-word arguments in parent class.
    """

    def __init__(self, *args, position='internal', **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
        self._truncated = None
        self._uout = None

    @property
    def betai(self):
        """An array of design stress factors, with respect to
        the specified load-cases.

        :rtype: `numpy.array`
        """
        if self._betai is None:
            self._betai = self.evaluate_betai(**self.column.slab.beta_config)
        return self._betai

    @property
    def vrdcs(self):
        """Minimum shear capacity of the slab
        on the perimeter assuming presence of
        shear reinforcement.

        ``[Pa]``

        :rtype: float
        """
        return self.ved

    @property
    def uout(self):
        """Theoretical length of the outer perimeter where
        no shear-reinforcement is required.

        ``[m]``

        :rtype: float
        """
        if self._uout is None:
            self._uout = self.beta*self.Ved/self.vrdc/self.deff
        return self._uout

    @property
    def path(self):
        """The path of the control perimeter.

        :rtype: LineString
        """
        if self._path is None:
            if self.position == 'internal':
                self._path = self.boundary
                return self._path
            super()._update_path()
        return self._path

    @property
    def truncated(self):
        """Calculate the truncated control perimeter
        for edge- and corner- columns according to the
        provisions of §6.4.3(4).

        :rtype: LineString
        """
        if self._truncated is None:
            self._truncated = self._truncate_path()
        return self._truncated

    def _truncate_path(self):
        """Truncate path on the intersections with the lines
        passing through the truncating point of the column that
        are parallel to the edges of the slab.

        :rtype: LineString
        """
        T = self.column.truncate_point
        column_projections = self.column.slab.project_to_boundary(T)
        # Filter only projections contained in the perimeter
        projections = []
        for point, ldir in column_projections:
            p = Point(point)
            if self.more.intersects(p):
                projections.append((point, ldir))

        if not projections:
            raise Exception(('Perimeter area does not contain projections '
                             'of the truncated point.'))

        if len(projections) > 2:
            projections = [projections[0], projections[-1]]

        # Construct truncating lines
        truncating_lines = []
        bounds = []
        for point, ldir in projections:
            line = LineString([T+INF*ldir, T-INF*ldir])
            xpoints = line.intersection(self.path)
            try:
                bounds.extend(xpoints)
            except TypeError:
                # intersection return a single point
                bounds.append(xpoints)

        # Derive bounding points on the path
        distances = sorted([self.path.project(Point(p), True) for p in bounds])
        smin, smax = distances[0], distances[-1]
        return self.path.truncate(smin, smax)

    def evaluate_betai(self, approximate=False, simplified=False):
        """Evaluate the factor β that increases
        the punching-shear stress in the presence of eccentricity,
        for all load-cases. See Eq. (6.38).

        :param bool approximate: Use approximate expressions where
            applicable.
        :param bool simplified: Use explicit values in §6.4.3(6)
        :rtype: np.ndarray
        """
        if simplified:
            return np.ones(self.column.nlc) * self.evaluate_beta_simplified()

        if self.position == 'internal':
            vsi = self.evaluate_vsi(approximate)
            u1 = self.path
            d = self.column.deff
            betai = 1. + vsi*d*u1.length/self.Vedi
            betai[betai == np.inf] = 1.
            return betai

        if self.position in {'edgex', 'edgey'}:
            return self.evaluate_betai_edge()

        if self.position == 'corner':
            return self.evaluate_betai_corner()

    def evaluate_beta_simplified(self):
        """Set the value of β following the simplified
        provisions of §6.4.3(6).

        :rtype: float
        :raises CodedValueError: If the position of the column is
            not recognized.
        """
        if self.position == 'internal':
            return 1.15
        elif self.position in {'edgex', 'edgey'}:
            return 1.4
        elif self.position == 'corner':
            return 1.5
        else:
            raise CodedValueError(4005, (f'Inconsistent column position '
                                         f'{self.position}'))

    def evaluate_betai_corner(self, approximate=False):
        """Evaluate the factor β in Eq. (6.38) for corner columns
        according to §6.4.3(5), for all load-cases specified.

        :param bool approximate: If `True` use simplified expressions
            where applicable.
        :rtype: `numpy.array`
        :raises CodedValueError: If the position of the perimeter is
            not on a corner of the slab.
        """
        if self.position != 'corner':
            raise CodedValueError(4006, (f'Inconsistent column position '
                                         f'{self.position}'))

        rcx, rcy = self.column.relative_centroid
        u1 = self.path
        u1star = self.truncated
        betai = np.ones(self.column.nlc) * u1.length / u1star.length

        # Strong condition to ensure that the column load is
        # eccentric toward the exterior of the slab
        eccentricity_toward_exterior = np.logical_and(
            rcx * self.exi > 0, rcy * self.eyi > 0
            )
        # For these cases use Eq. (6.39)
        vsi = self.evaluate_vsi(approximate)
        index = eccentricity_toward_exterior
        betai[index] = 1. + (vsi[index]*self.column.deff*u1.length/self.Vedi[index])
        betai[betai == np.inf] = 1.

        # Handle cases with no eccentricity
        bMomenti = self.column.bMomenti & 3
        betai[bMomenti == 0] = 1.
        return betai

    def evaluate_betai_edge(self, approximate=False):
        """Evaluate the factor β in Eq. (6.38) for edge columns
        according to §6.4.3(4), for all specified loadcases.

        :param bool approximate: If `True` use simplified expressions
            where applicable.
        :rtype: `numpy.array`
        :raises CodedValueError:
            If the position of the perimeter is
            not on the edges of the slab.
        """
        if self.position not in {'edgex', 'edgey'}:
            raise CodedValueError(4007, (f'Inconsistent column position '
                                         f'{self.position}'))

        # Aliasing for consistency with the code
        # variables
        u1 = self.path.length
        u1star = self.truncated.length
        d = self.column.deff
        Vedi = self.Vedi
        Mexi, Meyi = map(np.abs, (self.column.Mexi, self.column.Meyi))
        beta0 = u1 / u1star
        rcx = self.column.relative_centroid[0]
        rcy = self.column.relative_centroid[1]
        if self.position == 'edgex':
            eccentricity_toward_exterior = rcx*self.exi >= 0
            # Eccentricity toward slab interior
            c1 = self.column.bx
            c2 = self.column.by
            k644 = self.column.k639(c1/c2/2)
            betai = beta0 + k644*(u1/self.Wx)*(Mexi/Vedi)
        elif self.position == 'edgey':
            eccentricity_toward_exterior = rcy*self.eyi >= 0
            # Eccentricity toward slab interior
            c1 = self.column.by
            c2 = self.column.bx
            k644 = self.column.k639(c1/c2/2)
            betai = beta0 + k644*(u1/self.Wy)*(Meyi/Vedi)

        if np.any(eccentricity_toward_exterior):
            beta0 = 1.
            self.recache_local_path(origin=self.path.centroid)
            vsi = self.evaluate_vsi(approximate)
            beta1 = vsi*d*u1/Vedi
            index = eccentricity_toward_exterior
            betai[index] = beta0 + beta1[index]

        # When Vedi == 0. betai should reduce to 1.
        betai[betai == np.inf] = 1.

        # Handle cases with no eccentricity
        bMomenti = self.column.bMomenti & 3
        betai[bMomenti == 0] = 1.
        return betai

    def evaluate_vsi(self, approximate=False):
        """Evaluate the design value of the component of the shear
        stress that balances any existing moment along the perimeter
        in consistency with Eq. (6.39), for all loadcases specified.

        The problem resolves in calculating the moment
        that is balanced by shear stress :math:`\\text{v}_s`
        along the perimeter, assuming uniform distribution as
        presented in Fig. 6.19. For uni-axial eccentricity
        the moment balanced by shear, :math:`M_s`, is given by:

        :math:`M_s = \\text{v}_sW_1 = kM_{ed}`,

        where :math:`k` is the factor quantified in Table 6.1,
        and :math:`W_1` the line-integral presented in Eq. (6.40).
        The latter is evaluated numerically using the data
        on the geometry of the control perimeter.

        For bi-axial eccentricity we use the following expression:

        :math:`\\text{v}_s = \sqrt{\\frac{k_xM_{edx}}{W_x}^2 + \\frac{k_yM_{edy}}{W_y}^2}`

        .. vs = √((kx*Medx/Wx)**2 + (ky*Medy/Wy)**2)

        :param bool approximate: Use approximate expressions where
            applicable.
        :rtype: `numpy.array`
        """
        bending = self.column.bMomenti & 3

        vsxi, vsyi = np.zeros(self.column.nlc), np.zeros(self.column.nlc)
        # Aliasing for consistency with the code
        # variables
        Mexi, Meyi = map(np.abs, (self.column.Mexi, self.column.Meyi))
        kx, ky = self.column.kx, self.column.ky
        u1 = self.path.length
        d = self.column.deff

        vsxi = kx*Mexi/self.Wx/d
        vsyi = ky*Meyi/self.Wy/d

        vsi = np.sqrt(vsxi**2 + vsyi**2)
        vsi[bending == 0] = 0.
        if approximate:
            index = bending == 3
            vsi[index] = 1.8/u1/d * np.sqrt(
                (Mexi[index]/self.by)**2 + (Meyi[index]/self.bx)**2
                )
        return vsi


class ColumnPerimeter(BasicControlPerimeter):
    """Represent the control perimeter at the sides
    of the column. The length is evaluated according to
    the provisions of §6.4.5(3).
    """

    @property
    def dcr(self):
        """Demand-to-capacity ratio. That is,
        the ratio between the most adverse shear stress
        and the maximum allowable stress ``vRd,max``.
        See Eq. (6.53).

        :rtype: float
        """
        if self._dcr is None:
            self._dcr = self.ved / self.column.slab.vrdmax
        return self._dcr

    @property
    def length(self):
        """Effective length according to
        the provisions of §6.4.5(3)

        ``[m]``

        :rtype: float
        """
        if self._length is None:
            self._length = self._evaluate_effective_length()
        return self._length

    def _evaluate_effective_length(self):
        """Evaluate the effective length according to
        the provisions of §6.4.5(3)

        :rtype: float
        """
        if self.column.position == 'internal':
            return super().length

        if self.column.position == 'edgex':
            return self.by + 2*min(self.bx, 1.5*self.column.deff)

        if self.column.position == 'edgey':
            return self.bx + 2*min(self.by, 1.5*self.column.deff)

        if self.column.position == 'corner':
            return min(self.bx+self.by, 3*self.column.deff)


class ShearCagePerimeter(object):
    """Outer perimeter in which no reinforcement
    is required, when the slab is reinforced against
    punching shear using shear cages.

    :param geometry: The geometry of the perimeter.
    :type geometry: LineString or MultiLineString.
    :param float ad: The length of the linear segment
        that connects the farthest perimeters between
        two consecutive (clockwise) shear cages.
    :param float r: The farthest distance of the cage from the
        sides of the column.
    :param float csx: The half-breadth of the shear cage that extends
        along the x-axis.
    :param float csy: The half-breadth of the shear cage that extends
        along the y-axis.
    """

    def __init__(self, geometry, ad, r, csx, csy):
        self.geometry = geometry
        self.ad = ad
        self.length = self.geometry.length
        self.r = r
        self.csx = csx
        self.csy = csy
