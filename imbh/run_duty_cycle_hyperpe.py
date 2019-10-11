# #!/usr/bin/env python3
import argparse
import logging
import os

import pandas as pd
from hyper_pe.duty_cycle import sample_duty_cycle_likelihood

logging.basicConfig(level=logging.DEBUG)


def start_duty_cycle_sampling(evid_csv_path):
    evid_df = pd.read_csv(evid_csv_path)
    sample_duty_cycle_likelihood(evid_df, os.path.dirname(evid_csv_path))


def main():
    parser = argparse.ArgumentParser(description="Generates duty cyckle from evid csv")
    parser.add_argument("--csv", "-c", type=str, help="path to csv of evid'")
    args = parser.parse_args()
    start_duty_cycle_sampling(args.csv)


if __name__ == "__main__":
    main()
