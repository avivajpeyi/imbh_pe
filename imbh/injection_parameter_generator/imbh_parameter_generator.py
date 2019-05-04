#!/usr/bin/env python3
"""
Generates an h5 containing the dataframe of injection parameters
"""
import argparse
import os
from typing import Optional

import deepdish
import injection_parameter_generator.injection_keys as keys
import pandas as pd
from tools.file_utils import IncorrectFileType
from tools.plotting import plot_mass_distribution

INJECTION_DATA_FNAME = "injection_data.h5"
INJECTION_NUMBER = "InjNum"


def generate_injection_paramter_h5(
    number_of_injections: int, prior_file: str, out_dir: Optional[str] = ""
):
    import bilby as bb

    new_priors = bb.gw.prior.BBHPriorDict(prior_file)
    priors = bb.gw.prior.BBHPriorDict()
    priors.update(new_priors)
    d = pd.DataFrame(priors.sample(number_of_injections))
    d[INJECTION_NUMBER] = range(0, len(d))
    d.to_hdf(os.path.join(out_dir, INJECTION_DATA_FNAME), key=keys.INJECTION)

    # plot masses
    plot_mass_distribution(mass1=d[keys.MASS_1], mass2=d[keys.MASS_2], out_dir=out_dir)


def load_injection_param_dataframe_from_h5(
    injection_file: str, id_number: Optional[int] = None
):
    injection_dict = dict(deepdish.io.load(injection_file))
    injection_param_dataframe = injection_dict.get(keys.INJECTION)
    if id_number:
        return injection_param_dataframe.loc[id_number]
    return injection_param_dataframe


def parse_args(args):
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
    args = parser.parse_args(args)

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            "Prior file does not end with '.prior': {}".format(args.prior_file)
        )

    return args
