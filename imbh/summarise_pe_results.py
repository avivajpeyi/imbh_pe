# #!/usr/bin/env python3
import argparse

from bilby.core.utils import logger, setup_logger
from hyper_pe.duty_cycle import sample_duty_cycle_likelihood
from hyper_pe.population_inference import sample_mass_distribution_likelihood
from pe_result.pe_result_plotting import plot_results_page
from pe_result.pe_results_summary import get_results_summary_dataframe

setup_logger(log_level="info")


def main():
    parser = argparse.ArgumentParser(description="Generates a summary of results")
    parser.add_argument(
        "--results", "-r", type=str, help="path to dir with '*result.json'"
    )
    args = parser.parse_args()

    df = get_results_summary_dataframe(root_path=args.results)
    logger.info(
        "{} PEs each with {} posterior samples".format(
            df.shape[0], len(df.iloc[0].posterior)
        )
    )

    if not df.empty:
        sample_duty_cycle_likelihood(results_dataframe=df, outdir=args.results)
        sample_mass_distribution_likelihood(results_dataframe=df, outdir=args.results)
        plot_results_page(results_dir=args.results, df=df)
    else:
        raise Exception("No result data obtained")


if __name__ == "__main__":
    main()
