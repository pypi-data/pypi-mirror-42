from EC2.punching_shear import Slab, Column
from EC2.materials import RC

import matplotlib.pyplot as plt
from .input_data import slab_coords, columns

exclude_columns = {
    77, 76, 75, 87, 74, 73, 94, 95, 1, 6, 7, 14, 92
    }
exclude_columns = {f'B{c}' for c in exclude_columns}

columns_with_drop_panel = {
    'B10', 'B11', 'B35', 'B38', 'B36', 'B37',
    'B68', 'B66', 'B67', 'B84', 'B86', 'B85',
    'B27', 'B26', 'B42B45', 'B15', 'B61', 'B62B63',
    'B59B60', 'B57B58', 'B55B56', 'B53B54', 'B30B31'
    }

drop_panels = {
    'default' : {'lx': 1.8, 'height': 0.7},
    'merged': {'lx': 1.8, 'height': 1.1},
    'B42': {'lx': 1.8, 'height': 0.35},
    'B30B31': {'lx': 1.8, 'height': 0.7},
    'B42B43': {'lx': 1.8, 'height': 0.7}
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
slab.add_soil_pressure(value=300e+03)
phi, s, d = 0.02, 0.15, 0.8
slab.add_uniform_rebar(phi, s, d, axes='xy')
for label in columns:
    if label in exclude_columns:
        continue
    geometry = columns[label]['geometry']
    bx, by = geometry['bx'], geometry['by']
    centroid = geometry['origin']
    for lc in columns[label]['forces']:
        forces = columns[label]['forces'][lc]
        slab.add_column(bx=bx, by=by, ref=centroid, _id=label, LC=lc,
                        N=forces['N'], Mex=forces['Mex'], Mey=forces['Mey'])
# Merge columns
columns_to_merge = [
    ('B53', 'B54'),
    ('B64', 'B65'),
    ('B62', 'B63'),
    ('B59', 'B60'),
    ('B57', 'B58'),
    ('B55', 'B56'),
    # ('B74', 'B73'),
    ('B43', 'B44'),
    ('B42', 'B45'),
    ('B51', 'B52'),
    ('B30', 'B31'),
    ('B81', 'B80'),
    ('B19', 'B25'),
    ('B40', 'B41'),
    ('B29', 'B28'),
    ('B49', 'B50'),
    ('B46', 'B47'),
    ('B46B47', 'B48'),
    # ('B43', 'P43'),
    ]

for id0, id1 in columns_to_merge:
    slab.merge_columns(id0, id1)

# Set drop panels
for _id in columns_with_drop_panel:
    config = drop_panels.get(_id)
    if config is None:
        if len(_id) > 3:
            config = drop_panels['merged']
        else:
            config = drop_panels['default']
    for lc in slab.index[_id]:
        slab.index[_id][lc].set_drop_panel(**config)

# Additional reinforcement
add_rebar = {
    'B81B80': {
        'geometry': {'dx': 3.4, 'dy': 4},
        'rebar': {
            'x': {'phi': 0.025, 's': 0.075, 'd': 0.79},
            'y': {'phi': 0.025, 's': 0.075, 'd': 0.78},
            }
        },
    'B43B44': {
        'geometry': {'dx': 3.3, 'dy': 4},
        'rebar': {
            'xy': {'phi': 0.025, 's': 0.075, 'd': 0.78},
            }
        },
    'B9': {
        'geometry': {'dx': 4.2, 'dy': 6},
        'rebar': {
            'xy': {'phi': 0.020, 's': 0.075, 'd': 0.79},
            }
        },
    }
for _id, config in add_rebar.items():
    c = next(iter(slab.index[_id].values()))
    shape = c.create_by_offset(c, **config['geometry'])
    shape = shape.intersection(slab)
    for axes, rebar in config['rebar'].items():
        slab.add_partial_rebar(**rebar, shape='generic', axes=axes,
                               vertices=shape.boundary.coords)

def plot(columns=None, color='r', text=False):
    plt.plot(slab.boundary.xy[0], slab.boundary.xy[1])
    if columns is None:
        columns = slab.columns
    for c in columns:
        plt.plot(c.boundary.xy[0], c.boundary.xy[1], color)
        if text:
            plt.text(c.centroid.x, c.centroid.y, c._id)
        # plt.plot(c.u1.path.xy[0], c.u1.path.xy[1], 'g')
