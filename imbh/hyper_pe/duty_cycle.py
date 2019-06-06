#!/usr/bin/env python3
"""
Calculates the % of the data that contains a signal
"""

from __future__ import division

import os

import bilby
import imbh_pe_calculator.results_keys as rkeys
import matplotlib
import numpy as np
import pandas as pd
from scipy.special import logsumexp

matplotlib.use("Agg")
bilby.utils.setup_logger(log_level="info")


LABEL = "DutyCycle"
DUTY_CYCLE_LATEX = "${\\xi}$"
DUTY_CYCLE = "xi"
SAMPLER = "dynesty"
FOLDER = "hyper_pe"


class DutyLikelihood(bilby.Likelihood):
    def __init__(self, evidence_dataframe: pd.DataFrame):
        """
        L(data|xi, signal *or* noise) = L(data|signal)*xi +(1-xi)*L(data|noise)
        where xi --> p(signal)

        https://tinyurl.com/y3vqu3nt

        Parameters
        ----------

        evidence_dataframe: pandas dataframe
        """
        bilby.Likelihood.__init__(self, parameters={DUTY_CYCLE: None})
        nan_present = evidence_dataframe.isnull().values.any()
        assert not nan_present, "NaN present in the evidence dataframe!"
        self.log_evidence = evidence_dataframe[rkeys.LOG_EVIDENCE].values
        self.log_noise_evidence = evidence_dataframe[rkeys.LOG_NOISE_EVIDENCE].values

    def log_likelihood(self) -> float:
        """
        The L = Z*xi + Zn*(1-xi)
        """
        log_xi = np.log(self.parameters[DUTY_CYCLE])
        log_1_minus_xi = np.log(1.0 - self.parameters[DUTY_CYCLE])
        ln_likelihood_di = logsumexp(
            a=[self.log_evidence + log_xi, self.log_noise_evidence + log_1_minus_xi],
            axis=0,
        )
        assert len(ln_likelihood_di) == len(
            self.log_evidence
        ), "len(d) {}, len(LnL(di)) {}".format(
            len(self.log_evidence), len(ln_likelihood_di)
        )
        ln_likelihood = np.sum(ln_likelihood_di)
        return ln_likelihood


def sample_duty_cycle_likelihood(results_dataframe: pd.DataFrame, outdir: str) -> None:
    likelihood_fn = DutyLikelihood(
        results_dataframe[[rkeys.LOG_EVIDENCE, rkeys.LOG_NOISE_EVIDENCE]]
    )
    priors = {
        DUTY_CYCLE: bilby.core.prior.Uniform(
            minimum=0.001, maximum=1, name=DUTY_CYCLE, latex_label=DUTY_CYCLE_LATEX
        )
    }

    result = bilby.run_sampler(
        likelihood=likelihood_fn,
        priors=priors,
        sampler=SAMPLER,
        npoints=500,
        walks=10,
        outdir=os.path.join(outdir, FOLDER),
        label=LABEL,
    )
    result.plot_corner()
