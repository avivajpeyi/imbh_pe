#!/usr/bin/env python3
# coding: utf-8
from __future__ import division, print_function

import logging
import sys

import bilby as bb
import deepdish
import numpy as np


def main():
    print(sys.argv)

    idx = sys.argv[1]
    injection_file = sys.argv[2]
    prior_file = sys.argv[3]
    dist = bool(int(sys.argv[4]))
    time = bool(int(sys.argv[5]))
    phase = bool(int(sys.argv[6]))
    outdir = "/{}".format(idx)

    bb.utils.setup_logger(log_level="info")

    logging.info(sys.argv)

    if dist:
        outdir = "dist" + outdir
        logging.info("Running with distance marginalisation.")
    if time:
        outdir = "time" + outdir
        logging.info("Running with time marginalisation.")
    if phase:
        outdir = "phase" + outdir
        logging.info("Running with phase marginalisation.")
    if not dist and not phase and not time:
        outdir = "none" + outdir

    data_seed = 170817 + int(idx)
    np.random.seed(data_seed)
    logging.info("Data seed is {}".format(data_seed))

    duration = 16.0
    sampling_frequency = 4096.0

    wfg = bb.gw.waveform_generator.WaveformGenerator(
        frequency_domain_source_model=bb.gw.source.lal_binary_black_hole,
        sampling_frequency=sampling_frequency,
        duration=duration,
        parameter_conversion=bb.gw.conversion.convert_to_lal_binary_black_hole_parameters,
    )

    try:
        injection_parameters = dict(
            deepdish.io.load(injection_file)["injections"].loc[int(idx)]
        )
        if "mass_2" in injection_parameters:
            if injection_parameters["mass_1"] < injection_parameters["mass_2"]:
                injection_parameters["mass_1"], injection_parameters["mass_2"] = (
                    injection_parameters["mass_2"],
                    injection_parameters["mass_1"],
                )
                injection_parameters["a_1"], injection_parameters["a_2"] = (
                    injection_parameters["a_2"],
                    injection_parameters["a_1"],
                )
                injection_parameters["tilt_1"], injection_parameters["tilt_2"] = (
                    injection_parameters["tilt_2"],
                    injection_parameters["tilt_1"],
                )

        injection_parameters["geocent_time"] = 15
        epoch = injection_parameters["geocent_time"] // duration * duration
        # inject = True
    except KeyError:
        epoch = 0
        outdir = "noise" + outdir
        # inject = False
        injection_parameters = None

    ifos = bb.gw.detector.InterferometerList(["H1", "L1"])
    ifos.set_strain_data_from_power_spectral_densities(
        sampling_frequency=sampling_frequency, duration=duration, start_time=epoch
    )

    ifos.inject_signal(waveform_generator=wfg, parameters=injection_parameters)

    priors = bb.gw.prior.BBHPriorDict(filename=prior_file)
    ms_prior = bb.core.prior.Uniform(
        minimum=7.5, maximum=50, name="m1_source", latex_label="$m_{1,s}$"
    )
    dc_prior = bb.gw.prior.UniformComovingVolumeTime(
        minimum=800, maximum=5000, unit="Mpc", name="comoving_distance"
    )
    z_prior = dc_prior.get_corresponding_prior("redshift")
    dl_prior = z_prior.get_corresponding_prior("luminosity_distance")
    ml_prior = bb.gw.prior.RedshiftedPrior(
        unredshifted_prior=ms_prior, redshift_prior=z_prior
    )
    priors["luminosity_distance"] = dl_prior

    priors["geocent_time"] = bb.prior.Uniform(
        minimum=epoch,
        maximum=epoch + duration,
        name="geocent_time",
        latex_label="$t_c$",
    )

    priors["mass_1"] = ml_prior
    priors["mass_1"].minimum = ms_prior.minimum * (1 + z_prior.minimum)
    priors["mass_1"].maximum = ms_prior.maximum * (1 + z_prior.maximum)

    like = bb.gw.likelihood.CosmologicalGravitationalWaveTransient(
        interferometers=ifos,
        waveform_generator=wfg,
        phase_marginalization=True,
        distance_marginalization=True,
        priors=priors,
        time_marginalization=True,
        distance_marginalization_lookup_table="/home/rory.smith/projects/cosmo_dist_marg_lookup/1gpc_to_15gpc/dist_marg_cache.npz",
    )

    priors["mass_ratio"] = bb.core.prior.Uniform(0.1, 1.0)

    sampling_seed = np.random.randint(1, 1e6)
    np.random.seed(sampling_seed)
    logging.info("Sampling seed is {}".format(sampling_seed))

    result = bb.run_sampler(
        likelihood=like,
        priors=priors,
        sampler="dynesty",
        nlive=1000,
        dlogz=0.1,
        injection_parameters=injection_parameters,
        outdir=outdir,
        label="{}_{}-{}".format("".join([ifo.name for ifo in ifos]), epoch, idx),
    )

    result.plot_corner(filename="/corner.png")


if __name__ == "__main__":
    main()
