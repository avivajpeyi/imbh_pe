#!/usr/bin/env python3
"""
Generates an h5 containing the dataframe of injection parameters
"""
import os
from typing import Optional

import imbh.injection_parameter_generator.injection_keys as keys
import matplotlib
import pandas as pd

matplotlib.use("PS")


def generate_injection_paramter_h5(
    number_of_injections: int, prior_file: str, out_dir: Optional[str] = ""
):
    import bilby as bb
    import matplotlib.pyplot as plt

    new_priors = bb.gw.prior.BBHPriorDict(prior_file)
    priors = bb.gw.prior.BBHPriorDict()
    priors.update(new_priors)
    d = pd.DataFrame(priors.sample(number_of_injections))
    d.to_hdf(os.path.join(out_dir, "injection_data.h5"), key=keys.INJECTION)

    # plot masses
    plt.hist2d(d["mass_1"], d["mass_2"], bins=100, cmap="Blues")
    plt.xlabel("$m_1$")
    plt.ylabel("$m_2$")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "m1_m2.png"))
