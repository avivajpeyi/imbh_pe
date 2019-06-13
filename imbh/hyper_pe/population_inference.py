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


# #!/usr/bin/env python3
# """
# Calculates the % of the data that contains a signal
# """
#
#
# import os
#
# import bilby
# import injection_parameter_generator.injection_keys as ikeys
# import matplotlib
# import pandas as pd
# from bilby.core.utils import logger, setup_logger
# from pe_result.plotting.latex_label import LATEX_LABEL_DICT
# from scipy.stats import norm
#
# """
# TRUE PRIOR
# chirp_mass = Gaussian(name='chirp_mass', latex_label='$\\mathcal{M}$', mu=40.0, sigma=10.0, unit='$M_{\\odot}$')
# mass_ratio = Gaussian(name='mass_ratio', latex_label='$q$', mu=0.15, sigma=0.05, unit='$M_{\\odot}$')
# """
#
# matplotlib.use("Agg")
# setup_logger(log_level="info")
#
#
# MC_MU_TRUE = 40
# MC_SIGMA_TRUE = 10
#
#
# Q_MU_TRUE = 0.15
# Q_SIGMA_TRUE = 0.05
#
#
# # keys
# Q_MU = "q_mu"
# Q_SIGMA = "q_sigma"
# MC_MU = "mc_mu"
# MC_SIGMA = "mc_sigma"
# # Latex labels
# latex_Q_MU = "$q_{\\mu}$"
# latex_Q_SIGMA = "$q_{\\sigma}$"
# latex_MC_MU = "$mc_{\\mu}$"
# latex_MC_SIGMA = "$mc_{\\sigma}$"
#
# FOLDER = "hyper_pe"
# #SAMPLING_LABEL = "QMC"
#
#
#
#
# def get_qmc_prior():
#     """
#     chirp_mass = Uniform(name='chirp_mass', latex_label='$\\mathcal{M}$', minimum=18.0, maximum=58.0, unit='$M_{\\odot}$')
#     mass_ratio = Uniform(name='mass_ratio', latex_label='$q$', minimum=0.1, maximum=0.5)
#     """
#
#     mc_min, mc_max = 18, 58
#     q_min, q_max = 0.1, 0.5
#
#     signal_pe_prior = bilby.core.prior.PriorDict(
#         {
#             ikeys.CHIRP_MASS: bilby.core.prior.Uniform(
#                 minimum=mc_min,
#                 maximum=mc_max,
#                 name=ikeys.CHIRP_MASS,
#                 latex_label=LATEX_LABEL_DICT[ikeys.CHIRP_MASS],
#             ),
#             ikeys.MASS_RATIO: bilby.core.prior.Uniform(
#                 minimum=q_min,
#                 maximum=q_max,
#                 name=ikeys.MASS_RATIO,
#                 latex_label=LATEX_LABEL_DICT[ikeys.MASS_RATIO],
#             ),
#         }
#     )
#     return signal_pe_prior
#
#
# def get_qmc_population_prior(num_sigma=3):
#     q_nsigma = num_sigma * Q_SIGMA_TRUE
#     mc_nsigma = num_sigma * MC_SIGMA_TRUE
#     priors = bilby.core.prior.PriorDict(
#         {
#             Q_MU: bilby.core.prior.Uniform(
#                 minimum=Q_MU_TRUE - q_nsigma,
#                 maximum=Q_MU_TRUE + q_nsigma,
#                 name=Q_MU,
#                 latex_label=latex_Q_MU,
#             ),
#             Q_SIGMA: bilby.core.prior.Uniform(
#                 minimum=0,
#                 maximum=Q_SIGMA_TRUE + q_nsigma,
#                 name=Q_SIGMA,
#                 latex_label=latex_Q_SIGMA,
#             ),
#             MC_MU: bilby.core.prior.Uniform(
#                 minimum=MC_MU_TRUE - mc_nsigma,
#                 maximum=MC_MU_TRUE + mc_nsigma,
#                 name=MC_MU,
#                 latex_label=latex_MC_MU,
#             ),
#             MC_SIGMA: bilby.core.prior.Uniform(
#                 minimum=0,
#                 maximum=MC_SIGMA_TRUE + mc_nsigma,
#                 name=MC_SIGMA,
#                 latex_label=latex_MC_SIGMA,
#             ),
#         }
#     )
#     return priors
#
#
# def get_qmc_hyperprior(data, q_mu, q_sigma, mc_mu, mc_sigma):
#     q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]
#     hyperprior_q = norm.pdf(q_sample, q_mu, q_sigma)
#     hyperprior_mc = norm.pdf(mc_sample, mc_mu, mc_sigma)
#     hyper_prior = hyperprior_q * hyperprior_mc
#     return hyper_prior
#
#
# def get_qmc_sample_prior(data):
#     q_sample, mc_sample = data[ikeys.MASS_RATIO], data[ikeys.CHIRP_MASS]
#     sample_prior = get_qmc_prior().prob(
#         {ikeys.MASS_RATIO: q_sample, ikeys.CHIRP_MASS: mc_sample}, axis=0
#     )
#     return sample_prior
#
#
# def get_qmc_population_likelihood(df):
#     likelihood = bilby.hyper.likelihood.HyperparameterLikelihood(
#         posteriors=[p[[ikeys.MASS_RATIO, ikeys.CHIRP_MASS]] for p in df.posterior],
#         hyper_prior=get_qmc_hyperprior,
#         sampling_prior=sample_mass_prior,
#         log_evidences=df.log_evidence,
#     )
#     return likelihood
#
#
# def sample_mass_distribution_likelihood(results_dataframe: pd.DataFrame, outdir):
#     # likelihood_fn = get_qmc_population_likelihood(results_dataframe)
#     # hyper_param_priors = get_qmc_population_prior()
#
#     likelihood_fn = get_mass_distribution_population_likelihood(
#         results_dataframe, "uniform"
#     )
#     hyper_param_priors = get_mass_distribution_prior("uniform")
#
#     result = bilby.run_sampler(
#         likelihood=likelihood_fn,
#         priors=hyper_param_priors,
#         sampler="dynesty",
#         npoints=500,
#         walks=10,
#         outdir=os.path.join(outdir, FOLDER),
#         label="TEST2",
#     )
#
#     try:
#         result.plot_corner(
#             truth={
#                 Q_MU: Q_MU_TRUE,
#                 Q_SIGMA: Q_SIGMA_TRUE,
#                 MC_MU: MC_MU_TRUE,
#                 MC_SIGMA: MC_SIGMA_TRUE,
#             }
#         )
#     except Exception as e:
#         logger.warn(
#             f"Trouble plotting Population hyperpe corner truths {e}. Plotting without truths."
#         )
#         result.plot_corner()
