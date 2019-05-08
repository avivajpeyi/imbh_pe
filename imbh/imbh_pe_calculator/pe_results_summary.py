#!/usr/bin/env python3
import math
import os
import re

import matplotlib
import numpy as np
import pandas as pd
from tools.file_utils import get_filepaths

try:
    import bilby
except ImportError:
    matplotlib.use("PS")
    import bilby

LIKELIHOOD = "likelihood"
INTERFEROMETERS = "interferometers"
MATCHED_FILTER_SNR = "matched_filter_SNR"
INTERFEROMETER_LIST = ["H1", "L1"]
INJ_ID_SEARCH = "injection(.*?)_result.json"
RESULT_FILE_ENDING = "result.json"


PARAMETERS = "parameters"
SUMMARY_FILE_NAME = "pe_results_summary.h5"
CORNER_FILE = "corner.png"
PLOT = "plot"


INJECTION_NUMBER = "InjNum"
SNR = "snr"
LOG_BF = "log_bayes_factor"
Q = "q"
LOG_EVIDENCE = "log_evidence"
LOG_NOISE_EVIDENCE = "log_noise_evidence"


class ResultSummary(object):
    def __init__(self, results_filepath):

        try:

            pe_result = bilby.core.result.read_in_result(filename=results_filepath)
            interferometer_data = pe_result.meta_data.get(LIKELIHOOD).get(
                INTERFEROMETERS
            )
            self.inj_num = int(
                re.search(INJ_ID_SEARCH, os.path.basename(results_filepath)).group(1)
            )
            self.snr = self._get_snr(interferometer_data)

            self.parameters = interferometer_data.get(INTERFEROMETER_LIST[0]).get(
                PARAMETERS
            )

            self.log_bayes_factor = pe_result.log_bayes_factor
            self.log_evidence = pe_result.log_evidence
            self.log_noise_evidence = pe_result.log_evidence
            self.q = self.parameters.get("mass_1") / self.parameters.get("mass_2")

        except AttributeError:
            raise Exception("file: {}".format(results_filepath))

    @staticmethod
    def _get_snr(interferometer_data):
        snr_vals = np.array(
            [
                interferometer_data.get(interferometer_id).get(MATCHED_FILTER_SNR)
                for interferometer_id in INTERFEROMETER_LIST
            ]
        )
        return math.sqrt(sum(abs(snr_vals) ** 2))

    def to_dict(self):
        result_summary_dict = {
            INJECTION_NUMBER: self.inj_num,
            SNR: self.snr,
            LOG_BF: self.log_bayes_factor,
            LOG_EVIDENCE: self.log_evidence,
            LOG_NOISE_EVIDENCE: self.log_noise_evidence,
            Q: self.q,
        }
        result_summary_dict.update(self.parameters)  # this unwraps the parameters
        return result_summary_dict


def get_results_dataframe(path):

    results_list = []
    for f in get_filepaths(path, file_ending=RESULT_FILE_ENDING):
        results_list.append(ResultSummary(f).to_dict())

    if results_list:
        # convert list of dict to dict of lists
        results_keys = results_list[0].keys()
        results_dict = {
            key: [result_dict.get(key, np.NaN) for result_dict in results_list]
            for key in results_keys
        }

        # saving data into a dataframe
        results_df = pd.DataFrame(results_dict)
        results_df.sort_values(by=[INJECTION_NUMBER])
        results_df.to_csv("test_result_sum.csv")
        results_df.fillna(np.nan, inplace=True)
        return results_df

    else:
        return None


def plot_results_page(results_dir, df):
    import plotly.graph_objs as go
    import plotly as py

    keys = [INJECTION_NUMBER, SNR, LOG_BF, Q]

    table_trace1 = go.Table(
        columnwidth=[15] + [15, 15, 15, 30],
        domain=dict(x=[0, 0.5], y=[0, 1.0]),
        header=dict(
            values=keys,
            line=dict(color="rgb(50, 50, 50)"),
            align=["left"] * 5,
            font=dict(color=["rgb(45, 45, 45)"] * 5, size=14),
            fill=dict(color="#d562be"),
        ),
        cells=dict(
            values=[df[k] for k in keys],
            line=dict(color="#506784"),
            align=["left"] * 5,
            font=dict(color=["rgb(40, 40, 40)"] * 5, size=12),
            format=[None, None, None, ".2f", None],
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

    hist_log_evid = go.Histogram(
        x=df.log_evidence, xaxis="x1", yaxis="y1", opacity=0.75, name="Log Z(signal)"
    )
    hist_log_noise_evid = go.Histogram(
        x=df.log_noise_evidence,
        xaxis="x1",
        yaxis="y1",
        opacity=0.75,
        name="Log Z(noise)",
    )

    hist_q = go.Histogram(x=df.q, xaxis="x2", yaxis="y2", opacity=0.75, name="q count")

    hist_snr = go.Histogram(
        x=df.snr, xaxis="x3", yaxis="y3", opacity=0.75, name="snr count"
    )

    layout1 = dict(
        autosize=True,
        title="IMBH PE Results",
        margin=dict(t=100),
        showlegend=False,
        xaxis1=dict(
            axis,
            title="Mass Ratio",
            **dict(domain=[0.55, 1], anchor="y1", showticklabels=False)
        ),
        yaxis1=dict(axis, **dict(domain=[0.66, 1.0], anchor="x1")),
        xaxis2=dict(
            axis,
            title="SNR Histogram",
            **dict(domain=[0.55, 1], anchor="y2", showticklabels=False)
        ),
        yaxis2=dict(axis, **dict(domain=[0.3 + 0.03, 0.63], anchor="x2")),
        xaxis3=dict(axis, **dict(domain=[0.55, 1], anchor="y3")),
        yaxis3=dict(axis, **dict(domain=[0.0, 0.3], anchor="x3")),
    )

    plotting_dict = dict(
        data=[table_trace1, hist_log_evid, hist_log_noise_evid, hist_q, hist_snr],
        layout=layout1,
    )

    save_dir = os.path.join(results_dir, "result_summary.html")
    py.offline.plot(plotting_dict, filename=save_dir, auto_open=True)
    print("File saved at : " + save_dir)
