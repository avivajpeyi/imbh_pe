#!/usr/bin/env python3
"""
Usage:
python create_dag.py [--jobs NUM_JOBS] [--fname FNAME]

Creates dag file of name FNAME with NUM_JOBS jos
initialises the variable $injectionNumber to the job's number.
FNAME must have .dag extension
"""
import argparse

from imbh.dag_creation.make_dag import create_dag_file


def main():
    parser = argparse.ArgumentParser(description="dag file creator")
    required = parser.add_argument_group("required named arguments")
    required.add_argument(
        "--jobs", "-j", default=200, type=int, help="number of jobs to be created"
    )
    required.add_argument("--dag_fname", "-d", type=str, help="dag output filename")
    required.add_argument("--sub_fname", "-s", type=str, help="subfile to run job")

    args = parser.parse_args()

    if not args.dag_fname.endswith(".dag"):
        raise IncorrectFileType(
            "Dag file doenst end with '.dag': {}".format(args.dag_fname)
        )

    if not args.sub_fname.endswith(".sub"):
        raise IncorrectFileType(
            "Sub file doenst end with '.sub': {}".format(args.sub_fname)
        )

    create_dag_file(
        number_of_jobs=args.jobs,
        sub_filename=args.sub_fname,
        dag_filename=args.dag_fname,
    )


class IncorrectFileType(Exception):
    pass


if __name__ == "__main__":
    main()
