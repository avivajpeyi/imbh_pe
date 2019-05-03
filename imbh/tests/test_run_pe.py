#!/usr/bin/env python3
import unittest

from imbh_pe_calculator.imbh_pe_runner import parse_args, run_pe_on_injection
from injection_parameter_generator.imbh_parameter_generator import (
    load_injection_param_dataframe_from_h5,
)


class TestCreateParam(unittest.TestCase):
    def test_create_param(self):
        args = parse_args(
            [
                "-f",
                "injection_parameter_generator/injection_data.h5",
                "-i",
                "1",
                "-p",
                "imbh_pe_calculator/imbh_pe.prior",
                "-o",
                "tests/pe_test",
            ]
        )
        injection_param_dataframe = load_injection_param_dataframe_from_h5(
            args.injection_file, args.idx
        )
        run_pe_on_injection(
            injection_parameters_dict=injection_param_dataframe.to_dict(),
            injection_id_num=args.idx,
            prior_file=args.prior_file,
            out_dir=args.out_dir,
        )
