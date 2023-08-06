import unittest.mock as mock
import numpy as np

from math import pi, sqrt
from shapely.geometry import LineString

from test import DXTestCase

from dx_punch.EC2 import Slab, BasicControlPerimeter
from dx_eurocode.EC2.materials import RC
from dx_utilities.integrals import line_moment
from dx_utilities.units import inverse_transform_value


@mock.patch('dx_punch.EC2.BasicControlPerimeter',
            mock.Mock(BasicControlPerimeter))
@mock.patch('dx_punch.EC2.BasicControlPerimeter.beta',
            mock.PropertyMock(return_value=None))
@mock.patch('dx_punch.EC2.Column.ui',
            mock.PropertyMock(return_value=BasicControlPerimeter()))
@mock.patch('dx_punch.EC2.Column.deff',
            new_callable=mock.PropertyMock)
class TestColumnPerimeter(DXTestCase):
    """Set of tests to assert the accuracy
    in the calculation of the control perimeter
    at the sides of the column.
    """

    def setUp(self):
        self.slab = Slab.new(bx=10., by=10., position='lower-left')
        self.bx = 0.2
        self.by = 0.2
        self.slab.add_column(shape='rectangle', bx=self.bx, by=self.by,
                             origin=(0.2, 0.2))
        self.slab.add_column(shape='rectangle', bx=self.bx, by=self.by,
                             origin=(0.2, 5.))
        self.slab.add_column(shape='rectangle', bx=self.bx, by=self.by,
                             origin=(5, 5.))
        self.corner = self.slab.columns[0]
        self.edge = self.slab.columns[1]
        self.internal = self.slab.columns[2]

    def test_corner_column(self, deff):
        column = self.corner
        deff.return_value = column.bx
        column.ui.position = 'corner'
        expected_length = column.bx + column.by
        self.assertAlmostEqual(column.u0.length, expected_length,
                               delta=1e-03*expected_length)

        deff.return_value = column.bx / 2
        expected_length = 3*column.deff
        column.u0._length = None
        self.assertAlmostEqual(column.u0.length, expected_length,
                               delta=1e-03*expected_length)

    def test_internal_column(self, deff):
        column = self.internal
        deff.return_value = 0.3
        column.ui.position = 'internal'
        expected_length = column.length
        self.assertAlmostEqual(column.u0.length, expected_length,
                               delta=1e-03*expected_length)

        column.u0._length = None
        deff.return_value = column.bx / 2
        expected_length = column.length

    def test_edge_column(self, deff):
        column = self.edge
        deff.return_value = column.bx
        column.ui.position = 'edgex'
        expected_length = 2*column.bx + column.by
        self.assertAlmostEqual(column.u0.length, expected_length,
                               delta=1e-03*expected_length)

        deff.return_value = column.bx / 2
        expected_length = 3*column.deff + column.by
        column.u0._length = None
        self.assertAlmostEqual(column.u0.length, expected_length,
                               delta=1e-03*expected_length)


@mock.patch('dx_punch.EC2.ControlPerimeter.dcr',
            mock.PropertyMock(return_value=1.))
