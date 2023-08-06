import re
import csv
import pickle
from collections import defaultdict


filename = 'mesh-geometry.csv'
reg_mid = re.compile('(?P<id>\d+$)')

mesh_geometry = {}
nskip = 2
with open(filename) as f:
    reader = csv.reader(f, delimiter=';')
    i = 0
    for row in reader:
        if i < nskip:
            i += 1
            continue
        _id = reg_mid.search(row[1].strip()).group('id')
        mesh_geometry[_id] = tuple(v*1e-03 for v in map(float, row[2:-1]))


filename = 'contact_stresses.pkl'

with open(filename, 'rb') as f:
    stresses = pickle.load(f)

elements = mesh_geometry
with open('mesh_geometry.pkl', 'wb') as f:
    pickle.dump(mesh_geometry, f)
