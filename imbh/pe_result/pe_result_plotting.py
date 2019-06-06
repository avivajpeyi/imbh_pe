import os

import bilby
import imbh_pe_calculator.results_keys as rkeys
import pandas as pd
from bilby.core.utils import logger
from pe_result.plotting.summary_graphs import (
    plot_analysis_statistics_data,
    plot_mass_data,
)
from pe_result.plotting.summary_table import plot_data_table
from pe_result.templates.section_template import SectionTemplate
from pe_result.templates.summary_template import SummaryTemplate
from tools.file_utils import get_filepaths

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
    mass_path = plot_mass_data(
        df, filename=os.path.join(save_dir, "mass_distribution.html")
    )
    data_table_path = plot_data_table(
        df, filename=os.path.join(save_dir, "summary_table.html")
    )
    analysis_stats_path = plot_analysis_statistics_data(
        df, filename=os.path.join(save_dir, "analysis_histograms.html")
    )

    # building summary page
    sections = [
        SectionTemplate(
            title="Injected Masses", html_path=mass_path, height="500", width="90%"
        ),
        SectionTemplate(title="Summary Table", html_path=data_table_path, height="500"),
        SectionTemplate(
            title="PE Statistics", html_path=analysis_stats_path, height="500"
        ),
        SectionTemplate(
            title="P-P test",
            html_path="pp.png",
            width="50%",
            height="50%",
            text="P-P test for q is inaccurate as prior provided for PE is 1/q",
            is_img=True,
        ),
        SectionTemplate(
            title="Duty Cycle",
            html_path="hyper_pe/DutyCycle_corner.png",
            width="50%",
            height="50%",
            is_img=True,
        ),
    ]
    summary_page = SummaryTemplate(title="IMBH Injection PE Summary", sections=sections)

    report_file_name = os.path.join(save_dir, "summary_report.html")
    with open(report_file_name, "w") as report_file:
        report_file.write(summary_page.render())
        report_file.close()

    logger.info("File saved at " + report_file_name)


def save_pp_plot(results_dir: str, keys=None):
    """

    :param root_path:
    :param keys: A list of keys to use, if None defaults to search_parameter_keys
    :return:
    """
    result_files = get_filepaths(results_dir, file_regex=rkeys.RESULT_FILE_REGEX)
    results = [bilby.core.result.read_in_result(f) for f in result_files]
    bilby.core.result.make_pp_plot(
        results, keys=keys, filename=os.path.join(results_dir, "pp.png")
    )
