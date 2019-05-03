#!/usr/bin/env python3
"""
Usage:
python create_dag.py [--jobs NUM_JOBS] [--fname FNAME]

Creates dag file of name FNAME with NUM_JOBS jos
initialises the variable $injectionNumber to the job's number.
FNAME must have .dag extension
"""

import sys

from dag_creation.make_dag import create_dag_file, parse_args


def main():
    args = parse_args(sys.argv[1:])
    create_dag_file(
        number_of_jobs=args.jobs,
        sub_filename=args.sub_fname,
        dag_filename=args.dag_fname,
    )


if __name__ == "__main__":
    main()
