# #!/usr/bin/env python3
import argparse

from hyper_pe.duty_cycle import sample_duty_cycle_likelihood
from imbh_pe_calculator.pe_results_summary import (
    get_results_dataframe,
    plot_results_page,
)


def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        "--results", "-r", type=str, help="path to dir with '*result.json'"
    )
    args = parser.parse_args()

    df = get_results_dataframe(args.results)
    sample_duty_cycle_likelihood(df)
    plot_results_page(args.results, df)


if __name__ == "__main__":
    main()
