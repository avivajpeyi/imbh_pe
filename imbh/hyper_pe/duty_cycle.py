#!/usr/bin/env python3
"""
Calculates the % of the data that contains a signal
"""

from __future__ import division

import matplotlib
import pandas as pd
from scipy.special import logsumexp

try:
    import bilby
except ImportError:
    matplotlib.use("PS")
    import bilby

RESULT_FILE_ENDING = "result.json"
LABEL = "DutyCycleTest"
OUTDIR = "./hyper_pe_outdir"
DUTY_CYCLE = "log_xi"
SAMPLER = "dynesty"


class DutyLikelihood(bilby.Likelihood):
    def __init__(self, results_dataframe: pd.DataFrame):
        """
        L(data|xi, signal *or* noise) = L(data|signal)*xi +(1-xi)*L(data|noise)
        where xi --> p(signal)

        https://tinyurl.com/y3vqu3nt

        Parameters
        ----------

        results_dataframe: pandas dataframe
        """
        bilby.Likelihood.__init__(self, parameters={DUTY_CYCLE: None})
        self.log_evidence = results_dataframe.log_evidence.values
        self.log_noise_evidence = results_dataframe.log_noise_evidence.values

    def log_likelihood(self) -> float:
        log_xi = self.parameters[DUTY_CYCLE]
        ln_likelihood = logsumexp(
            self.log_evidence * log_xi
            - self.log_noise_evidence * log_xi
            + self.log_noise_evidence
        )
        return ln_likelihood


def sample_duty_cycle_likelihood(results_dataframe: pd.DataFrame) -> None:
    likelihood_fn = DutyLikelihood(results_dataframe)
    priors = dict(log_xi=bilby.core.prior.Uniform(-50, 0, DUTY_CYCLE))

    result = bilby.run_sampler(
        likelihood=likelihood_fn,
        priors=priors,
        sampler=SAMPLER,
        npoints=500,
        walks=10,
        outdir=OUTDIR,
        label=LABEL,
    )
    result.plot_corner()
