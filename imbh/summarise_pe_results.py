# #!/usr/bin/env python3
import argparse

from hyper_pe.duty_cycle import sample_duty_cycle_likelihood
from imbh_pe_calculator.pe_results_summary import (
    get_results_summary_dataframe,
    plot_results_page,
)


def main():
    parser = argparse.ArgumentParser(description="Generates a summary of results")
    parser.add_argument(
        "--results", "-r", type=str, help="path to dir with '*result.json'"
    )
    args = parser.parse_args()

    df = get_results_summary_dataframe(root_path=args.results)
    if not df.empty:

        sample_duty_cycle_likelihood(results_dataframe=df, outdir=args.results)
        plot_results_page(results_dir=args.results, df=df)
    else:
        raise Exception("no result data obtained")

if __name__ == "__main__":
    main()
