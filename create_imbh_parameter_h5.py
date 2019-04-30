#!/usr/bin/env python3
"""
Usage:
python create_imbh_parameter_h5.py [-n --number_of_injections NUMBER_OF_INJECTIONS]
                                   [-p --prior_file PRIOR_FILE]


Creates NUM_INJECTIONS injection parameters (by sampling priors) and stores parameters in h5 file
PRIOR_FPATH must have .prior extension
"""
import argparse

from imbh.injection_parameter_generator.imbh_parameter_generator import (
    generate_injection_paramter_h5,
)


def main():
    parser = argparse.ArgumentParser(description="imbh injection parameter generator")
    required = parser.add_argument_group("required named arguments")
    parser.add_argument(
        "--number_of_injections",
        "-n",
        default=200,
        type=int,
        help="number of injection parameters",
    )
    required.add_argument(
        "--prior_file", "-p", type=str, help="prior file used to create the parameters"
    )
    parser.add_argument(
        "--out_dir",
        "-o",
        default="",
        type=str,
        help="out dir where data and image stored",
    )
    args = parser.parse_args()

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            "Prior file does not end with '.prior': {}".format(args.prior_file)
        )

    generate_injection_paramter_h5(
        args.number_of_injections, args.prior_file, args.out_dir
    )


class IncorrectFileType(Exception):
    pass


if __name__ == "__main__":
    main()
