#!/usr/bin/env python3
from __future__ import division, print_function

import argparse
import logging
import os

import bilby as bb
import deepdish
import imbh.injection_parameter_generator.injection_keys as keys
import pandas as pd

bb.utils.setup_logger(log_level="info")

DURATION = 16.0
SAMPLING_FREQUENCY = 4096.0


def run_pe_on_injection(
    injection_parameters_dataframe: pd.DataFrame,
    injection_id_num: int,
    priors: bb.gw.prior.BBHPriorDict,
    out_dir: str,
) -> None:

    # creating waveform generator that will be used to construct the injection signal
    waveform_generator = bb.gw.waveform_generator.WaveformGenerator(
        frequency_domain_source_model=bb.gw.source.lal_binary_black_hole,
        sampling_frequency=DURATION,
        duration=SAMPLING_FREQUENCY,
        parameter_conversion=bb.gw.conversion.convert_to_lal_binary_black_hole_parameters,
    )

    # setting up detectors, creating and injecting signal into detector data
    interferometer_list = bb.gw.detector.InterferometerList([keys.H1, keys.L1])
    interferometer_list.inject_signal(
        waveform_generator=waveform_generator, parameters=injection_parameters_dataframe
    )

    # Initialise the likelihood function
    likelihood = bb.gw.GravitationalWaveTransient(
        interferometers=interferometer_list, waveform_generator=waveform_generator
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
        nlive=1000,
        dlogz=0.1,
        injection_parameters=injection_parameters_dataframe,
        outdir=out_dir,
        label=label,
    )
    result.plot_corner(filename=os.path.join(out_dir, "corner.png"))


def main():
    parser = argparse.ArgumentParser(description="imbh signal pe runner")
    parser.add_argument(
        "--injection_file", "-f", type=str, help="h5 file of a dataframe of injections"
    )
    parser.add_argument(
        "--idx", "-i", type=int, help="index number of injection from injection file"
    )
    parser.add_argument(
        "--prior_file",
        "-p",
        type=str,
        help="prior file for what is known about IMBH signals",
    )
    parser.add_argument(
        "--out_dir", "-o", type=str, help="the out dir for the PE results"
    )
    args = parser.parse_args()

    # verifying correct file types
    if not args.injection_file.endswith(".h5"):
        raise IncorrectFileType(
            f"Injection file does not end with '.h5': {args.injection_file}"
        )

    if not args.prior_file.endswith(".prior"):
        raise IncorrectFileType(
            f"Prior file does not end with '.prior': {args.prior_file}"
        )

    # unpacking injection parameters and priors
    injection_dict = dict(deepdish.io.load(args.injection_file))
    injection_param_dataframe = injection_dict.get(keys.INJECTION).loc[args.idx]
    priors = bb.gw.prior.BBHPriorDict(filename=args.prior_file)

    run_pe_on_injection(
        injection_parameters_dataframe=injection_param_dataframe,
        injection_id_num=args.idx,
        priors=priors,
        out_dir=args.out_dir,
    )


class IncorrectFileType(Exception):
    pass


if __name__ == "__main__":
    main()
