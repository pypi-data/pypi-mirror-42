import unittest
import numpy as np

from dx_punch.EC2.column import ColumnForces


class TestColumnForces(unittest.TestCase):

    def test_add_new_lc(self):
        c = ColumnForces()
        self.assertIsNotNone(c.lc_index['LC0'])
        c.add_new_lc('new-lc', 10., 150., 18.)
        self.assertEqual(len(c.Ni), 2)
        Mexi = np.array([0., 150.])
        np.testing.assert_equal(c.Mexi, Mexi)
