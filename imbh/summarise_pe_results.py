# #!/usr/bin/env python3
import argparse

from imbh_pe_calculator.pe_results_summary import combine_summary_and_samples_dataframes


def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        "--results", "-r", type=str, help="path to dir with '*result.json'"
    )
    parser.add_argument(
        "--inj", "-i", type=str, help="path to dir with 'injection_param.h5'"
    )
    args = parser.parse_args()

    combine_summary_and_samples_dataframes(args.results, args.inj)
