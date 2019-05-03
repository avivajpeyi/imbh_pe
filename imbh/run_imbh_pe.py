#!/usr/bin/env python3
"""
Usage:
python run_imbh_pe.py [--injection_file INJECTION_FILE] [--idx IDX]
                      [--prior_file PRIOR_FILE] [--out_dir OUT_DIR]

Runs PE on injected signal specified by parameters at row IDX of dataframe in INJECTION_FILE.
"""
import sys

from imbh_pe_calculator.imbh_pe_runner import parse_args, run_pe_on_injection
from injection_parameter_generator.imbh_parameter_generator import (
    load_injection_param_dataframe_from_h5,
)


def main():
    args = parse_args(sys.argv[1:])
    injection_param_dataframe = load_injection_param_dataframe_from_h5(
        args.injection_file, args.idx
    )
    run_pe_on_injection(
        injection_parameters_dict=injection_param_dataframe.to_dict(),
        injection_id_num=args.idx,
        prior_file=args.prior_file,
        out_dir=args.out_dir,
    )


if __name__ == "__main__":
    main()
