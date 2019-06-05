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
    report_file_name = "report.html"
    with open(report_file_name, "w") as report_file:
        report_file.write(html_string)
        report_file.close()

    logger.info("File saved at : " + save_dir)
