# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
"""Classes and functions to represent and handle
the types of shear reinforcement discussed in
§6.4.5(3).
"""
from math import pi


__all__ = ['ShearCage']


class ShearCage(object):
    """Represent any shear-cage reinforcement that may be
    present, or required, in the vicinity of the columns
    of the slab.

    :param Aswr: Total area of reinforcement bars per unit
        radial length.
    :type Aswr: float or None
    :param csx: Breadth of shear reinforcement cage distributed
        along the **x**-axis.
    :type csx: float or None
    :param csy: Breadth of shear reinforcement cage distributed
        along the **y**-axis.
    :type csy: float or None
    :param float angle: The angle of the reinforcement bars with the
        level of the slab.
    """
    def __init__(self, Aswr=None, csx=None, csy=None, angle=pi/2.):
        self.Aswr = Aswr
        self.csx = csx
        self.csy = csy
        self.angle = angle
