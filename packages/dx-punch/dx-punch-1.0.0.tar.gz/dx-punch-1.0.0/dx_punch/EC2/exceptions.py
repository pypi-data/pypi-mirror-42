# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
from dx_utilities.exceptions import CodedException


class ImpossibleShearCages(CodedException):
    """Signify that no valid configuration of
    shear cages can be constructed.
    """
    pass
