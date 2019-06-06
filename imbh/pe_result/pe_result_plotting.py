import math
import os
import re

import bilby
import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import numpy as np
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
from tools.utils import flatten_dict, list_dicts_to_dict_lists

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

    html_paths = [plot_mass_data(), plot_data_table(), plot_analysis_statistics_data()]
    sections = [SectionTemplate(title=p, html_paths=p) for p in html_paths]

    report_file_name = "report.html"
    with open(report_file_name, "w") as report_file:
        report_file.write(html_string)
        report_file.close()

    logger.info("File saved at : " + save_dir)


def save_pp_plot(root_path: str, keys=None):
    """

    :param root_path:
    :param keys: A list of keys to use, if None defaults to search_parameter_keys
    :return:
    """
    result_files = get_filepaths(root_path, file_regex=rkeys.RESULT_FILE_REGEX)
    results = [bilby.core.result.read_in_result(f) for f in result_files]
    bilby.core.result.make_pp_plot(
        results, keys=keys, filename=os.path.join(root_path, "pp.png")
    )
