#!/usr/bin/env python
# Copyright (C) 2019 demetriou engineering ltd.
# Part of `dx-punch`, licensed under the AGPLv3+
import logging
import argparse

import sys, json, pprint

from dx_punch.EC2 import Slab


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--figurename', help="Provide a filename to save the output plot",
        default=None
        )
    return parser.parse_args()


def get_exception_code(e, default_code='0000'):
    """Check if exception ``e`` has a ``code`` attribute
    and return that code, or a default one otherwise.

    :param Exception e:
    :param str default_code:
    :rtype: str
    """
    try:
        code = e.code
    except AttributeError:
        code = default_code
    return code


def main():
    logging.info("Starting dx-punch calculation...")
    args = parse_args()
    json_str = ""

    for line in sys.stdin:
        json_str += line

    logging.debug(f"Processing JSON: {json_str}")
    datadict = json.loads(json_str)
    try:
        slab = Slab.from_json(datadict)
    except Exception as e:
        code = get_exception_code(e)
        print(json.dumps({f'Error {code}': str(e)}))
        raise

    try:
        print(slab.to_json())
    except Exception as e:
        code = get_exception_code(e)
        print(json.dumps({f'Error {code}': str(e)}))
        raise

    if args.figurename:
        logging.info(f"Saving plot to {args.figurename}")
        fig, ax = slab.postprocessor.plot_u1()
        fig.savefig(args.figurename, dpi=600)

if __name__ == "__main__":
    logging.basicConfig(filename='/tmp/dx-punch.log', level=logging.DEBUG)
    try:
        main()
    except Exception as e:
        code = get_exception_code(e)
        logging.info(f'Error {code}: {e}')
        raise
    else:
        logging.info('Calculation finished successfully.')
