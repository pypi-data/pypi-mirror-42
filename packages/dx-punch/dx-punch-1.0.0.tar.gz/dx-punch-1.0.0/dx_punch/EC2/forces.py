# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
from dx_base.forces import NMyMz


class InternalForces(NMyMz):

    def __init__(self, LC='LC0', N=0., Mex=0., Mey=0., *args, **kwargs):
        super().__init__(LC=LC, N=N, My=Mex, Mz=Mey, **kwargs)
        self.Mex = self.My
        self.Mey = self.Mz

    @property
    def container(self):
        """List of nodal forces ``[N, Mex, Mey]``

        :rtype: list
        """
        return [self.N, self.Mex, self.Mey]
