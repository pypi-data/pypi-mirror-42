# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
"""Classes and utilities to represent slabs in the context of
punching-shear design according
to the provisions of EC2 (EN-1992-1-1) §6.4.
"""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pprint

from copy import deepcopy
from collections import defaultdict
from math import isclose, atan, asin, tan, sqrt, pi, sin
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

from dx_base.elements import RCSlab
from dx_base.exceptions import *

from dx_eurocode.EC2.formulas import k647
from dx_eurocode.EC2.materials import ReinforcementSteel, RC

from .perimeters import *
from .shear_reinforcement import *
from .forces import InternalForces

from .column import Column


__all__ = ['Slab', 'SlabPostProcessor']


class Slab(RCSlab):
    """
    :param float theta: The prescribed arc-tan of the ratio
        between the effective depth of the slab, and the
        distance of the control perimeter to the boundary
        of a column. In **radians**.
    :param beta_config: A map between the configuration parameters
        for the evaluation of the design stress factor beta, and
        their value::

            {'approximate': True|False,
             'simplified': True|False}

        If ``'approximate'`` is `True` the calculations
        use approximate expressions for the evaluation where
        applicable. If ``'simplified'`` is `True`, the simplified values
        of §6.4.3(6) are used. Among the two declaration, ``'simplified'``
        has higher priority.
    :param str design_situation: The situation to design for. Valid
        values are ``('persistent', 'transient', 'accidental', 'seismic')``
        in consistency with EC0.
    :param str limit_state: The limit state for the design. Valid
        values are ``{ultimate, serviceability}`` in consistency
        with EC0.
    :param float fyk: Characteristic yield strength of reinforcement
        steel. In **MPa**.
    """

    @tolerate_input('theta', 'fyk')
    def __init__(self, theta=atan(1./2.), beta_config=None,
                 design_situation='persistent', limit_state='ultimate',
                 fyk=500., *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theta = theta
        self.control_distance_factor = 1. / tan(self.theta)
        self.beta_config = {
            'approximate': False,
            'simplified': False
            }
        if beta_config is not None:
            self.beta_config.update(beta_config)
        self.design_situation = design_situation
        self.limit_state = limit_state
        self.steel = ReinforcementSteel(fyk)
        self._CRdc = None
        self._vrdmax = None
        self._fywd = None
        self._Aswrtmin = None
        self._index = dict()
        self._passed_columns = None
        self._failed_columns = None
        self._postprocessor = None

    @property
    def postprocessor(self):
        """A postprocessor for the design output.

        :rtype: SlabPostProcessor
        """
        if self._postprocessor is None:
            self._postprocessor = SlabPostProcessor(self)
        return self._postprocessor

    @property
    def passed_columns(self):
        """`Column` instances that pass the
        design checks on each control perimeter,
        organized into a dictionary of the form::

            {'u0': list(Column), 'ui': list(Column)}

        :rtype: collections.defaultdict(list)
        """
        if self._passed_columns is None:
            self._classify_columns()
        return self._passed_columns

    @property
    def failed_columns(self):
        """`Column` instances that have failed the
        design checks on each control perimeter,
        organized into a dictionary::

            {'u0': list(Column), 'ui': list(Column)}

        :rtype: collections.defaultdict(list)
        """
        if self._failed_columns is None:
            self._classify_columns()
        return self._failed_columns

    def _classify_columns(self):
        """Classify columns into failed and passed according
        to the result of the basic checks.
        """
        self._failed_columns = defaultdict(list)
        self._passed_columns = defaultdict(list)
        for c in self.index.values():
            if c.dcr0 > 1.:
                self._failed_columns['u0'].append(c)
            else:
                self._passed_columns['u0'].append(c)
            if c.dcri > 1.:
                self._failed_columns['ui'].append(c)
            else:
                self._passed_columns['ui'].append(c)

    @property
    def index(self):
        """A map between column-ids and `Column` instances::

            {<column-id>: <Column instance>}

        :rtype: dict
        """
        if not self._index:
            self._index = {c._id: c for c in self.columns}
        return self._index

    @property
    def Aswrtmin(self):
        """Minimum shear reinforcement area per unit length
        along the radial direction, per unit length along
        the tangential direction, according to Eq. (9.11).

        ``[m.m/m/m]``

        :rtype: float
        """
        if self._Aswrtmin is None:
            fck = self.material.fck * 1e-06
            fyk = self.steel.fyk * 1e-06
            self._Aswrtmin = 0.08 * sqrt(fck) / fyk
        return self._Aswrtmin

    @property
    def fywd(self):
        """Design yield strength of the shear reinforcement
        bars.

        ``[Pa]``

        :rtype: float
        """
        if self._fywd is None:
            self._fywd = self.steel.fyd(self.design_situation,
                                        self.limit_state)
        return self._fywd

    @property
    def CRdc(self):
        """Factor used in the evaluation of shear capacity.
        See, for example, Eq. (6.47) and Eq. (6.2a).

        :param str design_situation:
        :param str limit_state:
        :rtype: float
        """
        if self._CRdc is None:
            self._CRdc = self.material.CRdc(self.design_situation,
                                            self.limit_state)
        return self._CRdc

    @property
    def vrdmax(self):
        """Maximum design shear stress evaluated from Eq. (6.5).

        ``[Pa]``

        :param str design_situation:
        :param str limit_state:
        :rtype: float
        """
        if self._vrdmax is None:
            self._vrdmax = self.material.vrdmax(self.design_situation,
                                                self.limit_state)
        return self._vrdmax

    @property
    def columns(self):
        """A list of the dependent `Column` instances.

        :rtype: list(Column)
        """
        return self.agents['columns']

    @columns.setter
    def columns(self, value):
        self.agents['columns'] = value

    def add_to_index(self, column):
        """Add a column to the dedicated `index`.

        :param Column column:
        """
        self._index[column._id] = column

    def add_column(self, *args, **kwargs):
        """Add a `Column` instance to the respective container
        of agents of this slab.

        The method updates a dedicated index of columns based on
        their user-defined id.

        :param ``*args``: See `Column` instantiation signature.
        :param ``**kwargs``: See `Column` instantiation signature.
        """
        #TODO: Check if added column intersects existing ones
        #      and raise an exception if True.
        column = self.index.get(kwargs.get('_id'))
        if column is None:
            self.add_agent(label='columns', agent_type=Column, slab=self,
                           *args, **kwargs)
            self.add_to_index(self.columns[-1])
        else:
            column.add_new_lc(*filter(
                None, map(kwargs.get, ['LC', 'N', 'Mex', 'Mey'])
                ))

    def merge_columns(self, id0, id1, remove_sources=True):
        """Merge columns with ``id0`` and ``id1``
        so that they are checked as a single column
        for punching.

        If successful, the resulting column is assigned
        the id ``<id0>m``.

        :param str id0:
        :param str id1:
        :param bool remove_sources: If `True` delete the
            merged columns from ``self.index`` and
            ``self.columns``.
        """
        s = self.index[id0]
        t = self.index[id1]
        lcs = set([*s.lc_index, *t.lc_index])
        new_shape = s.more.union(t.more)
        try:
            new_shape.geoms
            new_shape = new_shape.envelope.boundary.coords
        except AttributeError:
            new_shape = new_shape.boundary.coords

        new_id = id0+'m'
        for lc in lcs:
            load_cases = list(
                filter(None, [s.lc_index.get(lc), t.lc_index.get(lc)])
                )
            new_lc = sum(load_cases, InternalForces(LC=lc))
            N, Mex, Mey = new_lc.N, new_lc.Mex, new_lc.Mey

            self.add_column(shape='generic', vertices=new_shape, _id=new_id,
                            LC=lc, N=N, Mex=Mex, Mey=Mey)
            c = self.index[new_id]
            c.add_pile_reaction(
                lc, s.reactions.get(lc, 0.)+t.reactions.get(lc, 0.)
                )
        if remove_sources:
            del self.index[id0]
            del self.index[id1]
        self.recreate_columns_from_index()

    def recreate_columns_from_index(self):
        """Recreate `columns` container from the index."""
        self.columns = list(self.index.values())

    def add_tension_rebar_raw(self, *args, **kwargs):
        """Expand parent-class method to update
        the effective depth in the vicinity of any columns.

        :param ``*args``: See signature of |RCSlab.add_tension_rebar_raw|.
        :param ``**kwargs``: See signature of |RCSlab.add_tension_rebar_raw|.
        """
        super().add_tension_rebar_raw(*args, **kwargs)
        for c in self.columns:
            c.update_effective_depth()
            c.recalculate_control_perimeters()

    def add_partial_rebar(self, *args, **kwargs):
        """Wrap the `add_rebar_raw <dx_base.elements.RCSlab.add_rebar_raw>`
        method to add reinforcement
        on a limited region of the slab. This method invokes
        the |PlanarShape.new| to generate the associated geometry.

        :param ``*args``: See signature of |RCSlab.add_partial_rebar|.
        :param ``**kwargs``: See signature of |RCSlab.add_partial_rebar|.
        """
        super().add_partial_rebar(*args, **kwargs)
        for c in self.columns:
            c.update_effective_depth()
            c.recalculate_control_perimeters()

    def to_json(self):
        """Produce a json output.

        :rtype: str
        """
        json_output = {'Columns': {}}
        for c in self.columns:
            json_output['Columns'][c._id] = c.to_json()

        return json.dumps(json_output)

    @classmethod
    def from_json(cls, json_input):
        """Create an instance from a json-loaded input structure.

        :param dict json_input: The input data.
        :rtype: Slab
        """
        # Basic config
        geometry = json_input['geometry']
        slab_type = json_input['type']
        materials = json_input['materials']
        new = cls.new(**geometry, slab_type=slab_type,
                      material=RC[materials['fck']], fyk=materials['fyk'])
        # Reinforcement
        uniform = json_input['reinforcement'].get('uniform', {})
        partial = json_input['reinforcement'].get('partial', {})
        for config in uniform:
            new.add_uniform_rebar(**config)
        for config in partial:
            new.add_partial_rebar(**config)
        # Columns
        for data in json_input['columns']:
            geometry = data['geometry']
            if geometry['shape'] == 'circle':
                origin = geometry['center']
                key = 'center'
            else:
                origin = geometry['origin']
                key = 'origin'

            geometry[key] = tuple(map(float, map(origin.get, ("x", "y"))))
            for lc in data['load-cases']:
                new.add_column(**geometry, _id=data['id'],
                               LC=lc['name'], N=lc['N'], Mex=lc['Mex'],
                               Mey=lc['Mey'])
            column = new.columns[-1]
            drop_panel = data.get('drop-panel')
            if drop_panel:
                column.set_drop_panel(**drop_panel)
        return new


class SlabPostProcessor(object):
    """Wrap postprocessing utilities for a slab instance.

    :param Slab slab:
    """

    def __init__(self, slab):
        self.slab = slab

    def plot_geometry(self):
        """Plot geometric overview of slab, columns
        and their drop-panels.
        """
        fig, ax = plt.subplots()
        # First subplot
        ax.set_aspect('equal')
        ax.plot(self.slab.boundary.xy[0], self.slab.boundary.xy[1],
                label=f'Slab (t: {self.slab.thickness*1e+03:.1f} mm)')
        ax.set_title('Overview')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='minor')
        hd = None
        for c in self.slab.index.values():
            hc = ax.plot(c.boundary.xy[0], c.boundary.xy[1], 'k')
            ax.text(c.centroid.x, c.centroid.y, c._id)
            if c.drop_panel:
                path = c.drop_panel.boundary
                hd = ax.plot(path.xy[0], path.xy[1], 'm')
        hc[0].set_label('Columns')
        if hd:
            hd[0].set_label('Drop panels')
        ax.legend()
        return fig, ax

    def plot_u0(self):
        """Plot the demand-to-capacity ratio
        on the sides of each column.
        """
        fig, ax = plt.subplots()
        # Second subplot
        ax.plot(self.slab.boundary.xy[0], self.slab.boundary.xy[1])
        ax.set_title('Demand-to-capacity ratio (u0)')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='minor')
        for c in self.slab.passed_columns['u0']:
            ax.plot(c.u0.path.xy[0], c.u0.path.xy[1], 'g')
            ax.text(c.centroid.x, c.centroid.y, f'{c.dcr0:.3f}')
        for c in self.slab.failed_columns['u0']:
            ax.plot(c.u0.path.xy[0], c.u0.path.xy[1], 'r')
            ax.text(c.centroid.x, c.centroid.y, f'{c.dcr0:.3f}')

    def plot_ui(self, show_legend=True):
        """Plot the demand-to-capacity ratio
        on the basic control perimeter.
        """
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        # Third subplot
        ax.plot(self.slab.boundary.xy[0], self.slab.boundary.xy[1],
                linewidth=2.)
        ax.set_title('Demand-to-capacity ratio (ui)')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='minor')
        p, f = None, None
        for c in self.slab.passed_columns['ui']:
            p = ax.plot(c.ui.path.xy[0], c.ui.path.xy[1], 'g',
                        linewidth=0.8)
            ax.plot(c.boundary.xy[0], c.boundary.xy[1], 'k',
                    linewidth=0.8)
            ax.text(c.centroid.x, c.centroid.y, f'{c.dcri:.3f}')
        for c in self.slab.failed_columns['ui']:
            f = ax.plot(c.ui.path.xy[0], c.ui.path.xy[1], 'r',
                        linewidth=0.8)
            ax.plot(c.boundary.xy[0], c.boundary.xy[1], 'k',
                    linewidth=0.8)
            ax.text(c.centroid.x, c.centroid.y, f'{c.dcri:.3f}')
        if f:
            f[0].set_label('Shear reinforcement required')
        if p:
            p[0].set_label('Passing')
        if show_legend:
            ax.legend()
        return fig, ax

    def plot_drop_panels(self, columns=None):
        """Plot layout of columns with drop-panels. If no specific
        set of columns is given all columns with drop-panels are
        displayed.

        :param columns: The columns for which to print
            the effective tensile area.
        :type columns: iterable or None
        """
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        # Third subplot
        ax.plot(self.slab.boundary.xy[0], self.slab.boundary.xy[1],
                linewidth=2.)
        ax.set_title('Details of drop-panels')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='minor')
        columns = columns or self.slab.columns
        for c in columns:
            drop_panel = c.drop_panel
            if drop_panel:
                ax.plot(c.boundary.xy[0], c.boundary.xy[1], 'k',
                        linewidth=0.7)
                ax.plot(drop_panel.boundary.xy[0], drop_panel.boundary.xy[1],
                        color='m', linewidth=0.7)
        return fig, ax

    def plot_effective_tensile_area(self, columns=None):
        """Plot layout of effective area of tensile reinforcement
        in accordance with §6.4.4(1) and the specifications of
        the section for which the :math:`\\rho` ratios are evaluated.

        If no columns are given, the columns failing
        at the control perimeter :math:`\\text{u}_1` are displayed.

        :param columns: The columns for which to print
            the effective tensile area.
        :type columns: iterable or None
        """
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        # Third subplot
        ax.plot(self.slab.boundary.xy[0], self.slab.boundary.xy[1],
                linewidth=2.)
        ax.set_title('Details of columns with additional reinforcement',
                     fontsize='medium')
        ax.set_xlabel('x [m]', fontsize='small')
        ax.set_ylabel('y [m]', fontsize='small')
        ax.grid()
        ax.minorticks_on()
        ax.grid(which='minor')
        columns = columns or self.slab.failed_columns['ui']
        for c in columns:
            ax.plot(c.boundary.xy[0], c.boundary.xy[1], 'k',
                    linewidth=0.7)
            region = c.tensile.effective_region
            hr = ax.plot(region.boundary.xy[0], region.boundary.xy[1], 'b',
                         linewidth=0.5)
            ax.text(c.centroid.x, c.centroid.y, f'{c._id}',
                    fontname='sans-serif', fontsize='x-small')
        return fig, ax

    def print(self, filename=None, DIR='./'):
        """Print design output.

        :param filename: The optional filename
            to print the output on.
        :type filename: str or None
        :param str DIR: The path to save
            any optional file given.
        """
        to_file = True if filename else False
        printout = []
        for c in self.slab.index.values():
            printout.append(c.print(to_file))

        if filename:
            with open(os.path.join(DIR, filename), 'w') as f:
                f.write('\n'.join(printout))

    def assemble_data(self, dataclass='shear-reinforcement', *args, **kwargs):
        """Assemble data as derived from the design procedure of
        each column, grouped by ``dataclass``.

        :param str dataclass: The category of the data. Valid values
            are::

                {'shear-reinforcement', 'tensile-reinforcement',
                'design-checks', 'drop-panels'}

        :param ``*args``: Any additional positional arguments that can
            be passed in the assembler methods.
        :param ``**kwargs``: Any additional keyword arguments that can
            be passed in the assembler methods.
        :rtype: tuple(dict) or dict
        :raises CodedValueError: If an unknown ``dataclass`` is requested.
        """
        if dataclass == 'shear-reinforcement':
            assembler = self._assemble_shear_reinforcement_data
        elif dataclass == 'tensile-reinforcement':
            assembler = self._assemble_tensile_reinforcement_data
        elif dataclass == 'design-checks':
            assembler = self._assemble_design_data
        elif dataclass == 'drop-panels':
            assembler = self._assemble_drop_panel_data
        else:
            raise CodedValueError(4008, f'Unsupported data-class {dataclass}')
        return assembler(*args, **kwargs)

    def create_dataframes(self, dataclass='shear-reinforcement'):
        """Wrapper of methods creating dataframes from a set
        of aggregated data derived from the design procedure.

        :param str dataclass: The category of the data. Valid values
            are::

                {'shear-reinforcement', 'tensile-reinforcement',
                'design-checks', 'drop-panels'}

        :rtype: pandas.DataFrame or tuple(pandas.DataFrame)
        :raises CodedValueError: If an unknown ``dataclass`` is requested.
        """
        if dataclass == 'shear-reinforcement':
            return self._create_shear_reinforcement_dataframes()
        elif dataclass == 'tensile-reinforcement':
            return self._create_tensile_reinforcement_dataframes()
        elif dataclass == 'design-checks':
            return self._create_design_data_dataframes()
        elif dataclass == 'drop-panels':
            return self._create_drop_panel_dataframes()
        else:
            raise CodedValueError(4009, f'Unsupported data-class {dataclass}')

    def _assemble_drop_panel_data(self):
        """Assemble drop-panel geometry data for
        all columns that are configured to one

        :rtype: dict
        """
        drop_panels = {}
        for column in self.slab.columns:
            drop_panel = column.output.get('Drop panel')
            if drop_panel:
                drop_panels[column._id] = drop_panel

        return drop_panels

    def _assemble_shear_reinforcement_data(self):
        """Assemble data for shear reinforcement as derived
        by the design procedure of each column that fails
        the basic check.

        The method distinguishes between basic shear
        reinforcement and diagonal fillups.

        :rtype: tuple(dict, dict)
        """
        basic_cage = {}
        diag_cage = {}
        for column in self.slab.failed_columns['ui']:
            i = column.basic_control_perimeters.index(column.ui) + 1
            try:
                data = (column.output['Design']
                                     ['Perimeter u%d' % i]
                                     ['Shear Reinforcement'])
            except KeyError as e:
                data = {'Error': str(e)}
            try:
                diag_cage_data = data.get('Diagonal', None)
            except AttributeError:
                diag_cage_data = None
            if diag_cage_data:
                diag_cage[column._id] = diag_cage_data
            basic_cage[column._id] = data.get('Basic')

        return basic_cage, diag_cage

    def _create_drop_panel_dataframes(self):
        """Create pandas dataframes containing data
        for the geometry of the drop-panels.

        :rtype: pd.DataFrame
        """
        return pd.DataFrame.from_dict(self._assemble_drop_panel_data(),
                                      orient='index')

    def _create_shear_reinforcement_dataframes(self):
        """Create pandas dataframes containing data
        of shear reinforcement.

        :rtype: tuple(pd.DataFrame, pd.DataFrame)
        """
        return tuple(
            df.T for df in map(pd.DataFrame.from_dict,
                               self._assemble_shear_reinforcement_data())
            )

    def _assemble_tensile_reinforcement_data(self):
        """Assemble data for tensile reinforcement as derived
        by the design procedure of each column.

        :rtype: dict
        """
        trebar_data = {}
        for c in self.slab.columns:
            data = deepcopy(c.output)
            trebar = data['Tensile Reinforcement']
            region = trebar.pop('Effective tensile region')
            trebar_data[c._id] = {'deff [mm]': data['Effective depth [mm]'],
                                  **region, **trebar}
        return trebar_data

    def _create_tensile_reinforcement_dataframes(self):
        """Create pandas dataframes containing data
        of tensile reinforcement.

        :rtype: pd.DataFrame
        """
        return pd.DataFrame.from_dict(
            self._assemble_tensile_reinforcement_data(), orient='index'
            )

    def _assemble_design_data(self, perimeter='ui'):
        """Assemble data for the design checks at the basic
        control perimeters of each column.

        :rtype: dict
        """
        out = {}
        for c in self.slab.columns:
            if perimeter == 'ui':
                i = c.basic_control_perimeters.index(c.ui) + 1
                pmax = 'u%d' % i
            else:
                pmax = perimeter
            data = deepcopy(c.output['Design']['Perimeter %s' % pmax])
            data.pop('Shear Reinforcement', None)
            loads = data.pop('Most adverse loadcase')
            out[c._id] = {'combination': loads.pop('name'), **loads, **data}
        return out

    def _create_design_data_dataframes(self):
        """Create pandas dataframes that contain data
        derived from the design checks at the basic control
        perimeters.

        :rtype: tuple(pd.DataFrame, pd.DataFrame)
        """
        u0 = pd.DataFrame.from_dict(self._assemble_design_data('u0'), orient='index')
        ui = pd.DataFrame.from_dict(self._assemble_design_data('ui'), orient='index')
        return u0, ui
