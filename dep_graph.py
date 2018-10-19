#!/usr/bin/env python

import os
import argparse
import json
from pathlib import Path

from graphviz import Digraph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Draw dependency graph for conda environment.'
    )
    parser.add_argument('-e', '--env', metavar='eigen', type=str,
                        help='a conda environment')
    parser.add_argument('-x', '--exclude', metavar='python', type=str, nargs='+',
                        help='a package to exclude')
    parser.add_argument('-i', '--include', metavar='numpy', type=str, nargs='+',
                        help='only consider these packages')
    parser.add_argument('-o', '--output', metavar='env-graph', type=str,
                        help='output filename')
    parser.add_argument('-t', '--format', default='svg', metavar='svg', type=str,
                        help='output format')

    args = parser.parse_args()

    default_conda_dir = Path(os.environ.get('HOME')) / 'miniconda3'
    meta_path = default_conda_dir / 'envs' / args.env / 'conda-meta'

    filename = args.output or f'{args.env}-dependency-graph'
    dg = Digraph(filename=filename, format=args.format)

    for f in meta_path.glob('*.json'):
        with f.open() as fh:
            d = json.load(fh)
        package_name = d.get('name')
        dg.node(package_name)
        for dep in d.get('depends', []):
            dependency_name = dep.split()[0]
            if args.include:
                if dependency_name not in args.include:
                    continue
            if args.exclude and dependency_name in args.exclude:
                print(f'exclude {dependency_name} for {package_name}')
                continue
            dg.edge(package_name, dependency_name)
    dg.render()
