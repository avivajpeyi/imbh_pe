#!/usr/bin/env python3
"""
Generates an h5 containing the dataframe of injection parameters
"""
import imbh.injection_parameter_generator.injection_keys as keys
import matplotlib
import pandas as pd

matplotlib.use("PS")


def generate_injection_paramter_h5(number_of_injections: int, prior_file: str):
    import bilby as bb

    priors = bb.gw.prior.BBHPriorDict(prior_file)
    d = pd.DataFrame(priors.sample(number_of_injections))
    d.to_hdf("injection_data.h5", key=keys.INJECTION)
