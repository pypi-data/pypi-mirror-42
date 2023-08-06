import unittest


from dx_punch.EC2 import Slab


class TestSlab(unittest.TestCase):

    def setUp(self):
        self.input = {
            'type': 'floor-slab', # {['floor-slab'], 'raft', 'base'}
            'geometry': {
                'bx': "6.25", # breadth along x
                'by': "11.45", # breadh along y
                'thickness': "0.30",
                # Position of the origin of the coordinate-system of the shape (one of the four vertices of the rectangle,
                # or the centroid)
                'position': 'lower-left' # {'lower-left', 'lower-right', 'upper-left', 'upper-right', ['centroid']}
                },
            'materials': {
                'fck': "30", # Characteristic cylinder strength of concrete [MPa]
                'fyk': "500" # Characteristic yield strength of steel [MPa]
                },
            'reinforcement': { # Distribution of reinforcement on the slab
                'uniform': [{
                    # The axis along which the bars are distributed
                    'axes': 'xy', # {['x'], 'y', 'xy'}. If 'xy', it is
                                  # assumed that reinforcement is uniform along
                                  # both axes
                    'phi': "0.010", # bar diameter [m]
                    's': "0.200", # spacing [m]
                    'd': "0.27" # effective depth [m]
                    },
                    ],
                },
            'soil-pressure': [{
                'LC': 'LC0',
                'value': "0." # [Pa]
                },
                ],
            'columns': [{
                'id': 'C0',
                'geometry': {
                    'shape': 'rectangle',
                    'bx': "0.25",
                    'by': "0.25",
                    'origin': {"x": "5.", "y": "5."},
                    },
                'load-cases': [{
                    'name': 'LC0',
                    'N': "111e+03",  # Compressive force [N]
                    'Mex': "25e+03", # [N.m]
                    'Mey': "22e+03", # [N.m]
                    },],
                'drop-panel': {
                    'lx': "0.4", # Offset from the column sides along x [m]
                    'ly': "0.6", # Optional: If ommited it is assumed that lx=ly [m]
                    'height': "0.2"  # Height of the drop-panel [m]
                    }
                }
                ]
            }

    def test_from_dict(self):
        slab = Slab.from_json(self.input)
