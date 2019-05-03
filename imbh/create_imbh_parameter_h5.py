#!/usr/bin/env python3
"""
Usage:
python create_imbh_parameter_h5.py [-n --number_of_injections NUMBER_OF_INJECTIONS]
                                   [-p --prior_file PRIOR_FILE]


Creates NUM_INJECTIONS injection parameters (by sampling priors) and stores parameters in h5 file
PRIOR_FPATH must have .prior extension
"""

import sys

from injection_parameter_generator.imbh_parameter_generator import (
    generate_injection_paramter_h5,
    parse_args,
)


def main():
    args = parse_args(sys.argv[1:])
    generate_injection_paramter_h5(
        number_of_injections=args.number_of_injections,
        prior_file=args.prior_file,
        out_dir=args.out_dir,
    )


if __name__ == "__main__":
    main()
