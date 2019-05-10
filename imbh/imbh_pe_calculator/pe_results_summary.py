#!/usr/bin/env python3
import math
import os

import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import matplotlib
import numpy as np
import pandas as pd
from tools.file_utils import IncorrectFileType, get_filepaths

try:
    import bilby
except ImportError:
    matplotlib.use("PS")

    import bilby


class ResultSummary(object):
    def __init__(self, results_filepath: str):
        pe_result = bilby.core.result.read_in_result(filename=results_filepath)
        interferometer_data = pe_result.meta_data.get(rkeys.LIKELIHOOD).get(
            ikeys.INTERFEROMETERS
        )

        self.snr = self._get_snr(interferometer_data)
        self.parameters = self._get_parameters(interferometer_data)
        self.inj_num = int(self.parameters.get(ikeys.INJECTION_NUMBER, -1))

        split_path = results_filepath.split("/home/avi.vajpeyi/public_html/")
        gotdata = len(split_path) > 1 and split_path[1]
        self.path = '<a href="https://ldas-jobs.ligo.caltech.edu/~avi.vajpeyi/{}">{}</a>'.format(
            split_path[1] if gotdata else "_", self.inj_num
        )
        self.q = self.parameters.get(ikeys.MASS_1) / self.parameters.get(ikeys.MASS_2)
        self.log_bayes_factor = pe_result.log_bayes_factor
        self.log_evidence = pe_result.log_evidence
        self.log_noise_evidence = pe_result.log_noise_evidence

    @staticmethod
    def _get_parameters(interferometer_data: dict):
        return interferometer_data.get(ikeys.INTERFEROMETER_LIST[0]).get(
            rkeys.PARAMETERS
        )

    @staticmethod
    def _get_snr(interferometer_data: dict) -> float:
        snr_vals = np.array(
            [
                interferometer_data.get(interferometer_id).get(rkeys.MATCHED_FILTER_SNR)
                for interferometer_id in ikeys.INTERFEROMETER_LIST
            ]
        )
        return math.sqrt(sum(abs(snr_vals) ** 2))

    def to_dict(self):
        result_summary_dict = {
            rkeys.INJECTION_NUMBER: self.inj_num,
            rkeys.SNR: self.snr,
            rkeys.LOG_BF: self.log_bayes_factor,
            rkeys.LOG_EVIDENCE: self.log_evidence,
            rkeys.LOG_NOISE_EVIDENCE: self.log_noise_evidence,
            rkeys.Q: self.q,
            rkeys.PATH: self.path,
        }
        result_summary_dict.update(self.parameters)  # this unwraps the parameters
        return result_summary_dict


def get_results_summary_dataframe(root_path: str):

    results_list = []
    result_files = get_filepaths(
        root_path=root_path, file_regex=rkeys.RESULT_FILE_REGEX
    )
    if result_files:
        try:
            results_list = [ResultSummary(f).to_dict() for f in result_files]
        except (AttributeError, ValueError, TypeError):
            raise IncorrectFileType("{} is not a inj PE result".format(result_files))

    if results_list:
        # convert list of dict to dict of lists
        results_keys = results_list[0].keys()
        results_dict = {
            key: [result_dict.get(key, np.NaN) for result_dict in results_list]
            for key in results_keys
        }

        # saving data into a dataframe
        results_df = pd.DataFrame(results_dict)
        results_df.sort_values(by=[rkeys.LOG_BF], na_position="first", inplace=True)
        results_df.dropna(inplace=True)
        results_df.to_csv("test_result_sum.csv")
        return results_df

    else:
        return None


def plot_results_page(results_dir: str, df: pd.DataFrame):
    import plotly.graph_objs as go
    import plotly as py

    df_keys = [
        rkeys.PATH,
        rkeys.Q,
        rkeys.SNR,
        rkeys.LOG_BF,
        rkeys.LOG_EVIDENCE,
        rkeys.LOG_NOISE_EVIDENCE,
    ]
    headers = ["i#", "Q", "SNR", "LnBF", "lnZ", "lnZn"]

    table_trace1 = go.Table(
        columnwidth=[5] + [10, 10, 10, 10, 10],
        domain=dict(x=[0, 0.5], y=[0, 1.0]),
        header=dict(
            values=headers,
            line=dict(color="rgb(50, 50, 50)"),
            align=["left"] * 5,
            font=dict(color=["rgb(45, 45, 45)"] * 5, size=14),
            fill=dict(color="#d562be"),
        ),
        cells=dict(
            values=[df[k] for k in df_keys],
            line=dict(color="#506784"),
            align=["left"] * 5,
            font=dict(color=["rgb(40, 40, 40)"] * 5, size=12),
            format=[None] + [".2f"] * 4,
            fill=dict(color=["rgb(235, 193, 238)", "rgba(228, 222, 249, 0.65)"]),
        ),
    )

    axis = dict(
        showline=True,
        zeroline=False,
        showgrid=True,
        mirror=True,
        ticklen=4,
        gridcolor="#ffffff",
        tickfont=dict(size=10),
    )

    mass_scat = go.Scatter(
        x=df.mass_1,
        y=df.mass_2,
        text=[
            "{:.2f},{:.2f}".format(df.mass_1.values[i], df.mass_2.values[i])
            for i in range(len(df))
        ],
        mode="markers",
        xaxis="x1",
        yaxis="y1",
        hoverinfo="text",
        name="mass",
    )

    hist_q = go.Histogram(x=df.q, xaxis="x2", yaxis="y2", opacity=0.75, name="q count")

    hist_lbf = go.Histogram(
        x=df[rkeys.LOG_BF], xaxis="x4", yaxis="y4", opacity=0.75, name="LnBF count"
    )

    hist_snr = go.Histogram(
        x=df.snr, xaxis="x3", yaxis="y3", opacity=0.75, name="snr count"
    )

    layout1 = dict(
        autosize=True,
        title="IMBH PE Results",
        margin=dict(t=100),
        showlegend=False,
        xaxis1=dict(axis, title="Mass Ratio", **dict(domain=[0.55, 1], anchor="y1")),
        yaxis1=dict(axis, **dict(domain=[0.75, 1.0], anchor="x1")),
        xaxis2=dict(axis, title="SNR Histogram", **dict(domain=[0.55, 1], anchor="y2")),
        yaxis2=dict(axis, **dict(domain=[0.50, 0.70], anchor="x2")),
        xaxis3=dict(
            axis, title="LnBF Histogram", **dict(domain=[0.55, 1], anchor="y3")
        ),
        yaxis3=dict(axis, **dict(domain=[0.25, 0.45], anchor="x3")),
        xaxis4=dict(axis, **dict(domain=[0.55, 1], anchor="y4")),
        yaxis4=dict(axis, **dict(domain=[0.0, 0.2], anchor="x4")),
    )

    plotting_dict = dict(
        data=[table_trace1, mass_scat, hist_q, hist_snr, hist_lbf], layout=layout1
    )

    save_dir = os.path.join(results_dir, "result_summary.html")
    py.offline.plot(plotting_dict, filename=save_dir, auto_open=False)
    print("File saved at : " + save_dir)
