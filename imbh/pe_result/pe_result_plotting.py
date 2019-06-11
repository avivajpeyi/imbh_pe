import os

import bilby
import pandas as pd
from bilby.core.utils import logger
from pe_result.plotting.summary_graphs import (
    plot_analysis_statistics_data,
    plot_mass_distribution,
    plot_mass_scatter,
    plot_pp_test,
)
from pe_result.plotting.summary_table import plot_data_table
from pe_result.templates.section_template import SectionTemplate
from pe_result.templates.summary_template import SummaryTemplate

bilby.utils.setup_logger(log_level="info")


def plot_results_page(results_dir: str, df: pd.DataFrame):
    """
    Given a directory of Bibly result.json and corner.png


    Makes pages of
        * injection and their PEs' summary table
        * injected mass distribution
        * PE snr and lnBF distribution
        * pp-test

    Combines the pages into a net summary page


    :param results_dir:
    :param df:
    :return:
    """

    save_dir = results_dir

    # plotting separate summary graphs and tables
    mass_scatter_path = plot_mass_scatter(
        df, filename=os.path.join(save_dir, "mass_scatter.html")
    )

    mass_distribution_path = plot_mass_distribution(
        df, filename=os.path.join(save_dir, "mass_distribution")
    )
    mass_distribution_is_image = is_file_image(mass_distribution_path)

    data_table_path = plot_data_table(
        df, filename=os.path.join(save_dir, "summary_table.html")
    )
    analysis_stats_path = plot_analysis_statistics_data(
        df, filename=os.path.join(save_dir, "analysis_histograms.html")
    )

    pp_test_path = plot_pp_test(results_dir)
    pp_test_is_img = is_file_image(pp_test_path)

    hyperpe_z_normal = bilby.core.result.read_in_result(
        os.path.join(save_dir, "hyper_pe/normalMassDistribution_result.json")
    ).log_evidence
    hyperpe_z_uniform = bilby.core.result.read_in_result(
        os.path.join(save_dir, "hyper_pe/uniformMassDistribution_result.json")
    ).log_evidence

    # building summary page
    sections = [
        SectionTemplate(
            title="Injected Masses",
            html_path=mass_scatter_path,
            height="500",
            width="90%",
        ),
        SectionTemplate(
            title="",
            html_path=mass_distribution_path,
            height="500",
            width="90%",
            is_img=mass_distribution_is_image,
        ),
        SectionTemplate(
            title="Summary Table",
            html_path=data_table_path,
            height="500",
            text=f"{len(df)} injections. Click on the Injection Numbers to go to the corresponding corner plot.",
        ),
        SectionTemplate(
            title="PE Statistics", html_path=analysis_stats_path, height="500"
        ),
        SectionTemplate(
            title="P-P test",
            html_path=pp_test_path,
            width="50%",
            height="50%",
            is_img=pp_test_is_img,
        ),
        SectionTemplate(
            title="Duty Cycle",
            html_path="hyper_pe/DutyCycle_corner.png",
            width="50%",
            height="50%",
            is_img=True,
        ),
        SectionTemplate(
            title="Mass Distribution: Normal distribution",
            html_path="hyper_pe/normalMassDistribution_corner.png",
            width="50%",
            height="50%",
            is_img=True,
        ),
        SectionTemplate(
            title="Mass Distribution: Uniform distribution",
            html_path="hyper_pe/uniformMassDistribution_corner.png",
            width="50%",
            height="50%",
            is_img=True,
            text=f"Log BF (uniform - normal): {hyperpe_z_uniform-hyperpe_z_normal}",
        ),
    ]
    summary_page = SummaryTemplate(title="IMBH Injection PE Summary", sections=sections)

    report_file_name = os.path.join(save_dir, "summary_report.html")
    with open(report_file_name, "w") as report_file:
        report_file.write(summary_page.render())
        report_file.close()

    logger.info("File saved at " + report_file_name)


def is_file_image(f):
    return True if f.endswith(".png") else False
