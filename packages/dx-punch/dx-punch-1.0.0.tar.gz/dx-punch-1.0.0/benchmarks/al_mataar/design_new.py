from collections import defaultdict
from dx_punch.EC2 import Slab, Column
from dx_punch.EC2.slab import SlabPostProcessor
from dx_eurocode.EC2.materials import RC

import matplotlib.pyplot as plt
from .input_data import slab_coords, columns, stresses, elements, piles

critical_lcs = {
# take4
'ULS10',
'ULS8',
'ULS9',
'ULS_Wind XY(+)18',
'ULS_Wind XY(+)5',
'ULS_Wind XY(+)6',
'ULS_Wind XY(+)7',
'ULS_Wind XY(+)8'
# take5
#     'ULS10', 'ULS8', 'ULS_Wind XY(+)19',
#     'ULS_Wind XY(+)25', 'ULS_Wind XY(+)5',
#     'ULS_Wind XY(+)6', 'ULS_Wind XY(+)7',
#     'ULS_Wind XY(+)8'
}

exclude_columns = {
    76, 75, 87, 74, 73, 94, 95, 1, 6, 7, 14, 92,
    2, 3, 4, 12, 13, 34, 5, 8, 16, 17, 18, 40, 41,
    19, 25, 28, 29, 39, 49, 50, 46, 77, 48
    }
exclude_columns = {f'B{c}' for c in exclude_columns}

columns_with_drop_panel = {
    # 'B9', 'B10', 'B11', 'B15', 'B35', 'B36', 'B38', 'B66', 'B67',
    # 'B68', 'B70', 'B71', 'B72', 'B82', 'B84', 'B85', 'B86',
    # 'B43B44', 'B42B45', 'B51B52', 'B81B80',
    # 'B62B63', 'B59B60', 'B57B58', 'B55B56', 'B53B54', 'B61',
    # 'B79B78'
    }

augmented_dp = {'B15', 'B84'}
drop_panels = {
    'default' : {'lx': 1.8, 'height': 0.80},
    'merged': {'lx': 1.2, 'height': 0.8},
    'B42B45': {'lx': 1.8, 'height': 0.80},
    'B43B44': {'lx': 1.8, 'height': 0.80},
    'B51B52': {'lx': 1.8, 'height': 0.80},
    'B81B80': {'lx': 1.8, 'height': 0.80},
    'add' : {'lx': 2.2, 'height': 0.80},
    'B42B45' : {'lx': 2.4, 'height': 0.80},
    'B85' : {'lx': 3.0, 'height': 0.80},
    # 'B79B78' : {'lx': 2.5, 'height': 0.90},
    }

b43origin = columns['B43']['geometry']['origin']
p43origin = (b43origin[0]-0.5, b43origin[1]-1.05)
b25origin = columns['B25']['geometry']['origin']
b19origin = (b25origin[0]+0.9, b25origin[1]+0.875)
precise_columns = {
    'B44': {
        'geometry': {'bx': .5, 'by': 1.1, 'origin': p43origin}
        },
    'B19': {
        'geometry': {'bx': 1.3, 'by': 1.0, 'origin': b19origin}
        },
    }
for label in precise_columns:
    columns[label]['geometry'].update(precise_columns[label]['geometry'])

slab = Slab.new(shape='generic', vertices=slab_coords, slab_type='raft',
                material=RC[45], thickness=0.9)
# Add soil pressure
for clc in critical_lcs:
    slab.add_discrete_soil_pressure(
        coords=[elements[_id] for _id in stresses[clc]],
        values=stresses[clc].values(), lc=clc
        )
# slab.add_soil_pressure(value=100e+03)
phi, s, d = 0.02, 0.15, 0.78
slab.add_uniform_rebar(phi, s, d, axes='xy')
# phi, s, d = 0.025, 0.075, 0.74
# slab.add_uniform_rebar(phi, s, d, axes='xy')
for label in columns:
    if label in exclude_columns:
        continue
    geometry = columns[label]['geometry']
    bx, by = geometry['bx'], geometry['by']
    centroid = geometry['origin']
    for lc in columns[label]['forces']:
        forces = columns[label]['forces'][lc]
        slab.add_column(bx=bx, by=by, origin=centroid, _id=label, LC=lc,
                        N=forces['N'], Mex=forces['Mex'], Mey=forces['Mey'])
        c = slab.index[label]
        if piles.get(label):
            try:
                c.add_pile_reaction(lc, piles[label][lc])
            except:
                print(label)
                raise
# Merge columns
columns_to_merge = [
    ('B53', 'B54'),
    ('B64', 'B65'),
    ('B62', 'B63'),
    ('B59', 'B60'),
    ('B57', 'B58'),
    ('B55', 'B56'),
    ('B79', 'B78'),
    # ('B74', 'B73'),
    ('B43', 'B44'),
    ('B42', 'B45'),
    ('B51', 'B52'),
    ('B30', 'B31'),
    ('B81', 'B80'),
    # ('B19', 'B25'),
    # ('B40', 'B41'),
    # ('B29', 'B28'),
    # ('B49', 'B50'),
    # ('B46', 'B47'),
    # ('B46B47', 'B48'),
    # ('B43', 'P43'),
    ]

for id0, id1 in columns_to_merge:
    slab.merge_columns(id0, id1)

# Set drop panels
for _id in columns_with_drop_panel:
    config = drop_panels.get(_id)
    if _id in augmented_dp:
        config = drop_panels['add']
    if config is None:
        if len(_id) > 3:
            config = drop_panels['merged']
        else:
            config = drop_panels['default']
    slab.index[_id].set_drop_panel(**config)

# Additional reinforcement
def additional_rebar():
    set1 = {
        'B9', 'B10', 'B11', 'B15', 'B26', 'B27', 'B33', 'B35', 'B36',
        'B38', 'B47', 'B66', 'B67', 'B68', 'B70', 'B71', 'B72',
        'B82', 'B83', 'B84', 'B85', 'B88', 'B64B65', 'B62B63',
        'B43B44', 'B42B45', 'B30B31', 'B79B78'
        }

    set2 = set([
        'B11', 'B15', 'B33', 'B47', 'B70', 'B83', 'B84', 'B85', 'B62B63',
        'B42B45', 'B79B78'
        ])
    set4 = set([
        'B15', 'B47', 'B84', 'B85', 'B42B45'
        ])
    set3 = set([
        ])

    default_rebar = {'phi': 0.025, 's': 0.075, 'd': 0.74}
    set2_rebar = {'phi': 0.025, 's': 0.05, 'd': 0.74}
    set3_rebar = {'phi': 0.032, 's': 0.075, 'd': 0.74}
    set4_rebar = {'phi': 0.040, 's': 0.100, 'd': 0.74}
    for _id in set1:
        if _id in set4:
            rebar = set4_rebar
        elif _id in set3:
          rebar = set3_rebar
        elif _id in set2:
            rebar = set2_rebar
        else:
            rebar = default_rebar
        c = slab.index[_id]
        shape = c.create_by_offset(c, dx=4*c.deff, dy=4*c.deff)
        shape = shape.intersection(slab)
        slab.add_partial_rebar(**rebar, shape='generic', axes='xy',
                vertices=shape.boundary.coords)
    return set1-set2-set3-set4, set2-set3-set4, set3-set4, set4

set1, set2, set3, set4 = additional_rebar()

import pandas as pd

postprocessor = SlabPostProcessor(slab)
basic_df, diag_df = postprocessor.shear_reinforcement_dataframes()
