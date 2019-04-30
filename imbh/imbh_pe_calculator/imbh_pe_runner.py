#!/usr/bin/env python3
from __future__ import division, print_function

import logging
import os

import imbh.injection_parameter_generator.injection_keys as keys
import matplotlib

matplotlib.use("PS")


DURATION = 16.0
SAMPLING_FREQUENCY = 4096.0
GEOCENT_TIME = 8


def run_pe_on_injection(
    injection_parameters_dict: dict,
    injection_id_num: int,
    prior_file: str,
    out_dir: str,
) -> None:

    import bilby as bb

    bb.utils.setup_logger(log_level="info")

    # creating waveform generator that will be used to construct the injection signal
    waveform_generator = bb.gw.waveform_generator.WaveformGenerator(
        frequency_domain_source_model=bb.gw.source.lal_binary_black_hole,
        sampling_frequency=SAMPLING_FREQUENCY,
        duration=DURATION,
        start_time=0,
        parameter_conversion=bb.gw.conversion.convert_to_lal_binary_black_hole_parameters,
    )

    # setting up detectors, creating and injecting signal into detector data
    interferometer_list = bb.gw.detector.InterferometerList([keys.H1, keys.L1])

    # setting up the strain data with some noise
    interferometer_list.set_strain_data_from_power_spectral_densities(
        sampling_frequency=SAMPLING_FREQUENCY,
        duration=DURATION,
        start_time=injection_parameters_dict.get(keys.GEOCENT_TIME) - 3,
    )

    # injecting the signal into the interferometer data
    interferometer_list.inject_signal(
        waveform_generator=waveform_generator, parameters=injection_parameters_dict
    )

    # load default priors
    new_priors = bb.gw.prior.BBHPriorDict(prior_file)
    priors = bb.gw.prior.BBHPriorDict()
    priors.update(new_priors)

    # initialise the likelihood function
    likelihood = bb.gw.GravitationalWaveTransient(
        interferometers=interferometer_list,
        waveform_generator=waveform_generator,
        priors=priors,
        distance_marginalization=True,
        phase_marginalization=True,
        time_marginalization=True,
    )

    # generating a label for current run
    label = "{}-injection{}".format(
        "".join([ifo.name for ifo in interferometer_list]), injection_id_num
    )
    out_dir = os.path.join(out_dir, label)
    logging.info(f"Beginning sampling for {label}")

    # run sampler and plot corner plot of pe results
    result = bb.run_sampler(
        likelihood=likelihood,
        priors=priors,
        sampler="dynesty",
        walkers=100,
        nlive=1000,
        dlogz=0.1,
        injection_parameters=injection_parameters_dict,
        outdir=out_dir,
        label=label,
        conversion_function=bb.gw.conversion.generate_all_bbh_parameters,
    )
    result.plot_corner(
        filename=os.path.join(out_dir, "corner.png"), quantiles=[0.05, 0.95]
    )
