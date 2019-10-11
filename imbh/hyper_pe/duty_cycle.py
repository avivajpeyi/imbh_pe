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
GLITCH_L1_DUTY_CYCLE_LATEX = "${\\xi}_{G_{L1}}$"
GLITCH_H1_DUTY_CYCLE_LATEX = "${\\xi}_{G_{H1}}$"
DUTY_CYCLE = "xi"
GLITCH_L1_DUTY_CYCLE = "xi_gl"
GLITCH_H1_DUTY_CYCLE = "xi_gh"
SAMPLER = "dynesty"
FOLDER = "hyper_pe"


class DutyLikelihood(bilby.Likelihood):
    def __init__(self, evidence_dataframe: pd.DataFrame):
        """
        L(data|xi, signal *or* noise) = L(data|signal)*xi +(1-xi)*L(data|noise)
        where xi --> p(signal)

        Parameters
        ----------

        evidence_dataframe: pandas dataframe
        """
        bilby.Likelihood.__init__(
            self,
            parameters={
                DUTY_CYCLE: None,
                GLITCH_H1_DUTY_CYCLE: None,
                GLITCH_L1_DUTY_CYCLE: None,
            },
        )
        nan_present = evidence_dataframe.isnull().values.any()
        assert not nan_present, "NaN present in the evidence dataframe!"
        self.log_evidence = evidence_dataframe[rkeys.LOG_EVIDENCE].values
        self.log_noise_evidence = evidence_dataframe[rkeys.LOG_NOISE_EVIDENCE].values
        self.log_glitch_H_evidence = evidence_dataframe[
            rkeys.LOG_GLITCH_H_EVIDENCE
        ].values
        self.log_glitch_L_evidence = evidence_dataframe[
            rkeys.LOG_GLITCH_L_EVIDENCE
        ].values

    def log_likelihood(self) -> float:
        """
        L(xi, xi_gH, xi_gL) =
            Zs    xi      (1-xi_gH)  (1-xi_gL)  +
            Zn    (1-xi)  (1-xi_gH)  (1-xi_gL)  +
            ZgH   (1-xi)  xi_gH      (1-xi_gL)  +
            ZgL   (1-xi)  (1-xi_gH)  xi_gL
        """

        zs = self.log_evidence
        zn = self.log_noise_evidence
        zg_h = self.log_glitch_H_evidence
        zg_l = self.log_glitch_L_evidence

        xi = self.parameters[DUTY_CYCLE]
        xi_gh = self.parameters[GLITCH_H1_DUTY_CYCLE]
        xi_gl = self.parameters[GLITCH_L1_DUTY_CYCLE]

        log_xi = np.log(xi)
        log_xi_gh = np.log(xi_gh)
        log_xi_gl = np.log(xi_gl)

        log_1_minus_xi = np.log(1.0 - xi)
        log_1_minus_xi_gh = np.log(1.0 - xi_gh)
        log_1_minus_xi_gl = np.log(1.0 - xi_gl)

        ln_likelihood_di = logsumexp(
            a=[
                zs + log_xi + log_1_minus_xi_gh + log_1_minus_xi_gl,
                zn + log_1_minus_xi + log_1_minus_xi_gh + log_1_minus_xi_gl,
                zg_h + log_1_minus_xi + log_xi_gh + log_1_minus_xi_gl,
                zg_l + log_1_minus_xi + log_1_minus_xi_gh + log_xi_gl,
            ],
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
        results_dataframe[
            [
                rkeys.LOG_EVIDENCE,
                rkeys.LOG_NOISE_EVIDENCE,
                rkeys.LOG_GLITCH_H_EVIDENCE,
                rkeys.LOG_GLITCH_L_EVIDENCE,
            ]
        ]
    )
    priors = {
        DUTY_CYCLE: bilby.core.prior.Uniform(
            minimum=0.001, maximum=1, name=DUTY_CYCLE, latex_label=DUTY_CYCLE_LATEX
        ),
        GLITCH_H1_DUTY_CYCLE: bilby.core.prior.Uniform(
            minimum=0.001,
            maximum=1,
            name=GLITCH_H1_DUTY_CYCLE,
            latex_label=GLITCH_H1_DUTY_CYCLE_LATEX,
        ),
        GLITCH_L1_DUTY_CYCLE: bilby.core.prior.Uniform(
            minimum=0.001,
            maximum=1,
            name=GLITCH_L1_DUTY_CYCLE,
            latex_label=GLITCH_L1_DUTY_CYCLE_LATEX,
        ),
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
