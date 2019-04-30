#!/usr/bin/env python3
"""
Usage:
python run_imbh_pe.py [--injection_file INJECTION_FILE] [--idx IDX]
                      [--prior_file PRIOR_FILE] [--out_dir OUT_DIR]

Runs PE on injected signal specified by parameters at row IDX of dataframe in INJECTION_FILE.
"""
import argparse

import deepdish
import imbh.injection_parameter_generator.injection_keys as keys
from imbh.imbh_pe_calculator.imbh_pe_runner import run_pe_on_injection


def main():
    parser = argparse.ArgumentParser(description="imbh signal pe runner")
    required = parser.add_argument_group("required named arguments")
    required.add_argument(
        "--injection_file", "-f", type=str, help="h5 file of a dataframe of injections"
    )
    required.add_argument(
        "--idx", "-i", type=int, help="index number of injection from injection file"
    )
    required.add_argument(
        "--prior_file",
        "-p",
        type=str,
        help="prior file for what is known about IMBH signals",
    )
    required.add_argument(
        "--out_dir", "-o", type=str, help="the out dir for the PE results"
    )
    args = parser.parse_args()

    # verifying correct file types
    if not args.injection_file.endswith(".h5"):
        raise IncorrectFileType(
            f"Injection file does not end with '.h5': {args.injection_file}"
        )

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            f"Prior file does not end with '.prior': {args.prior_file}"
        )

    # unpacking injection parameters and priors
    injection_dict = dict(deepdish.io.load(args.injection_file))
    injection_param_dataframe = injection_dict.get(keys.INJECTION).loc[args.idx]

    run_pe_on_injection(
        injection_parameters_dict=injection_param_dataframe.to_dict(),
        injection_id_num=args.idx,
        prior_file=args.prior_file,
        out_dir=args.out_dir,
    )


class IncorrectFileType(Exception):
    pass


if __name__ == "__main__":
    main()
