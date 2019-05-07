#!/usr/bin/env python3
"""

Trying to find the % of the data that contains a signal

let p(signal) = xi

L(data|xi, signal *or* noise) = L(data|signal)*xi +(1-xi)*L(data|noise)

https://lscsoft.docs.ligo.org/bilby/hyperparameters.html#understanding-the-population-using-hyperparameters


L(d| x, H_sig, H_pop) =
Prod_i^N  (( Like(d_i | H_sig)  /  n_i  ) * (Sum_k^n_i    prior() )  )

https://tinyurl.com/y3vqu3nt

"""

from __future__ import division

import matplotlib
from scipy.special import logsumexp

try:
    import bilby
except ImportError:
    matplotlib.use("PS")
    import bilby

RESULT_FILE_ENDING = "result.json"

# A few simple setup steps
label = "DutyCycleTest"
outdir = "./hyper_pe_outdir"


DUTY_CYCLE = "log_xi"


class DutyLikelihood(bilby.Likelihood):
    def __init__(self, results_dataframe):
        """

        where xi --> p(signal)

        L(data|xi, signal *or* noise) = L(data|signal)*xi +(1-xi)*L(data|noise)

        Parameters
        ----------
        """
        bilby.Likelihood.__init__(self, parameters={DUTY_CYCLE: None})
        self.log_evidence = results_dataframe.log_evidence.values
        self.log_noise_evidence = results_dataframe.log_noise_evidence.values

    def log_likelihood(self):
        log_xi = self.parameters[DUTY_CYCLE]
        ln_likelihood = logsumexp(
            self.log_evidence * log_xi
            - self.log_noise_evidence * log_xi
            + self.log_noise_evidence
        )
        return ln_likelihood


def sample_duty_cycle_likelihood(results_dataframe):
    likelihood_fn = DutyLikelihood(results_dataframe)
    priors = dict(log_xi=bilby.core.prior.Uniform(-50, 0, DUTY_CYCLE))

    # And run sampler
    result = bilby.run_sampler(
        likelihood=likelihood_fn,
        priors=priors,
        sampler="dynesty",
        npoints=500,
        walks=10,
        outdir=outdir,
        label=label,
    )
    result.plot_corner()
