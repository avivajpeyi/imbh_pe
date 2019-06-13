#!/usr/bin/env python3
"""
Calculates the % of the data that contains a signal
"""

from __future__ import division

import os

import bilby
import matplotlib
import pandas as pd
from bilby.core.utils import logger, setup_logger
from hyper_pe import population_inference_keys as keys, prior_file_paths as path
from injection_parameter_generator import injection_keys as ikeys
from scipy import stats

matplotlib.use("Agg")
setup_logger(log_level="info")


FOLDER = "hyper_pe"
SAMPLING_LABEL = "{}MassDistribution"


MASS_KEYS = [ikeys.MASS_RATIO, ikeys.CHIRP_MASS]


def get_mass_prior():
    """
    The PE prior for mass
    """
    pe_prior = bilby.core.prior.PriorDict(path.NORMAL_PE_PRIOR)
    return bilby.core.prior.PriorDict({k: pe_prior[k] for k in MASS_KEYS})


def sample_mass_prior(data):
    sample_prior = get_mass_prior().prob({k: data[k] for k in MASS_KEYS}, axis=0)
    return sample_prior


def get_mass_distribution_prior(hyperprior_type: str):
    if hyperprior_type == "normal":
        return bilby.core.prior.PriorDict(path.NORMAL_HYPERPRIOR)
    else:
        return bilby.core.prior.PriorDict(path.UNIFORM_HYPERPRIOR)


def get_normal_mass_distribution_hyperprior(
    data, q_mu, q_sigma, mchirp_mu, mchirp_sigma
):
    # unpack parameters
    q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]

    # calculate hyperprior
    # hyperprior_q = stats.truncnorm.pdf(
    #     q_sample, loc=q_mu, scale=q_sigma, a=q_min, b=q_max
    # )
    hyperprior_q = stats.norm.pdf(q_sample, loc=q_mu, scale=q_sigma)
    hyperprior_mc = stats.norm.pdf(mc_sample, loc=mchirp_mu, scale=mchirp_sigma)

    hyper_prior = hyperprior_q * hyperprior_mc
    return hyper_prior


def get_uniform_mass_distribution_hyperprior(
    data, q_min, q_max, mchirp_min, mchirp_max
):
    # unpack parameters
    q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]
    # calculate hyperprior
    hyperprior_q = stats.uniform.pdf(q_sample, loc=q_min, scale=q_max - q_min)
    hyperprior_mc = stats.uniform.pdf(
        mc_sample, loc=mchirp_min, scale=mchirp_max - mchirp_min
    )
    hyper_prior = hyperprior_q * hyperprior_mc
    return hyper_prior


def get_mass_distribution_population_likelihood(df, hyperprior_type):

    if hyperprior_type == "normal":
        hyper_prior = get_normal_mass_distribution_hyperprior
    else:
        hyper_prior = get_uniform_mass_distribution_hyperprior

    likelihood = bilby.hyper.likelihood.HyperparameterLikelihood(
        posteriors=[p[MASS_KEYS] for p in df.posterior],
        hyper_prior=hyper_prior,
        sampling_prior=sample_mass_prior,
        log_evidences=df.log_evidence,
    )
    return likelihood


def get_true_values_from_injection_prior():
    injection_prior = bilby.core.prior.PriorDict(path.UNIFORM_INJECTION_PRIOR)
    return {
        keys.Q_MIN: injection_prior[ikeys.MASS_RATIO].minimum,
        keys.Q_MAX: injection_prior[ikeys.MASS_RATIO].maximum,
        keys.MCHIRP_MIN: injection_prior[ikeys.CHIRP_MASS].minimum,
        keys.MCHIRP_MAX: injection_prior[ikeys.CHIRP_MASS].maximum,
    }


def sample_mass_distribution_likelihood(results_dataframe: pd.DataFrame, outdir):
    hyper_prior_types = ["uniform", "normal"]
    for hyper_prior_type in hyper_prior_types:
        likelihood_fn = get_mass_distribution_population_likelihood(
            results_dataframe, hyper_prior_type
        )
        hyper_param_priors = get_mass_distribution_prior(hyper_prior_type)

        label = SAMPLING_LABEL.format(hyper_prior_type)

        for _ in range(10):
            likelihood_fn.parameters.update(hyper_param_priors.sample())
            logger.info(likelihood_fn.log_likelihood())

        result = bilby.run_sampler(
            likelihood=likelihood_fn,
            priors=hyper_param_priors,
            sampler="dynesty",
            npoints=500,
            walks=10,
            outdir=os.path.join(outdir, FOLDER),
            label=label,
        )

        try:
            fig = result.plot_corner(
                truth=get_true_values_from_injection_prior(), save=False
            )

        except Exception as e:
            logger.warn(
                f"Trouble plotting Population hyperpe corner truths {e}. Plotting without truths."
            )
            fig = result.plot_corner(save=False)
        fig.suptitle(f"Log Evidence = {result.log_evidence}")
        filename = "{}/{}/{}_corner.png".format(outdir, FOLDER, label)
        fig.savefig(filename, dpi=300)
