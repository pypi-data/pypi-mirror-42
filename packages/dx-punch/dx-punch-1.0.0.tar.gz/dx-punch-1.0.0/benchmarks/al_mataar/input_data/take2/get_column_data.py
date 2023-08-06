import re
import csv
import pickle
from collections import defaultdict

filename = 'internal-forces.csv'

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

piles = {}
# filename = 'pile-reactions.csv'
# with open(filename) as f:
#     reader = csv.reader(f, delimiter=';')
#     for row in reader:
#         piles[row[0]] = {
#             'Rx': float(row[2])*1e+03
#             }
# 
# for c in piles:
#     for LC in columns[c]:
#         columns[c][LC]['N'] -= piles[c]['Rx']

eligible = defaultdict(dict)
for label in columns:
    for LC in columns[label]:
        if columns[label][LC]['N'] > 0.:
            eligible[label][LC] = columns[label][LC]

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
