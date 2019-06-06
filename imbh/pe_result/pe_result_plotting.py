import os

import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from numpy import np
from pe_result import colors
from pe_result.latex_label import LATEX_LABEL_DICT
from plotly.offline import plot

BILBY_LOGO = "https://git.ligo.org/uploads/-/system/project/avatar/1846/bilby.jpg"


def plot_result_page(results_dir: str, df: pd.DataFrame):
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
    report_file_name = "report.html"
    with open(report_file_name, "w") as report_file:
        report_file.write(html_string)
        report_file.close()

    logger.info("File saved at : " + save_dir)
