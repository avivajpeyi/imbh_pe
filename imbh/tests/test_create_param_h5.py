import unittest

from injection_parameter_generator.imbh_parameter_generator import (
    generate_injection_paramter_h5,
    parse_args,
)


class TestCreateParam(unittest.TestCase):
    def test_create_param(self):
        args = parse_args(
            [
                "--number_of_injections",
                "200",
                "--prior_file",
                "injection_parameter_generator/imbh_injection_generation.prior",
                "--out_dir",
                "tests/temp/",
            ]
        )
        generate_injection_paramter_h5(
            number_of_injections=args.number_of_injections,
            prior_file=args.prior_file,
            out_dir=args.out_dir,
        )
