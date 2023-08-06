import re
import csv
import pickle
from collections import defaultdict


def main():
    filename = 'exploded-combinations.csv'

    exploded_lcs = defaultdict(list)
    nskip = 2
    with open(filename) as f:
        reader = csv.reader(f, delimiter=';')
        i = 0
        for row in reader:
            if i < nskip:
                i += 1
                continue
            name = row[0].strip()
            combination = (row[3].replace(' ', '')
                                 .replace('-staticload', '')
                                 .replace('-Buoyancy', ''))
            factor = row[4].replace(',', '.')
            if name:
                key = name
            exploded_lcs[key].append((factor, combination))

    # Filter duplicates
    import re
    regex = re.compile('(\d+)?\.\d')
    duplicates = list(filter(lambda k: regex.search(k), exploded_lcs))
    for key in duplicates:
      del exploded_lcs[key]

    # Map backward
    combinations_to_exploded = dict()
    for name, components in exploded_lcs.items():
        key = '+'.join([f'{lc}*{f}' for f, lc in components])
        combinations_to_exploded[key] = name

    # Map combination keys
    combination_keys = dict()
    filename = 'combination-keys.csv'
    nskip = 1
    with open(filename) as f:
        reader = csv.reader(f, delimiter=';')
        i = 0
        for row in reader:
            if i < nskip:
                i += 1
                continue
            combination_keys[row[0]] = (row[1].replace(' ', '')
                                              .replace(',', '.'))

    key_to_exploded = {
        k: combinations_to_exploded[v] for k, v in combination_keys.items()
        }

    with open('key_to_exploded.pkl', 'wb') as f:
        pickle.dump(key_to_exploded, f)

    return key_to_exploded, combination_keys, combinations_to_exploded, exploded_lcs


key_regex = re.compile('.+/(?P<key>\d+)$')


def parse_combination_key(key):
    return key_regex.search(key).group('key')


if __name__ == '__main__':
    key_to_exploded, k2c, c2e, e2c = main()