class TestBasicControlPerimeter(DXTestCase):

    def setUp(self):
        self.slab = Slab.create_rectangle_by_dimensions(
                bx=10., by=10., position='lower-left'
                )
        self.slab.add_tension_rebar_raw(phi=.016, s=.100, d=0.5)
        self.slab.add_column(bx=1.5, by=1., origin=(8.5, 5.))
        self.slab.add_column(bx=1., by=1.5, origin=(5, 8.5))
        self.slab.add_column(bx=1., by=1., origin=(8.5, 8.5))
        self.slab.add_column(bx=0.75, by=0.5, origin=(6., 6.))
        self.slab.add_column(shape='circle', r=0.5, center=(4., 4.))
        self.columns = self.slab.columns

    def test_eccentricities(self):
        c = self.slab.columns[0]
        self.assertAlmostEqual(c.ui.ex, 0.)
        self.assertAlmostEqual(c.ui.ey, 0.)

        lc = c.load_cases[0]
        c.set_lc(lc.LC, Mey=-10.)
        self.assertAlmostEqual(c.ui.ex, 10.)
        self.assertAlmostEqual(c.ui.ey, 0.)

        c.Mey = 0.
        c.Mex = -10.
        c.set_lc(lc.LC, Mex=-10., Mey=0.)
        self.assertAlmostEqual(c.ui.ex, 0.)
        self.assertAlmostEqual(c.ui.ey, -10.)

        c.set_lc(lc.LC, Mex=+1., Mey=+1.)
        self.assertAlmostEqual(c.ui.ex, -1.)
        self.assertAlmostEqual(c.ui.ey, 1.)

        c.set_lc(lc.LC, N=10.)
        self.assertAlmostEqual(c.ui.ex, -.1)
        self.assertAlmostEqual(c.ui.ey, .1)

    def test_path_edge_x(self):
        column = self.columns[0]
        control_perimeter = column.ui
        self.assertTrue(control_perimeter.position=='edgex')
        path = control_perimeter.path
        self.assertIsInstance(path, LineString)
        expected_length = (pi*(2*column.deff) + 2*column.bx
                           + 2*column.oxmin + column.by)
        self.assertAlmostEqual(path.length, expected_length,
                               delta=0.001*expected_length)

    def test_path_edge_y(self):
        column = self.columns[1]
        control_perimeter = column.ui
        self.assertTrue(control_perimeter.position=='edgey')
        path = control_perimeter.path
        self.assertIsInstance(path, LineString)
        expected_length = (pi*(2*column.deff) + 2*column.by
                           + 2*column.oymin + column.bx)
        self.assertAlmostEqual(path.length, expected_length,
                               delta=0.001*expected_length)

    def test_path_corner(self):
        column = self.columns[2]
        control_perimeter = column.ui
        self.assertTrue(control_perimeter.position=='corner')
        path = control_perimeter.path
        self.assertIsInstance(path, LineString)
        expected_length = (pi*(2*column.deff)/2 + column.bx
                           + column.by + column.oxmin
                           + column.oymin)
        self.assertAlmostEqual(path.length, expected_length,
                               delta=0.001*expected_length)

    def test_path_internal(self):
        column = self.columns[3]
        control_perimeter = column.ui
        self.assertTrue(control_perimeter.position=='internal')
        path = control_perimeter.path
        self.assertIsInstance(path, LineString)
        expected_length = (2* pi*(2*column.deff) + 2*column.bx
                           + 2*column.by)
        self.assertAlmostEqual(path.length, expected_length,
                               delta=0.001*expected_length)

    def test_path_local_internal(self):
        """Test that the coordinates of the local path
        are expressed with reference to the parent-column
        centroid. To this end, the vector representing
        the local-path centroid in the local coordinate
        system is verified.
        """
        column = self.columns[3]
        perimeter = column.ui
        # Expected vector representation
        dexpected = (
                perimeter.path.centroid.x - column.centroid.x,
                perimeter.path.centroid.y - column.centroid.y,
                )
        # Calculated vector representation
        dactual = tuple(perimeter.path_local.centroid.coords)[0]
        self.assertTupleAlmostEqual(dexpected, dactual)

    def test_path_local_edge_column(self):
        """Test that the coordinates of the local path
        are expressed with reference to the perimeter's
        centroid.
        """
        column = self.columns[0]
        perimeter = column.ui
        perimeter.recache_local_path(origin=perimeter.path.centroid)
        # Expected vector representation
        dexpected = (0., 0)
        # Calculated vector representation
        dactual = tuple(perimeter.path_local.centroid.coords)[0]
        self.assertTupleAlmostEqual(dexpected, dactual)

    def test_Wx_internal(self):
        column = self.columns[3]
        control_perimeter = column.ui

        bx = column.bx
        by = column.by
        d = column.deff
        expected = by**2/2. + 2*pi*d*by + 16*d**2 + bx*by + 4*bx*d
        self.assertAlmostEqual(control_perimeter.Wx, expected,
                               delta=0.001*expected)

    def test_Wy_internal(self):
        column = self.columns[3]
        control_perimeter = column.ui

        bx = column.bx
        by = column.by
        d = column.deff
        expected = bx**2/2. + 2*pi*d*bx + 16*d**2 + bx*by + 4*by*d
        self.assertAlmostEqual(control_perimeter.Wy, expected,
                               delta=0.001*expected)

    def test_Wxy_internal_circ(self):
        column = self.columns[4]
        control_perimeter = column.ui

        bx = column.bx
        d = column.deff
        expected = (bx + 4*d)**2
        self.assertAlmostEqual(control_perimeter.Wx, expected,
                               delta=0.001*expected)
        self.assertAlmostEqual(control_perimeter.Wy, expected,
                               delta=0.001*expected)

    def test_Wy_edgex(self):
        """Verify the accuracy of the evaluation of the
        modulus of the control perimeter of an edge column.

        The modulus is calculated about the local-axis
        parallel to the edge, in a coordinate system whose
        origin is the column's centroid.
        """
        column = self.columns[0]
        perimeter = column.ui

        bx = column.bx
        by = column.by
        ox = column.oxmin
        d = column.deff

        expected = (ox+bx/2)**2 + bx**2/4 + d*bx*pi + 8*d**2 + by*(bx/2 + 2*d)
        self.assertAlmostEqual(perimeter.Wy, expected, delta=0.001*expected)

    def test_Wy_perimeter_centroid_edgex(self):
        """Verify the accuracy of the evaluation of the
        modulus of the control perimeter of an edge column.

        The modulus is calculated about the local-axis
        parallel to the edge, in a coordinate system whose
        origin is the perimeter's centroid.
        """
        column = self.columns[0]
        perimeter = column.ui
        perimeter.recache_local_path(origin=perimeter.path.centroid)

        # For the analytical evaluation we express all
        # coordinates with reference to a system with
        # origin a point (column.centroid.x, self.slab.by)
        bx = column.bx
        by = column.by
        ox = column.oxmin
        d = column.deff

        a = bx + ox
        b = by

        cox = self.slab.bx - perimeter.path.centroid.x
        expected = (2*(cox**2 + 1/2*a**2 - cox*a) + 2*2*d*(2*d + a*pi/2 - cox*pi/2)
              + 2*(a*b/2 + d*b - cox*b/2))
        self.assertAlmostEqual(perimeter.Wy, expected, delta=0.001*expected)

    def test_Wx_edgex(self):
        """Verify the accuracy of the evaluation of the
        modulus of the control perimeter of an edge column.

        The modulus is calculated about the local-axis
        perpendicular to the edge, in a coordinate system whose
        origin is the perimeter's centroid.
        """
        column = self.columns[0]
        perimeter = column.ui

        # For the analytical evaluation we express all
        # coordinates with reference to a system with
        # origin a point (column.centroid.x, self.slab.by)
        bx = column.bx
        by = column.by
        ox = column.oxmin
        d = column.deff

        a = bx + ox
        b = by

        expected = 2*(b*a/2 + 2*d*a) + 2*(b*d*pi/2 + 4*d**2) + 2*b**2/8
        self.assertAlmostEqual(perimeter.Wx, expected, delta=0.001*expected)

    def test_Wxy_perimeter_centroid_corner(self):
        """Verify the accuracy of the evaluation of the
        modulus of the control perimeter of a corner column.

        The modulus is calculated about the local-axis
        x and y, in a coordinate system whose origin is
        the perimeter's centroid.
        """
        column = self.columns[2]
        perimeter = column.ui
        perimeter.recache_local_path(origin=perimeter.path.centroid)

        # For the analytical evaluation we express all
        # coordinates with reference to a system with
        # origin a point (self.slab.x, self.slab.by)
        # and axes pointing inwards.
        bx = column.bx
        by = column.by
        ox = column.oxmin
        oy = column.oymin
        d = column.deff

        a = by + oy
        b = bx + ox
        cox = self.slab.bx - perimeter.path.centroid.x
        coy = self.slab.by - perimeter.path.centroid.y

        expectedWx = (b*a + 2*b*d - b*coy + 2*d*a*pi/2 - 2*d*coy*pi/2 + 4*d**2
                      + (coy - a)**2 + a*(coy-a) + a**2/2)
        self.assertAlmostEqual(perimeter.Wx, expectedWx, delta=0.001*expectedWx)

        expectedWy = (b*a + 2*a*d - a*cox + 2*d*b*pi/2 - 2*d*cox*pi/2 + 4*d**2
                      + (cox - b)**2 + b*(cox-b) + b**2/2)
        self.assertAlmostEqual(perimeter.Wy, expectedWy, delta=0.001*expectedWy)

    def test_truncated_perimeter(self):
        """Verify the accuracy in evaluating the truncated
        control perimeter (u1star) for edge columns according
        to § 6.4.3(4).
        """
        slab = Slab.create_rectangle_by_dimensions(
           bx=10., by=10., position='lower-left'
           )
        # case ``1.5d = 0.5c1``
        slab.add_tension_rebar_raw(phi=.016, s=.100, d=0.5)
        slab.add_column(bx=1.5, by=1., origin=(0.75, 5.))

        c = slab.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated

        expected_length = c.by + c.bx + pi*2*c.deff
        self.assertAlmostEqual(u1star.length, expected_length,
                               delta=0.001*expected_length)

        # case ``1.5d < 0.5c1``
        slab.add_column(bx=2.0, by=1., origin=(9.00, 5.))
        c = slab.columns[1]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated

        expected_length = c.by + 3*c.deff + pi*2*c.deff
        self.assertAlmostEqual(u1star.length, expected_length,
                               delta=0.001*expected_length)

    def test_vsi_internal(self):
        column = self.columns[0]
        perimeter = column.ui
        d = column.deff
        u1 = perimeter.path.length
        kx = column.kx
        ky = column.ky
        lc = column.load_cases[0]

        # no moment
        self.assertAlmostEqual(perimeter.evaluate_vsi()[0],
                               0.)

        # bending along x-axis
        column.set_lc(lc.LC, Mex=10.)
        vsx = kx*lc.Mex/column.ui.Wx/d
        self.assertAlmostEqual(column.ui.evaluate_vsi()[0],
                               vsx)

        # bending along y-axis
        column.set_lc(lc.LC, Mex=0., Mey=10.)
        vsy = ky*lc.Mey/perimeter.Wy/d
        self.assertAlmostEqual(column.ui.evaluate_vsi()[0],
                               vsy)

        # bending along both axes
        column.set_lc(lc.LC, Mex=10.)
        vs = sqrt(vsx**2 + vsy**2)
        self.assertAlmostEqual(column.ui.evaluate_vsi()[0],
                               vs)

        #  -> approximate
        vsappr = (1.8/u1/d * sqrt(
            (lc.Mex/perimeter.by)**2 + (lc.Mey/perimeter.bx)**2
            ))
        self.assertAlmostEqual(
                column.ui.evaluate_vsi(approximate=True)[0],
                vsappr
                )
        self.assertGreater(vsappr, vs)

    def test_evaluate_betai_edge_raises(self):
        c = self.columns[3]
        control_perimeter = c.ui
        self.assertEqual(control_perimeter.position, 'internal')
        with self.assertRaises(ValueError):
            control_perimeter.evaluate_betai_edge()

    def test_evaluate_beta_edge_no_bending(self):
        c = self.columns[0]
        control_perimeter = c.ui
        beta = control_perimeter.beta
        self.assertAlmostEqual(beta, 1.)

    def test_evaluate_beta_edgex_Myinward_Mx0(self):
        """Verify the evaluation of beta for
        a column close to an edge along its x-axis.

        We assume that there exists a bending moment
        about the axis parallel to the edge (My in this case),
        causing eccentricity toward the interior of the slab.
        We further assume that ``Mx`` is zero.

        Under these conditions we expect the factor beta
        to be equal to the ratio u1/u1star
        """
        c = self.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        c.set_lc(lc.LC, Mey=10.)
        beta = perimeter.beta
        expected = u1.length / u1star.length
        self.assertGreater(expected, 1.)
        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_beta_edgex_Myinward_Mx(self):
        """Verify the evaluation of beta for
        a column close to an edge along its x-axis.

        We assume that there exists a bending moment
        about the axis parallel to the edge (My in this case),
        causing eccentricity toward the interior of the slab.
        We further assume that ``Mx`` is not zero.

        Under these conditions we expect the factor beta
        to be evaluated according to Eq. (6.44).
        """
        c = self.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Set bending moments
        c.set_lc(lc.LC, Mex=10., Mey=10.)
        # Calculate beta manually
        beta0 = u1.length / u1star.length
        c1 = c.bx
        c2 = c.by
        k644 = c.k639(c1/c2/2)
        beta1 = k644 * (c.ui.length/c.ui.Wx) * (abs(lc.Mex)/lc.N)
        expected = beta0 + beta1
        # Calucate beta numerically
        beta = perimeter.beta

        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_beta_edgex_Myoutward_Mx(self):
        """Verify the evaluation of beta for
        a column close to an edge along its x-axis.

        We assume that there exists a bending moment
        about the axis parallel to the edge (My in this case),
        causing eccentricity toward the exterior of the slab.
        We further assume that ``Mx`` is not zero.

        Under these conditions we expect the factor beta
        to be evaluated according to Eq. (6.39), calculating
        ``W1`` with respect to the perimeters centroid.
        """
        c = self.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Evaluate modified path-moduli
        modified_path = perimeter.evaluate_local_path(u1.centroid)
        Wx = line_moment(modified_path, (1., 0.))
        Wy = line_moment(modified_path, (0., 1.))
        self.assertAlmostEqual(perimeter.Wx, Wx)
        self.assertNotAlmostEqual(perimeter.Wy, Wy)

        # Set bending moments
        c.set_lc(lc.LC, Mex=10., Mey=-10.)
        # Evaluate balancing shear
        vsx = c.kx * (abs(lc.Mex)/Wx/c.deff)
        vsy = c.ky * (abs(lc.Mey)/Wy/c.deff)
        vs = sqrt(vsx**2 + vsy**2)
        # Evaluate beta semi-manually
        beta1 = vs*c.deff*u1.length / lc.N
        expected = 1. + beta1

        # Evaluate beta through the developed method
        beta = perimeter.beta

        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_beta_edgex_Myoutward_Mx0(self):
        """Verify the evaluation of beta for
        a column close to an edge along its x-axis.

        We assume that there exists a bending moment
        about the axis parallel to the edge (My in this case),
        causing eccentricity toward the exterior of the slab.
        We further assume that ``Mx`` is zero.

        Under these conditions we expect the factor beta
        to be evaluated according to Eq. (6.39), calculating
        ``W1`` with respect to the perimeters centroid.
        """
        c = self.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Evaluate modified path-moduli
        modified_path = perimeter.evaluate_local_path(u1.centroid)
        Wy = line_moment(modified_path, (0., 1.))
        self.assertNotAlmostEqual(perimeter.Wy, Wy)

        # Set bending moments
        c.set_lc(lc.LC, Mey=-10.)
        # Evaluate balancing shear
        vs = c.ky * (abs(lc.Mey)/Wy/c.deff)
        # Evaluate beta semi-manually
        beta1 = vs*c.deff*u1.length / lc.N
        expected = 1. + beta1

        # Evaluate beta through the developed method
        beta = perimeter.beta

        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_beta_edgex_My0_Mx(self):
        """Verify the evaluation of beta for
        a column close to an edge along its x-axis.

        We assume that there is no bending moment
        about the axis parallel to the edge (My in this case).
        We further assume that ``Mx`` is not zero.

        Under these conditions we expect the factor beta
        to be evaluated according to Eq. (6.39), calculating
        ``W1`` with respect to the perimeters centroid.
        """
        c = self.columns[0]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Set bending moments
        c.set_lc(lc.LC, Mex=10.)
        # Evaluate modified path-moduli
        modified_path = perimeter.evaluate_local_path(u1.centroid)
        Wx = line_moment(modified_path, (1., 0.))
        self.assertAlmostEqual(perimeter.Wx, Wx)

        # Evaluate balancing shear
        vs = c.kx * (abs(lc.Mex)/Wx/c.deff)
        # Evaluate beta semi-manually
        beta1 = vs*c.deff*u1.length / lc.N
        expected = 1. + beta1

        # Evaluate beta through the developed method
        beta = perimeter.beta

        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_beta_edgey_Mxinward_My(self):
        """Verify the evaluation of beta for
        a column close to an edge along its y-axis.

        We assume that there exists a bending moment
        about the axis parallel to the edge (Mx in this case),
        that causes eccentricity toward the interior
        of the slab.  We further assume
        that ``My`` is not zero.

        Under these conditions we expect the factor beta
        to be evaluated according to Eq. (6.44).
        """
        c = self.columns[1]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Set bending moments
        c.set_lc(lc.LC, Mex=-10., Mey=10.)
        # Calculate beta manually
        beta0 = u1.length / u1star.length
        c2 = c.bx
        c1 = c.by
        k644 = c.k639(c1/c2/2)
        beta1 = k644 * (u1.length/perimeter.Wy) * (abs(lc.Mey)/lc.N)
        expected = beta0 + beta1
        # Calucate beta numerically
        beta = perimeter.beta

        self.assertAlmostEqual(beta, expected, delta=0.001*expected)

    def test_evaluate_betai_corner_raises(self):
        c = self.columns[3]
        perimeter = c.ui
        with self.assertRaises(ValueError):
            perimeter.evaluate_betai_corner()

    def test_evaluate_beta_corner(self):
        """Verify evaluate of beta factor for
        corner columns considering both cases
        provided in § 6.4.3(5).
        """
        c = self.columns[2]
        perimeter = c.ui
        u1 = perimeter.path
        u1star = perimeter.truncated
        lc = c.load_cases[0]

        # Case: Inward eccentricity
        # Set bending moments
        c.set_lc(lc.LC, Mex=-0.5, Mey=+0.5)
        # Verify beta
        expected = u1.length / u1star.length
        beta_inward = c.ui.beta
        self.assertAlmostEqual(beta_inward, expected, delta=1e-03*expected)

        # Case: Outward eccentricity
        # Set bending moments
        c.set_lc(lc.LC, Mex=+0.5, Mey=-0.5)
        # Verify beta
        vs = perimeter.evaluate_vsi()[0]
        expected = 1 + vs*c.deff*u1.length/lc.N
        beta_outward = c.ui.beta
        self.assertAlmostEqual(beta_outward, expected, delta=1e-03*expected)
        self.assertGreater(beta_inward, beta_outward)

    def test_evaluate_beta_simplified(self):
        # Internal
        c = self.columns[3]
        perimeter = c.ui

        expected = 1.15
        self.assertAlmostEqual(perimeter.evaluate_beta_simplified(), expected)

        # Edge
        c = self.columns[0]
        perimeter = c.ui

        expected = 1.4
        self.assertAlmostEqual(perimeter.evaluate_beta_simplified(), expected)

        c = self.columns[1]
        perimeter = c.ui
        self.assertAlmostEqual(perimeter.evaluate_beta_simplified(), expected)

        # Corner
        c = self.columns[2]
        expected = 1.5
        perimeter = c.ui
        self.assertAlmostEqual(perimeter.evaluate_beta_simplified(), expected)

    @mock.patch(('dx_punch.EC2.BasicControlPerimeter.'
                'evaluate_vsi'), mock.Mock(return_value=np.ones(1)))
    @mock.patch(('dx_punch.EC2.BasicControlPerimeter.'
                'evaluate_betai_edge'), mock.Mock(return_value=np.ones(1)))
    @mock.patch(('dx_punch.EC2.BasicControlPerimeter.'
                'evaluate_betai_corner'), mock.Mock(return_value=np.ones(1)))
    @mock.patch(('dx_punch.EC2.BasicControlPerimeter.'
                'evaluate_beta_simplified'), mock.Mock(return_value=np.ones(1)))
    def test_evaluate_betai(self):
        """All nested methods have been tested seperately
        so it suffices to assert proper calls in the range
        of cases we consider.
        """
        # Internal columns
        c = self.columns[3]
        perimeter = c.ui

        beta = perimeter.evaluate_betai(simplified=True)
        perimeter.evaluate_beta_simplified.assert_called_once()

        beta = perimeter.evaluate_betai()
        perimeter.evaluate_vsi.assert_called_once()

        # Edge columns
        c = self.columns[0]
        perimeter = c.ui

        beta = perimeter.evaluate_betai()
        perimeter.evaluate_betai_edge.assert_called_once()

        perimeter.evaluate_betai_edge.reset_mock()
        c = self.columns[0]
        perimeter = c.ui

        beta = perimeter.evaluate_betai()
        perimeter.evaluate_betai_edge.assert_called_once()

        # Corner column
        c = self.columns[2]
        perimeter = c.ui

        beta = perimeter.evaluate_betai()
        perimeter.evaluate_betai_corner.assert_called_once()

    def test_evaluate_design_shear_stress(self):
        c = self.columns[0]
        lc = c.load_cases[0]
        c.set_lc(lc.LC, Mex=1., Mey=-1.)
        perimeter = c.ui
        # Set method of evaluation
        beta_config = dict([('approximate', True), ('simplified', False)])
        self.slab.beta_config = beta_config
        # Evaluate and verify
        beta = perimeter.beta
        u1 = perimeter.path
        Ved = lc.N
        d = c.deff
        expected = beta * (Ved/u1.length/d)
        self.assertAlmostEqual(perimeter.ved, expected, delta=1e-03*expected)

        # Set method of evaluation
        self.slab.beta_config['approximate'] = False
        c.ui = None
        # Evaluate and verify
        beta = perimeter.beta
        expected = beta * (Ved/u1.length/d)
        self.assertAlmostEqual(perimeter.ved, expected, delta=1e-03*expected)

        # Set method of evaluation
        self.slab.beta_config['simplified'] = True
        c.ui = None
        # Evaluate and verify
        beta = perimeter.beta
        expected = beta * (Ved/u1.length/d)
        self.assertAlmostEqual(perimeter.ved, expected, delta=1e-03*expected)

    @mock.patch(('dx_punch.EC2.BasicControlPerimeter'
                 '.evaluate_vedi'), mock.Mock(return_value=[None]))
    def test_ved_property(self):
        c = self.columns[0]
        # flush any leaked cache
        c._ved = None
        perimeter = c.ui
        self.assertIsNone(perimeter.ved)
        perimeter.evaluate_vedi.assert_called_once()

    def test_evaluate_effective_shear_force(self):
        # Input parameters
        h = 0.30
        mat = RC[16]
        N = 10e+03
        Mex = 5e+03
        Mey = -5e+03
        # Set elements
        slab = Slab.create_circle(r=10., thickness=h,
                                               material=RC[16])
        slab.add_column(shape='circle', r=0.25, center=(5., 5.), N=N,
                        Mex=Mex, Mey=Mey)
        c = slab.columns[0]
        c.deff = 0.28

        control_perimeter = c.ui
        Ved = control_perimeter.Ved
        self.assertAlmostEqual(Ved, N)

        # Flag the slab as foundation
        slab.foundation = True
        c.soil_pressure = 3e+03 # Less than the concrete-weight per
                                 # unit-thickness
        c.ui = None
        c.recalculate_control_perimeters()
        Ved = c.ui.Ved
        self.assertAlmostEqual(Ved, N)

        # -> dVed negative (No shear)
        c.soil_pressure = 30e+03
        c.ui = None
        c.recalculate_control_perimeters()
        Ved = c.ui.Ved
        dVed = ((c.soil_pressure - slab.material.w*slab.thickness) *
                control_perimeter.area)
        self.assertAlmostEqual(Ved, 0.)

        # -> dVed negative (No shear)
        lc = c.load_cases[0]
        c.set_lc(lc.LC, N=100e+03)
        c.ui = None
        c.recalculate_control_perimeters()
        Ved = c.ui.Ved
        dVed = ((c.soil_pressure - slab.material.w*slab.thickness) *
                c.ui.area)
        self.assertAlmostEqual(Ved, lc.N - dVed)
