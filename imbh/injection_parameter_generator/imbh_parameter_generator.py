#!/usr/bin/env python3
"""
Generates an h5 containing the dataframe of injection parameters
"""
import argparse

import bibly as bb
import imbh.injection_parameter_generator.injection_keys as keys
import pandas as pd


def generate_injection_paramter_h5(number_of_injections: int, prior_file: str):
    priors = bb.gw.prior.BBHPriorDict(prior_file)
    d = pd.DataFrame(priors.sample(number_of_injections))
    d.to_hdf("injection_data.h5", key=keys.INJECTION)


def main():
    parser = argparse.ArgumentParser(description="imbh injection parameter generator")
    parser.add_argument(
        "--number_of_injections",
        "-n",
        default=200,
        type=int,
        help="number of injection parameters",
    )
    parser.add_argument(
        "--prior_file", "-p", type=str, help="prior file used to create the parameters"
    )
    args = parser.parse_args()

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            f"Prior file does not end with '.prior': {args.prior_file}"
        )

    generate_injection_paramter_h5(argparse.number_of_injections, argparse.prior_file)


class IncorrectFileType(Exception):
    pass
