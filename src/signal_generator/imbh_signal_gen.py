# #!/usr/bin/env python3
# from __future__ import division, print_function
#
# import argparse
# import logging
# import sys
#
# import bilby as bb
# import deepdish
# import numpy as np
#
# bb.utils.setup_logger(log_level="info")
#
# DURATION = 16.0
# SAMPLING_FREQUENCY = 4096.0
#
#
# def generate_wave():
#
#     wfg = bb.gw.waveform_generator.WaveformGenerator(
#         frequency_domain_source_model=bb.gw.source.lal_binary_black_hole,
#         sampling_frequency=DURATION,
#         duration=SAMPLING_FREQUENCY,
#         parameter_conversion=bb.gw.conversion.convert_to_lal_binary_black_hole_parameters,
#     )
#
#
# def main():
#     parser = argparse.ArgumentParser(description="imbh signal generator")
#     parser.add_argument(
#         "--jobs", "-j", default=5, type=int, help="number of jobs to be created"
#     )
#     parser.add_argument(
#         "--fname", "-f", type=str, default="inj_imbh.dag", help="file name for output"
#     )
#     args = parser.parse_args()
#
#     if not args.fname.endswith(".dag"):
#         args.fname = args.fname + ".dag"
#
#
# if __name__ == "__main__":
#     main()
