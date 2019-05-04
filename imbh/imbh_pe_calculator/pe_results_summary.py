#!/usr/bin/env python3
import math
import os
import re

import matplotlib
import numpy as np
import pandas as pd
from injection_parameter_generator.imbh_parameter_generator import (
    load_injection_param_dataframe_from_h5,
)
from tools.file_utils import get_filepaths

matplotlib.use("PS")

LIKELIHOOD = "likelihood"
INTERFEROMETERS = "interferometers"
MATCHED_FILTER_SNR = "matched_filter_SNR"
INTERFEROMETER_LIST = ["H1", "L1"]
INJ_ID_SEARCH = "/H1L1-injection(.*?)/H1L1-injection"
RESULT_FILE_ENDING = "result.json"

INJECTION_NUMBER = "InjNum"
SNR = "snr"
LOG_BF = "lnBF"

PARAMETERS = "parameters"
SUMMARY_FILE_NAME = "pe_results_summary.h5"


def get_results_dataframe(path):
    import bilby as bb

    snr = []
    inj_num = []
    log_bf = []
    parameters = []
    snr_at_inter = {"{} snr".format(i): [] for i in INTERFEROMETER_LIST}
    for idx, f in enumerate(get_filepaths(path, file_ending=RESULT_FILE_ENDING)):
        inj_num.append(int(re.search(INJ_ID_SEARCH, f).group(1)))
        pe_result = bb.core.result.read_in_result(filename=f)

        # getting net signal:noise ratio
        snr_temp = 0
        interferometer_data = pe_result.meta_data.get(LIKELIHOOD).get(INTERFEROMETERS)
        for interferometer_id in INTERFEROMETER_LIST:
            interferometer_snr = interferometer_data.get(interferometer_id).get(
                MATCHED_FILTER_SNR
            )
            snr_temp += abs(interferometer_snr) ** 2
            snr_at_inter["{} snr".format(interferometer_id)].append(interferometer_snr)
        snr.append(math.sqrt(snr_temp))
        parameters.append(
            interferometer_data.get(INTERFEROMETER_LIST[0]).get(PARAMETERS)
        )
        log_bf.append(pe_result.log_bayes_factor)
    parameters_dic = {
        key: [dic.get(key, np.NaN) for dic in parameters]
        for key in parameters[0].keys()
    }
    data_dict = {INJECTION_NUMBER: inj_num, SNR: snr, LOG_BF: log_bf}

    data_dict.update(snr_at_inter)
    data_dict.update(parameters_dic)
    df = pd.DataFrame(data_dict)
    df.sort_values(by=[INJECTION_NUMBER])
    df.fillna(np.nan, inplace=True)
    return df


def combine_summary_and_samples_dataframes(results_dir, samples_df_path):
    results_summary = get_results_dataframe(results_dir)
    param_inj_ids = load_injection_param_dataframe_from_h5(samples_df_path)
    df = results_summary.merge(param_inj_ids, how="outer", indicator=True).sort_values(
        by=[INJECTION_NUMBER], ascending=True
    )

    df.drop_duplicates(subset=[INJECTION_NUMBER], inplace=True, keep="first")
    return df


def plot_results_page(results_dir, df):
    import plotly.graph_objs as go
    import plotly as py

    df.drop(df.select_dtypes(["complex"]), inplace=True, axis=1)
    keys = ["InjNum", "snr", "lnBF", "q"]
    headers = ["Inj", "SNR", "Log BF", "q"]
    df["q"] = df.mass_1 / df.mass_2
    df["analysing"] = np.where(df.snr > 0, "complete", "running")

    table_trace1 = go.Table(
        columnwidth=[20] + [33, 35, 33],
        domain=dict(x=[0, 0.5], y=[0, 1.0]),
        header=dict(
            values=headers,
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
            format=[None, None, None, ".2f"],
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

    hist_analysing = go.Histogram(
        x=df.analysing, xaxis="x1", yaxis="y1", opacity=0.75, name="PE Complete"
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
        annotations=[
            dict(
                x=0.5,
                y=len(df.analysing) + 20,
                showarrow=False,
                text="Job Status",
                xref="x1",
                yref="y1",
            )
        ],
    )

    plotting_dict = dict(
        data=[table_trace1, hist_analysing, hist_q, hist_snr], layout=layout1
    )
    py.offline.plot(
        plotting_dict,
        filename=os.path.join(results_dir, "result_summary.html"),
        auto_open=True,
    )
