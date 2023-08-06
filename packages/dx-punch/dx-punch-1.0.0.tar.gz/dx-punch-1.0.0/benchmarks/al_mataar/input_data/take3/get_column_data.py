import re
import csv
import pickle
from collections import defaultdict

from resolve_combinations import parse_combination_key

with open('key_to_exploded.pkl', 'rb') as f:
    lckey_to_exploded = pickle.load(f)

filename = 'internal-forces-2.csv'

columns = defaultdict(dict)
with open(filename) as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        if float(row[2]) > 0:
            continue
        N = row[4].replace(',', '.')
        Mx = row[9].replace(',', '.')
        My = row[8].replace(',', '.')
        columns[row[0]][row[3]] = {
            'N': -float(N)*1e+03,
            'Mex': -float(Mx)*1e+03, # -Mz
            'Mey': float(My)*1e+03, # My
            }
raw_columns = dict(columns)

filename = 'pile_reactions/pile_reactions.pkl'
with open(filename, 'rb') as f:
    piles = pickle.load(f)

# for c in piles:
#     for LC in columns[c]:
#         eLC = lckey_to_exploded[parse_combination_key(LC)]
#         dN = piles[c].get(eLC, 30e+06)
#         old_value = columns[c][LC]['N']
#         columns[c][LC]['N'] -= dN
#         new_value = columns[c][LC]['N']

eligible = defaultdict(dict)
for label in columns:
    for LC in columns[label]:
        eLC = lckey_to_exploded[parse_combination_key(LC)]
        data = columns[label][LC]
        if data['N'] > 0.:
            eligible[label][eLC] = data

nodes = {}
with open('node-data.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        nodes[row[1]] = tuple([float(c.replace(',', '.')) for c in row[2:]])

column_nodes = {}
breadth_reg = re.compile("\((?P<bx>\d+);\s+(?P<by>\d+)\)")
columns = defaultdict(dict)
with open('column-nodes.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        label = row[1]
        m = breadth_reg.search(row[2])
        bx = float(m.group('bx'))*1e-03
        by = float(m.group('by'))*1e-03
        node = row[6]
        origin = tuple(nodes[node][:-1])
        if label == 'B44':
            by = 1.05
            cy = origin[1] + 0.025
            origin = (origin[0], cy)
        if label in eligible:
            columns[label]['forces'] = eligible[label]
            columns[label]['geometry'] = dict(
                [('bx', bx), ('by', by), ('origin', origin)]
                )

# Add new column
columns['B2602']['forces'] = eligible['B2602']
columns['B2602']['geometry'] = {
    'bx': 0.5,
    'by': 1.,
    'origin': (5.545, 92.032)
    }

with open('columns.pkl', 'wb') as f:
    pickle.dump(columns, f)

slab = []
with open('slab-nodes.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        node = row[0]
        slab.append(tuple(nodes[node][:-1]))

with open('slab.pkl', 'wb') as f:
    pickle.dump(slab, f)

# Post-processing
maxN = {_id: dict([max(v['forces'].items(), key=lambda t: t[1]['N'])]) for _id,
        v in columns.items()}

maxNP = defaultdict(dict)
for _id in piles:
    lc = next(iter(maxN[_id].keys()))
    N = maxN[_id][lc]['N'] * 1e-03
    Rp = piles[_id].get(lc, 0.) * 1e-03
    maxNP[_id][lc] = (N, Rp)
