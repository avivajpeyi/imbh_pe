#!/usr/bin/env python3
from __future__ import division, print_function

import argparse
import logging
import os

import injection_parameter_generator.injection_keys as keys
import matplotlib
from tools.file_utils import IncorrectFileType

try:
    import bilby
except ImportError:
    matplotlib.use("PS")
    import bilby


DURATION = 16.0
SAMPLING_FREQUENCY = 4096.0
GEOCENT_TIME = 8
LABEL = "{}-injection{}"
CORNER_PLOT_FNAME = "corner.png"
SAMPLER = "dynesty"


def run_pe_on_injection(
    injection_parameters_dict: dict,
    injection_id_num: int,
    prior_file: str,
    out_dir: str,
) -> None:

    bilby.utils.setup_logger(log_level="info")

    # creating waveform generator that will be used to construct the injection signal
    waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
        frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        sampling_frequency=SAMPLING_FREQUENCY,
        duration=DURATION,
        start_time=0,
        parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
    )

    # setting up detectors, creating and injecting signal into detector data
    interferometer_list = bilby.gw.detector.InterferometerList([keys.H1, keys.L1])

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

    # load priors
    priors = bilby.gw.prior.BBHPriorDict(prior_file)

    # initialise the likelihood function
    likelihood = bilby.gw.GravitationalWaveTransient(
        interferometers=interferometer_list,
        waveform_generator=waveform_generator,
        priors=priors,
        distance_marginalization=True,
        phase_marginalization=True,
        time_marginalization=True,
    )

    # generating a label for current run
    label = LABEL.format(
        "".join([ifo.name for ifo in interferometer_list]), injection_id_num
    )
    out_dir = os.path.join(out_dir, label)
    logging.info("Beginning sampling for {}".format(label))

    # run sampler and plot corner plot of pe results
    result = bilby.run_sampler(
        likelihood=likelihood,
        priors=priors,
        sampler=SAMPLER,
        walkers=100,
        nlive=1000,
        dlogz=0.1,
        injection_parameters=injection_parameters_dict,
        outdir=out_dir,
        label=label,
        conversion_function=bilby.gw.conversion.generate_all_bbh_parameters,
    )
    result.plot_corner(
        filename=os.path.join(out_dir, CORNER_PLOT_FNAME), quantiles=[0.05, 0.95]
    )


def parse_args(args):
    parser = argparse.ArgumentParser(description="imbh signal pe runner")
    required = parser.add_argument_group("required named arguments")
    required.add_argument(
        "--injection_file", "-f", type=str, help="h5 file of a dataframe of injections"
    )
    required.add_argument(
        "--idx", "-i", type=int, help="index number of injection from injection file"
    )
    required.add_argument(
        "--prior_file",
        "-p",
        type=str,
        help="prior file for what is known about IMBH signals",
    )
    required.add_argument(
        "--out_dir", "-o", type=str, help="the out dir for the PE results"
    )
    args = parser.parse_args(args)

    # verifying correct file types
    if not args.injection_file.endswith(".h5"):
        raise IncorrectFileType(
            "Injection file does not end with '.h5': {}".format(args.injection_file)
        )

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            "Prior file does not end with '.prior': {}".format(args.prior_file)
        )

    return args
