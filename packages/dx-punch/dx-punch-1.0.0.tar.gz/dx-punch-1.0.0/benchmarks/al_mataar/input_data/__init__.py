import pickle
import os

DIR = os.path.dirname(os.path.abspath(__file__))
take = 'take4'

with open(os.path.join(DIR, take, 'slab.pkl'), 'rb') as f:
    slab_coords = pickle.load(f)

with open(os.path.join(DIR, take, 'columns.pkl'), 'rb') as f:
    columns = pickle.load(f)

with open(os.path.join(DIR, take, 'contact_stresses.pkl'), 'rb') as f:
    stresses = pickle.load(f)

with open(os.path.join(DIR, take, 'mesh_geometry.pkl'), 'rb') as f:
    elements = pickle.load(f)

with open(os.path.join(DIR, take, 'pile_reactions.pkl'), 'rb') as f:
    piles = pickle.load(f)
