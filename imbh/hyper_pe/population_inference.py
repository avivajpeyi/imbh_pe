#!/usr/bin/env python3
"""
Calculates the % of the data that contains a signal
"""

from __future__ import division

import os

import bilby
import injection_parameter_generator.injection_keys as ikeys
import matplotlib
import pandas as pd
from pe_result.plotting.latex_label import LATEX_LABEL_DICT
from scipy.stats import norm

"""
TRUE PRIOR

chirp_mass = Gaussian(name='chirp_mass', latex_label='$\\mathcal{M}$', mu=40.0, sigma=10.0, unit='$M_{\\odot}$')
mass_ratio = Gaussian(name='mass_ratio', latex_label='$q$', mu=0.15, sigma=0.05, unit='$M_{\\odot}$')
"""

matplotlib.use("Agg")
bilby.utils.setup_logger(log_level="info")


MC_MU_TRUE = 40
MC_SIGMA_TRUE = 10


Q_MU_TRUE = 0.15
Q_SIGMA_TRUE = 0.05


# keys
Q_MU = "q_mu"
Q_SIGMA = "q_sigma"
MC_MU = "mc_mu"
MC_SIGMA = "mc_sigma"
# Latex labels
latex_Q_MU = "$q_{\\mu}$"
latex_Q_SIGMA = "$q_{\\sigma}$"
latex_MC_MU = "$mc_{\\mu}$"
latex_MC_SIGMA = "$mc_{\\sigma}$"

FOLDER = "hyper_pe"
SAMPLING_LABEL = "QMC"


def get_qmc_prior():

    signal_pe_prior = bilby.core.prior.PriorDict(
        {
            ikeys.MASS_RATIO: bilby.core.prior.Uniform(
                minimum=1.8,
                maximum=5,
                name=ikeys.MASS_RATIO,
                latex_label=LATEX_LABEL_DICT[ikeys.MASS_RATIO],
            ),
            ikeys.CHIRP_MASS: bilby.core.prior.Uniform(
                minimum=18,
                maximum=58,
                name=ikeys.CHIRP_MASS,
                latex_label=LATEX_LABEL_DICT[ikeys.CHIRP_MASS],
            ),
        }
    )
    return signal_pe_prior


def get_qmc_population_prior(num_sigma=3):
    q_nsigma = num_sigma * Q_SIGMA_TRUE
    mc_nsigma = num_sigma * MC_SIGMA_TRUE
    priors = bilby.core.prior.PriorDict(
        {
            Q_MU: bilby.core.prior.Uniform(
                minimum=Q_MU_TRUE - q_nsigma,
                maximum=Q_MU_TRUE + q_nsigma,
                name=Q_MU,
                latex_label=latex_Q_MU,
            ),
            Q_SIGMA: bilby.core.prior.Uniform(
                minimum=0,
                maximum=Q_SIGMA_TRUE + q_nsigma,
                name=Q_SIGMA,
                latex_label=latex_Q_SIGMA,
            ),
            MC_MU: bilby.core.prior.Uniform(
                minimum=MC_MU_TRUE - mc_nsigma,
                maximum=MC_MU_TRUE + mc_nsigma,
                name=MC_MU,
                latex_label=latex_MC_MU,
            ),
            MC_SIGMA: bilby.core.prior.Uniform(
                minimum=0,
                maximum=MC_SIGMA_TRUE + mc_nsigma,
                name=MC_SIGMA,
                latex_label=latex_MC_SIGMA,
            ),
        }
    )
    return priors


def get_qmc_hyperprior(data, q_mu, q_sigma, mc_mu, mc_sigma):
    q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]
    hyperprior_q = norm.pdf(q_sample, q_mu, q_sigma)
    hyperprior_mc = norm.pdf(mc_sample, mc_mu, mc_sigma)
    hyper_prior = hyperprior_q * hyperprior_mc
    return hyper_prior


def get_qmc_sample_prior(data):
    q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]
    sample_prior = get_qmc_prior().prob(
        {ikeys.MASS_RATIO: q_sample, ikeys.CHIRP_MASS: mc_sample}, axis=0
    )
    return sample_prior


def get_qmc_population_likelihood(df):
    likelihood = bilby.hyper.likelihood.HyperparameterLikelihood(
        posteriors=[p[[ikeys.MASS_RATIO, ikeys.CHIRP_MASS]] for p in df.posterior],
        hyper_prior=get_qmc_hyperprior,
        sampling_prior=get_qmc_sample_prior,
        log_evidences=df.log_evidence,
    )
    return likelihood


def sample_qmc_likelihood(results_dataframe: pd.DataFrame, outdir):
    likelihood_fn = get_qmc_population_likelihood(results_dataframe)
    hyper_param_priors = get_qmc_population_prior()

    result = bilby.run_sampler(
        likelihood=likelihood_fn,
        priors=hyper_param_priors,
        sampler="dynesty",
        npoints=500,
        walks=10,
        outdir=os.path.join(outdir, FOLDER),
        label=SAMPLING_LABEL,
    )
    result.plot_corner(
        truth={
            {
                Q_MU: Q_MU_TRUE,
                Q_SIGMA: Q_SIGMA_TRUE,
                MC_MU: MC_MU_TRUE,
                MC_SIGMA: MC_SIGMA_TRUE,
            }
        }
    )
