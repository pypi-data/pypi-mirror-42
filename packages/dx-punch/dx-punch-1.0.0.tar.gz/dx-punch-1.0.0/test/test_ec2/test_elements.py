import numpy as np
import unittest.mock as mock

from shapely.geometry import LineString

from test import DXTestCase

from math import pi, atan, sqrt
from numpy.testing import assert_allclose

from dx_punch.EC2 import (Slab, Column, DropPanel, BasicControlPerimeter,
                          ControlPerimeter)
from dx_base.exceptions import ImplementationError
from dx_eurocode.EC2.materials import RC
from dx_utilities.geometry import PlanarShape
from dx_utilities.units import inverse_transform_value, transform_value


class TestSlab(DXTestCase):

    def test_control_distance_factor(self):
        slab = Slab.create_circle(r=1., theta=atan(1./3.))
        self.assertAlmostEqual(slab.control_distance_factor, 3.)

    def test_Aswrtmin(self):
        slab = Slab(fyk=500., material=RC[16])
        expected = 0.08 * sqrt(16) / 500
        self.assertAlmostEqual(slab.Aswrtmin, expected)


class TestColumnSlab(DXTestCase):

    def _calculate_theoretical_length(self, conf, distance):
        """Calculate  the theoretical length of the simplest control
        perimeter around a column, at a specified distance.

        :param dict conf: The column configuration. Should include
            ``'shape'`` keyword and the characteristic dimensions:
            ``('bx', 'by')`` for rectangular shapes, and ``'r'``
            for circular shapes.
        :param float distance: The distance of the perimeter from the
            column faces.
        :rtype: float
        """
        if conf['shape'] == 'rectangle':
            bx, by = conf['bx'], conf['by']
            area = (bx + 2*distance)*(by + 2*distance) - (4 - pi)*distance**2
            length = 2*bx + 2*by + 2*pi*distance
        elif conf['shape'] == 'circle':
            r = conf['r']
            area = pi*(r + distance)**2
            length = 2*pi*(r+distance)
        else:
            area, length = None, None

        return length, area

    def setUp(self):
        self.slab_configuration = {
                'bx': 6000., # breadth along local x axis
                'by': 6000., # breadth along local y axis
                'thickness': 200.,
                'position': 'lower-left'
                }

        self.columns = [
                {
                    'shape': 'rectangle',
                    'bx': 300.,
                    'by': 300.,
                    'position': 'lower-left',
                    'origin': (1000., 1000.)
                    },
                {
                    'shape': 'rectangle',
                    'bx': 300.,
                    'by': 300.,
                    'position': 'lower-left',
                    'origin': (4700., 1000.)
                    },
                {
                    'shape': 'rectangle',
                    'bx': 300.,
                    'by': 300.,
                    'position': 'lower-left',
                    'origin': (4700., 4700.)
                    },
                {
                    'shape': 'rectangle',
                    'bx': 300.,
                    'by': 300.,
                    'position': 'lower-left',
                    'origin': (1000., 4700.)
                    },
                {
                    'shape': 'circle',
                    'r': 150.,
                    'center': (3000., 3000.)
                    },
                ]

        self.slab = Slab.create_rectangle_by_dimensions(
                **self.slab_configuration
                )
        for column_conf in self.columns:
            self.slab.add_column(**column_conf)

    def test_relative_centroid(self):
        c = self.slab.columns[0]
        expected = np.array([-1850., -1850.])
        assert_allclose(c.relative_centroid, expected)

    def test_valid_test_case(self):
        self.assertGreater(self.slab.area, 0.)
        self.assertGreater(self.slab.thickness, 0.)
        self.assertEqual(len(self.slab.columns), len(self.columns))
        self.assertTrue(all([c.area > 0. for c in self.slab.columns]))

    def test_instantiation(self):
        for c in self.slab.columns:
            self.assertEqual(c.slab, self.slab)

    def test_construct_minimum_perimeter_internal(self):
        c = self.slab.columns[0]
        distance = 150.
        p = c.construct_minimum_perimeter(distance)

        self.assertTrue(p.contains(c))
        self.assertGreater(p.area, c.area)

        self.assertFalse(p.difference(c).is_empty)
        self.assertTrue(c.difference(p).is_empty)

        self.assertAlmostEqual(p.hausdorff_distance(c), distance)

        for i, conf in enumerate(self.columns):
            p = self.slab.columns[i].construct_minimum_perimeter(distance)
            expected_length, expected_area = self._calculate_theoretical_length(
                    conf, distance
                    )
            self.assertAlmostEqual(p.length, expected_length,
                                   delta=0.001*expected_length, msg=conf)
            self.assertAlmostEqual(p.area, expected_area,
                                   delta=0.001*expected_area, msg=conf)

    def test_construct_minimum_perimeter_edge(self):
        """Test the calculation of the critical perimeter of
        a rectangular column, that should be classified as
        'edge' column, according to EC2 provisions. The conditions
        that yield this classification can be summarized as follows:

            1. ``2*bx + by + 2*cex + d*π < 2*(bx+by) + 2*d*π``
            2. ``2*bx + by + 2*cex + d*π < 2*by + bx + 2*cey + d*π``
            3. ``2*bx + by + 2*cex + d*π < by + bx + cey + cex + d*π/2``

        where the underlying variables are defined as follows

            * ``bx``, ``by`` denote the column's breadth along the x-, and
              y-direction respectively,
            * ``cex``, ``cey`` denote the shortest distances from the column's
              boundary to the slab-boundary, in the x- and y-direction
            * ``d``, is the distance of the control perimeter from the
              column's boundary.

        Apparently, the combinations represent the case that the edge is perpendicular
        to the x-direction. Nevertheless, if we interchange ``cex`` with ``cey``
        the conditions would represent the case where the edge is perpendicular
        to the y-direction. Hence, the two cases are completely equivalent, for
        the purposes of this calculation.

        We test the following combination of parameter-values:

            * ``bx`` = ``by`` = 1.
            * ``cex`` = 1.
            * ``cey`` = 4.
            * ``d`` = 1.2

        It can be readily verified that this combination satisfies the
        conditions (1)-(3).
        """
        slab = Slab.create_rectangle_by_dimensions(
                10., 10., position='lower-left'
                )
        bx = 1.
        by = 1.
        cex = 1.
        cey = 4.
        slab.add_column(bx=bx, by=by, origin=(slab.bx-bx-cex, cey),
                        position='lower-left')

        d = 1.2
        column = slab.columns[0]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = 2*bx + by + 2*cex + d*pi
        self.assertAlmostEqual(
                u1.boundary.difference(slab.boundary).length, expected_length,
                delta=0.001*expected_length
                )

    def test_construct_minimum_perimeter_corner(self):
        """Test the calculation of the critical perimeter of
        a rectangular column, that should be classified as
        'corner' column, according to EC2 provisions. The conditions
        that yield this classification can be summarized as follows:

            1. ``by + bx + cey + cex + d*π/2 < 2*bx + by + 2*cex + d*π``
            2. ``by + bx + cey + cex + d*π/2 < 2*by + by + 2*cey + d*π``
            3. ``by + bx + cey + cex + d*π/2 < 2*(bx+by) + 2*d*π``

        where the underlying variables are defined as follows

            * ``bx``, ``by`` denote the column's breadth along the x-, and
              y-direction respectively,
            * ``cex``, ``cey`` denote the shortest distances from the column's
              boundary to the slab-boundary, in the x- and y-direction
            * ``d``, is the distance of the control perimeter from the
              column's boundary.

        We test the following combination of parameter-values:

            * ``bx`` = ``by`` = 1.
            * ``cex`` = 1.
            * ``cey`` = 1.
            * ``d`` = 1.

        It can be readily verified that this combination satisfies the
        conditions (1)-(3).
        """
        slab = Slab.create_rectangle_by_dimensions(
                10., 10., position='lower-left'
                )
        bx = 1.
        by = 1.
        cex = 1.
        cey = 1.
        slab.add_column(bx=bx, by=by, origin=(slab.bx-bx-cex, cey),
                        position='lower-left')

        d = 1.
        column = slab.columns[0]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = bx + by + cex + cey + d*pi/2.
        self.assertAlmostEqual(
            u1.boundary.difference(slab.boundary).length, expected_length,
            delta=0.001*expected_length
            )

        # Add a tangent column
        slab.add_column(bx=bx, by=by, position='lower-left')
        column = slab.columns[1]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = bx + by + d*pi/2.
        self.assertAlmostEqual(
            u1.boundary.difference(slab.boundary).length, expected_length,
            delta=0.001*expected_length
            )
        position = 'corner'
        self.assertEqual(u1.position, position)

    def test_construct_minimum_perimeter_corner_circle(self):
        """Test the calculation of the critical perimeter of
        a circular column, that should be classified as
        'corner' column, according to EC2 provisions. The conditions
        that yield this classification can be summarized as follows:

            1. ``2*r + cex + cey + (r+d)*π/2 < 2*r + 2*cex + (r+d)*π``
            2. ``2*r + cex + cey + (r+d)*π/2 < 2*r + 2*cey + (r+d)*π``
            3. ``2*r + cex + cey + (r+d)*π/2 < 2*(r+d)*π``

        where the underlying variables are defined as follows

            * ``r`` denotes the radius of the column.
            * ``cex``, ``cey`` denote the shortest distances from the column's
              boundary to the slab-boundary, in the x- and y-direction
            * ``d``, is the distance of the control perimeter from the
              column's boundary.

        We test the following combination of parameter-values:

            * ``r`` =  0.5
            * ``cex`` = 0.5
            * ``cey`` = 0.5
            * ``d`` = 1.

        It can be readily verified that this combination satisfies the
        conditions (1)-(3).
        """
        slab = Slab.create_rectangle_by_dimensions(
                10., 10., position='lower-left'
                )
        r = 0.5
        cex = 0.5
        cey = 0.5
        slab.add_column(shape='circle', r=r, center=(slab.bx-r-cex, cey+r))

        d = 1.
        column = slab.columns[0]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = 2*r + cex + cey + (r+d)*pi/2.
        self.assertAlmostEqual(
                u1.boundary.difference(slab.boundary).length, expected_length,
                delta=0.001*expected_length
                )

    def test_construct_minimum_perimeter_corner_edge(self):
        """Test the calculation of the critical perimeter of
        a circular column, that should be classified as
        'corner' column, according to EC2 provisions. The conditions
        that yield this classification can be summarized as follows:

            1. ``2*r + 2*cex + (r+d)*π < 2*r + cex + cey + (r+d)*π/2``
            2. ``2*r + 2*cex + (r+d)*π < 4*r + 2*cey + (r+d)*π``
            3. ``2*r + 2*cex + (r+d)*π < 2*(r+d)*π``

        where the underlying variables are defined as follows

            * ``r`` denotes the radius of the column.
            * ``cex``, ``cey`` denote the shortest distances from the column's
              boundary to the slab-boundary, in the x- and y-direction
            * ``d``, is the distance of the control perimeter from the
              column's boundary.

        We test the following combination of parameter-values:

            * ``r`` =  0.5
            * ``cex`` = 0.5
            * ``cey`` = 4.5
            * ``d`` = 1.

        It can be readily verified that this combination satisfies the
        conditions (1)-(3).
        """
        slab = Slab.create_rectangle_by_dimensions(
                10., 10., position='lower-left'
                )
        r = 0.5
        cex = 0.5
        cey = 4.5
        slab.add_column(shape='circle', r=r, center=(slab.bx-r-cex, cey+r))

        d = 1.
        column = slab.columns[0]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = 2*r + 2*cex + (r+d)*pi
        self.assertAlmostEqual(
                u1.boundary.difference(slab.boundary).length, expected_length,
                delta=0.001*expected_length
                )

        # Add a tangent column
        slab.add_column(shape='circle', r=r, center=(r, slab.by/2))
        column = slab.columns[1]
        u1 = column.construct_minimum_perimeter(distance=d)
        expected_length = 2*r + (r+d)*pi
        self.assertAlmostEqual(
            u1.boundary.difference(slab.boundary).length, expected_length,
            delta=0.001*expected_length
            )
        position = 'edgex'
        self.assertEqual(u1.position, position)

    def test_drop_panel_property(self):
        column = Column.create_rectangle_by_dimensions(1., 1.)
        self.assertIsNone(column.drop_panel)

        column.set_drop_panel(lx=0.5, height=0.3)
        self.assertAlmostEqual(column.drop_panel.area, 4.)
        self.assertAlmostEqual(column.drop_panel.height, 0.3)

    def test_construct_minimum_perimeter_explicit_shape(self):
        slab = Slab.create_rectangle_by_dimensions(
                10., 10., position='lower-left'
                )
        r = 0.5
        slab.add_column(shape='circle', r=r, center=(5., 5.))
        rmodified = 1.
        shape = PlanarShape.create_circle(r=rmodified, center=(5., 5.))
        column = slab.columns[0]
        deff = 1.
        u1 = column.construct_minimum_perimeter(distance=deff, shape=shape)
        expected_length = pi * (deff + rmodified)**2
        self.assertAlmostEqual(u1.length, expected_length,
                               delta=0.001*expected_length)

        shape = PlanarShape.create_circle(r=rmodified, center=(15., 15.))
        with self.assertRaises(ValueError):
            u1 = column.construct_minimum_perimeter(distance=deff,
                                                    shape=shape)

    def test_deff(self):
        slab = Slab.create_rectangle_by_dimensions(
            10., 10., position='lower-left'
            )
        phix, sxy, dx = 12., 100., .280
        slab.add_tension_rebar_raw(phi=phix, s=sxy, d=dx)

        r = 0.5
        slab.add_column(shape='circle', r=r, center=(5., 5.))
        self.assertAlmostEqual(slab.columns[0].deff, dx)

        phiy, syx, dy = 14., 100., .300
        slab.add_tension_rebar_raw(phi=phiy, s=syx, d=dy, axes='y', index=0)
        self.assertAlmostEqual(slab.columns[0].deff, (dx+dy)/2.)

        phiy2, syx2, dy2 = 14., 100., .280
        slab.add_tension_rebar_raw(phi=phiy2, s=syx2, d=dy2, axes='y')
        dy = (dy + dy2)/2.
        self.assertAlmostEqual(slab.columns[0].deff, (dx+dy)/2.)

    @mock.patch(('dx_punch.EC2.DropPanel'
                 '.resolve_control_perimeter_parameters'),
                mock.Mock(return_value=(None, None)))
    @mock.patch('dx_punch.EC2.BasicControlPerimeter',
                mock.Mock(BasicControlPerimeter))
    @mock.patch('dx_punch.EC2.Column.u0',
                mock.Mock(ControlPerimeter))
    @mock.patch('dx_punch.EC2.Column.ui',
                mock.PropertyMock(return_value=BasicControlPerimeter))
    def test_control_perimeters_raise_error(self):
        column = Column.create_rectangle_by_dimensions(1., 1.)
        column.set_drop_panel(lx=0.5, height=0.3)
        with self.assertRaises(ImplementationError):
            column.control_perimeters

    def test_k639(self):
        c = Column
        self.assertAlmostEqual(c.k639(0.2), 0.45)
        self.assertAlmostEqual(c.k639(0.8), 0.54)
        self.assertAlmostEqual(c.k639(1.), 0.6)
        self.assertAlmostEqual(c.k639(1.5), 0.65)
        self.assertAlmostEqual(c.k639(2.0), 0.70)
        self.assertAlmostEqual(c.k639(3.0), 0.80)

    def test_kxy(self):
        c = Column.create_rectangle_by_dimensions(bx=1., by=2.)
        self.assertAlmostEqual(c.kx, 0.70)
        self.assertAlmostEqual(c.ky, 0.45)

    def test_offsets(self):
        slab = Slab.create_rectangle_by_dimensions(
           bx=10., by=10., position='lower-left'
           )
        slab.add_column(bx=1., by=1., origin=(8.5, 5.))
        column = slab.columns[0]
        self.assertTupleAlmostEqual(column.offset, (8., 4.5, 1., 4.5))
        self.assertAlmostEqual(column.oxmin, 1.)
        self.assertAlmostEqual(column.oymin, 4.5)
        self.assertAlmostEqual(column.oxmax, 8.)
        self.assertAlmostEqual(column.oymax, 4.5)

    @mock.patch('dx_punch.EC2.Column.control_perimeters',
                mock.PropertyMock(return_value=[]))
    @mock.patch('dx_punch.EC2.BasicControlPerimeter',
                mock.Mock(BasicControlPerimeter))
    @mock.patch('dx_punch.EC2.Column.construct_minimum_perimeter',
                mock.Mock(return_value=BasicControlPerimeter))
    @mock.patch('dx_punch.EC2.Column.deff',
                mock.PropertyMock(return_value=1.))
    def test_bMomenti(self):
        s = Slab.new(bx=1., by=1.)
        c = Column.create_rectangle_by_dimensions(slab=s, bx=1., by=2.)
        lc = c.load_cases[0]
        self.assertEqual(c.bMomenti[0], 0)
        c.set_lc(lc.LC, Mex=1.)
        self.assertEqual(c.bMomenti[0], 1)
        c.set_lc(lc.LC, Mex=0.)
        self.assertEqual(c.bMomenti[0], 0)
        c.set_lc(lc.LC, Mey=1.)
        self.assertEqual(c.bMomenti[0], 2)
        c.set_lc(lc.LC, Mey=0.)
        self.assertEqual(c.bMomenti[0], 0)
        c.set_lc(lc.LC, Mex=1., Mey=1.)
        self.assertEqual(c.bMomenti[0], 3)

    @mock.patch('dx_punch.EC2.Column.deff',
                new_callable=mock.PropertyMock)
    def test_truncate_point(self, deff):
        slab = Slab.create_rectangle_by_dimensions(
                bx=10., by=10., position='lower-left'
                )
        # Rectangle columns
        slab.add_column(bx=1., by=1, origin=(2., 2.))
        slab.add_column(bx=1., by=1, origin=(2., 8.))
        slab.add_column(bx=1., by=1, origin=(8., 8.))
        slab.add_column(bx=1., by=1, origin=(8., 2.))

        self.assertIsInstance(slab.columns[0].truncate_point, np.ndarray)

        # -> large deff
        deff.return_value = 1.

        self.assertTrue(np.allclose(
            slab.columns[0].truncate_point, np.array([2., 2.])
            ))
        self.assertTrue(np.allclose(
            slab.columns[1].truncate_point, np.array([2., 8.])
            ))
        self.assertTrue(np.allclose(
            slab.columns[2].truncate_point, np.array([8., 8.])
            ))
        self.assertTrue(np.allclose(
            slab.columns[3].truncate_point, np.array([8., 2.])
            ))

        # -> small deff (1.5d < bx/2 and 1.5d < by/2)
        deff.return_value = 0.3
        for c in slab.columns:
            c._truncate_point = c._evaluate_truncate_point()

        self.assertTrue(np.allclose(
            slab.columns[0].truncate_point, np.array([2.05, 2.05])
            ), slab.columns[0].truncate_point)
        self.assertTrue(np.allclose(
            slab.columns[1].truncate_point, np.array([2.05, 7.95])
            ))
        self.assertTrue(np.allclose(
            slab.columns[2].truncate_point, np.array([7.95, 7.95])
            ))
        self.assertTrue(np.allclose(
            slab.columns[3].truncate_point, np.array([7.95, 2.05])
            ))

        # Circular columns
        slab.agents['columns'] = []
        slab.add_column(shape='circle', r=0.5, center=(2., 2.))
        slab.add_column(shape='circle', r=0.5, center=(2., 8.))
        slab.add_column(shape='circle', r=0.5, center=(8., 8.))
        slab.add_column(shape='circle', r=0.5, center=(8., 2.))

        # -> small deff (1.5d < bx/2 and 1.5d < by/2)

        self.assertTrue(np.allclose(
            slab.columns[0].truncate_point, np.array([2.05, 2.05]))
            )
        self.assertTrue(np.allclose(
            slab.columns[1].truncate_point, np.array([2.05, 7.95]))
            )
        self.assertTrue(np.allclose(
            slab.columns[2].truncate_point, np.array([7.95, 7.95])
            ))
        self.assertTrue(np.allclose(
            slab.columns[3].truncate_point, np.array([7.95, 2.05])
            ))

        # -> large deff
        deff.return_value = 1.0
        for c in slab.columns:
            c._truncate_point = c._evaluate_truncate_point()

        self.assertTrue(np.allclose(
            slab.columns[0].truncate_point, [2., 2.])
            , slab.columns[0].truncate_point)
        self.assertTrue(np.allclose(
            slab.columns[1].truncate_point, np.array([2., 8.]))
            )
        self.assertTrue(np.allclose(
            slab.columns[2].truncate_point, np.array([8., 8.]))
            )
        self.assertTrue(np.allclose(
            slab.columns[3].truncate_point, np.array([8., 2.]))
            )

        # Angle-shaped

        # -> large deff
        coords = [(0., 0.), (1., 0), (1., 0.3), (0.3, 0.3),
                  (0.3, 1.5), (0., 1.5)]
        slab.agents['columns'] = []
        slab.add_column(shape='generic', vertices=coords)

        T = slab.columns[0].truncate_point
        self.assertAlmostEqual(T[0], 0.309, delta=0.001*T[0])
        self.assertAlmostEqual(T[1], 0.559, delta=0.001*T[1])

        # -> small deff
        deff.return_value = 0.3
        c = slab.columns[0]
        c._truncate_point = c._evaluate_truncate_point()
        T = slab.columns[0].truncate_point
        self.assertAlmostEqual(T[0], 0.55, delta=0.001*T[0])
        self.assertAlmostEqual(T[1], 1.05, delta=0.001*T[1])

    def test_resolve_soil_pressure(self):
        slab = Slab.create_rectangle_by_dimensions(
            10., 10., position='lower-left', slab_type='raft'
            )
        slab.add_column(shape='circle', r=1., center=(5., 5.))
        c = slab.columns[0]
        self.assertAlmostEqual(c._resolve_soil_pressure(), 0.)
        slab.foundation = True
        self.assertAlmostEqual(c._resolve_soil_pressure(), 0.)
        slab.add_soil_pressure(10.)
        self.assertAlmostEqual(c._resolve_soil_pressure(), 10.)

    @mock.patch('dx_punch.EC2.Column._resolve_soil_pressure',
                mock.Mock(return_value=None))
    def test_soil_pressure(self):
        c = self.slab.columns[0]
        self.assertIsNone(c.soil_pressure)
        c._resolve_soil_pressure.assert_called_once()

    def test_k647(self):
        slab = Slab.create_circle(r=10., thickness=0.3)
        slab.add_column(shape='circle', r=0.5)
        c = slab.columns[0]
        c.deff = 0.28
        expected = 1 + (0.2 / c.deff)**0.5
        self.assertAlmostEqual(c.k647, expected)
        c.deff = 0.29
        expected = 1 + (0.2 / c.deff)**0.5
        self.assertAlmostEqual(c.k647, expected)

    def test_vmin(self):
        slab = Slab.create_circle(r=10., thickness=0.3,
                                               material=RC[16])
        slab.add_column(shape='circle', r=0.5)
        c = slab.columns[0]
        c.deff = 0.28
        fck = inverse_transform_value(slab.material.fck)
        expected = 0.035 * c.k647**1.5 * fck**0.5
        self.assertAlmostEqual(c.vmin, transform_value(expected))
        c.deff = 0.29
        expected = 0.035 * c.k647**1.5 * fck**0.5
        self.assertAlmostEqual(c.vmin, transform_value(expected))

    def test_effective_region(self):
        slab = Slab.create_rectangle_by_dimensions(
            bx=10., by=10., origin=(5., 5.), thickness=0.3
            )
        # Region not intersecting slab
        slab.add_column(shape='circle', r=0.5, center=(5., 5.))
        c = slab.columns[0]
        c.deff = 0.25
        region = c.tensile.effective_region
        self.assertIsInstance(region, PlanarShape)
        expected_area = (6*c.deff + c.bx) * (6*c.deff + c.by)
        self.assertAlmostEqual(region.area, expected_area)
        self.assertAlmostEqual(region.centroid.x, c.centroid.x)
        self.assertAlmostEqual(region.centroid.y, c.centroid.y)
        # Region intersecting slab
        slab.add_column(bx=1., by=1., origin=(1.5, 5.))
        c = slab.columns[1]
        c.deff = 0.5
        region = c.tensile.effective_region
        expected_area = (3*c.deff + c.bx + c.oxmin) * (6*c.deff + c.by)
        self.assertAlmostEqual(region.area, expected_area)
        self.assertNotAlmostEqual(region.centroid.x, c.centroid.x)
        self.assertAlmostEqual(region.centroid.y, c.centroid.y)

    def test_Ast(self):
        slab = Slab.create_rectangle_by_dimensions(
            10., 10., position='lower-left'
            )
        # Add reinforcement along x
        phi1, s1, d1 = 12., 100., .280
        slab.add_uniform_rebar(phi=phi1, s=s1, d=d1)
        rebar1 = slab.rebar[0]

        phi2, s2, d2 = 14., 100., .300
        slab.add_partial_rebar(phi=phi2, s=s2, d=d2, bx=1., by=10.,
                               origin=(0.5, 5.))
        rebar2 = slab.rebar[1]

        slab.add_column(bx=0.5, by=0.5, origin=(0.25, 5.))
        c = slab.columns[0]

        domain1 = PlanarShape(c.tensile.effective_region.intersection(rebar1.geometry))
        domain2 = PlanarShape(c.tensile.effective_region.intersection(rebar2.geometry))

        Asx = rebar1.value[0].Asbr * domain1.by
        Asx += rebar2.value[0].Asbr * domain2.by

        self.assertAlmostEqual(c.Ast[0], Asx)
        self.assertAlmostEqual(c.Ast[1], 0.)
        # Add reinforcement along y
        slab.add_rebar_raw(phi=phi1, s=s1, d=d1, axes='y', index=0)
        slab.add_rebar_raw(phi=phi2, s=s2, d=d2, axes='y', index=1)
        Asy = rebar1.value[1].Asbr * domain1.bx
        Asy += rebar2.value[1].Asbr * domain2.bx
        c.tensile._Ast = None
        self.assertAlmostEqual(c.Asx, Asx)
        self.assertAlmostEqual(c.Asy, Asy)

    def test_rho(self):
        slab = Slab.create_rectangle_by_dimensions(
            10., 10., position='lower-left', thickness=0.3
            )
        # Add uniform reinforcement throughout the slab
        # ⌀12/150 @ 26mm depth
        phi, s, d = 0.012, 0.15, .26
        slab.add_uniform_rebar(phi, s, d, axes='xy')
        uniform_rebar = slab.rebar[0]
        Asbrx = uniform_rebar.value[0].Asbr
        Asbry = uniform_rebar.value[1].Asbr
        rhox, rhoy = (Asbr / d for Asbr in (Asbrx, Asbry))
        rhol = min(sqrt(rhox*rhoy), 0.02)

        slab.add_column(bx=1., by=1., origin=(0.5, 5.))
        column = slab.columns[0]
        self.assertAlmostEqual(column.rhox, rhox)
        self.assertAlmostEqual(column.rhoy, rhoy)
        self.assertAlmostEqual(column.rhol, rhol)

        t_region = column.tensile.effective_region
        # Add additional reinforcement near the edge
        # of the slab:
        # 6⌀12/200 @ left-edge over a breadth of 1 m

        phi1, s1, d1, nbars = 0.012, 0.2, .28, 6
        slab.add_partial_rebar(phi1, s1, d1, nbars,
                               bx=1., by=10., position='lower-left')
        t_region = column.tensile.effective_region
        add_rebar = slab.rebar[1]
        Asbrx1 = add_rebar.value[0].Asbr
        domain1 = PlanarShape(add_rebar.geometry.intersection(t_region))

        # clear cache
        column.tensile._Ast = None
        column._Ast = None
        column.update_effective_depth()
        column.tensile._rhox = None
        column.tensile._rhoy = None
        column.tensile._rhol = None

        Asx = Asbrx*t_region.by + Asbrx1*domain1.by
        self.assertAlmostEqual(column.Asx, Asx)
        rhox = Asx / t_region.by / column.deff
        rhoy = Asbry / column.deff
        rhol = min(sqrt(rhox*rhoy), 0.02)
        self.assertAlmostEqual(column.rhox, rhox)
        self.assertAlmostEqual(column.rhoy, rhoy)
        self.assertAlmostEqual(column.rhol, rhol)

    def test_vrdc(self):
        # Configure the structure
        slab = Slab.new(bx=10., by=10., position='lower-left', thickness=.3,
                                     material=RC[16])
        slab.add_uniform_rebar(phi=0.012, d=0.28, s=0.1, axes='xy')
        slab.add_column(shape='circle', r=0.5, center=(5., 5.))
        column = slab.columns[0]
        # Evaluate the expected value
        CRdc = slab.material.CRdc()
        fck = inverse_transform_value(slab.material.fck)
        k = column.k647
        rhol = column.rhol
        vmin = inverse_transform_value(column.vmin)
        vrdc = max(CRdc * k * (100*rhol*fck)**(1/3), vmin)
        self.assertAlmostEqual(column.vrdc, transform_value(vrdc))

    @mock.patch('dx_punch.EC2.Column.deff',
                new_callable=mock.PropertyMock)
    def test_fywdef(self, deff):
        slab = Slab()
        column = Column(slab=slab)
        deff.return_value = 0.30
        expected = (250 + 0.25*300)*1e+06
        self.assertAlmostEqual(column.fywdef, expected)
        deff.return_value = 1.2
        expected = slab.fywd
        column._fywdef = None
        self.assertAlmostEqual(column.fywdef, expected)

    def test_set_shear_reinforcement(self):
        column = Column()
        self.assertIsNone(column.shear.csx)
        column.set_shear_reinforcement(Aswr=1.)
        self.assertAlmostEqual(column.shear.Aswr, 1.)


class TestDropPanel(DXTestCase):

    def test_create_as_rectangle_offset(self):
        column = Column.create_rectangle_by_dimensions(1., 1.)
        lx = 0.5
        ly = 1.
        hH = 0.3
        drop_panel = DropPanel.create_as_column_offset(column, lx, hH,
                                                             ly)

        expected_l1 = max(2., 3.)
        expected_l2 = min(2., 3.)
        self.assertAlmostEqual(drop_panel.l1, expected_l1)
        self.assertAlmostEqual(drop_panel.l2, expected_l2)

    def test_create_as_circle_offset(self):
        return
        column = Column.create_circle(r=1., center=(0., 0.))
        lx = 0.5
        hH = 0.3
        drop_panel = DropPanel.create_as_column_offset(column, lx, hH)

        expected_l1 = max(3., 3.)
        expected_l2 = min(3., 3.)
        self.assertAlmostEqual(drop_panel.l1, expected_l1)
        self.assertAlmostEqual(drop_panel.l2, expected_l2)

    @mock.patch('dx_punch.EC2.Column.deff',
                new_callable=mock.PropertyMock)
    def test_resolve_control_perimeter_parameters_small_head(self, deff):
        """Test the case in which lH < 2*hH"""
        slab = Slab.create_circle(r=10.)
        column = Column.create_circle(slab=slab, r=1.)
        deff.return_value = 1.

        lx = 0.5
        hH = 0.3
        drop_panel = DropPanel.create_as_column_offset(column, lx, hH)
        internal, external = drop_panel.resolve_control_perimeter_parameters()
        # Internal should be none
        self.assertIsNone(internal)
        # External should have the column as the source-shape
        # and min(lx, ly) + 2*deff as offset-distance
        self.assertEqual(external[0], column)
        self.assertAlmostEqual(external[1], 2.5)

    @mock.patch('dx_punch.EC2.Column.deff',
                new_callable=mock.PropertyMock)
    def test_resolve_control_perimeter_parameters_medium_head(self, deff):
        """Test the case in which 2*(hH + deff) >= lH >= 2*hH"""
        slab = Slab.create_circle(r=10.)
        column = Column.create_circle(slab=slab, r=1.)
        deff.return_value = 1.

        lx = 1.5
        hH = 0.3
        drop_panel = DropPanel.create_as_column_offset(column, lx, hH)
        internal, external = drop_panel.resolve_control_perimeter_parameters()
        # Internal should have the column as the source-shape
        # and 2*(deff + hH) as offset-distance
        self.assertEqual(internal[0], column)
        self.assertAlmostEqual(internal[1], 2*(column.deff + hH))
        # External should have the column as the source-shape
        # and min(lx, ly) + 2*deff as offset-distance
        self.assertEqual(external[0], column)
        self.assertAlmostEqual(external[1], 3.5)

    @mock.patch('dx_punch.EC2.Column.deff',
                new_callable=mock.PropertyMock)
    def test_resolve_control_perimeter_parameters_large_head(self, deff):
        """Test the case in which lH > 2*(hH + deff)"""
        slab = Slab.create_circle(r=10.)
        column = Column.create_circle(slab=slab, r=1.)
        deff.return_value = 1.

        lx = 3.0
        hH = 0.3
        drop_panel = DropPanel.create_as_column_offset(column, lx, hH)
        internal, external = drop_panel.resolve_control_perimeter_parameters()
        # Internal should have the column as the source-shape
        # and 2*(hH + deff) as offset-distance
        self.assertIsNotNone(internal)
        self.assertEqual(internal[0], column)
        self.assertAlmostEqual(internal[1], 2.6)
        # External should have the column as the source-shape
        # and min(lx, ly) + 2*deff as offset-distance
        self.assertEqual(external[0], column)
        self.assertAlmostEqual(external[1], 5.)
