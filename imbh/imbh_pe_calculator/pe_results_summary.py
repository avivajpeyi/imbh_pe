import math
import os
import re

import bilby
import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import numpy as np
import pandas as pd
from tools.file_utils import get_filepaths
from tools.utils import flatten_dict, list_dicts_to_dict_lists


class ResultSummary(object):
    def __init__(self, results_filepath: str):
        self.path = results_filepath
        self.inj_num = self._get_injection_number(results_filepath)

        # PE data
        pe_result = bilby.core.result.read_in_result(filename=results_filepath)
        self.log_bayes_factor = pe_result.log_bayes_factor
        self.log_evidence = pe_result.log_evidence
        self.log_noise_evidence = pe_result.log_noise_evidence

        # injection data
        self.truths = flatten_dict(pe_result.injection_parameters)
        self.snr = self._get_snr(pe_result.meta_data)

    @staticmethod
    def _get_snr(meta_data: dict) -> float:
        interferometer_data = meta_data.get(rkeys.LIKELIHOOD).get(ikeys.INTERFEROMETERS)
        snr_vals = np.array(
            [
                interferometer_data.get(interferometer_id).get(rkeys.MATCHED_FILTER_SNR)
                for interferometer_id in ikeys.INTERFEROMETER_LIST
            ]
        )
        return math.sqrt(sum(abs(snr_vals) ** 2))

    @staticmethod
    def _get_injection_number(file_path: str) -> int:
        numbers_in_filepath = re.findall(
            re.compile(rkeys.INJECTION_NUM_REGEX), file_path
        )
        if numbers_in_filepath:
            inj_num = int(numbers_in_filepath.pop())
        else:
            inj_num = -1
            print(
                f"WARNING: cant find inj number\n{file_path}, regexresult:{numbers_in_filepath}"
            )
        return inj_num

    @staticmethod
    def _get_q(data_dict):
        if data_dict.get(ikeys.MASS_RATIO):
            return data_dict.get(ikeys.MASS_RATIO)
        else:
            data_dict.get(ikeys.MASS_1) / data_dict.get(ikeys.MASS_2)

    def to_dict(self):
        result_summary_dict = {
            rkeys.INJECTION_NUMBER: self.inj_num,
            rkeys.SNR: self.snr,
            rkeys.LOG_BF: self.log_bayes_factor,
            rkeys.LOG_EVIDENCE: self.log_evidence,
            rkeys.LOG_NOISE_EVIDENCE: self.log_noise_evidence,
            rkeys.PATH: self.path,
        }
        result_summary_dict.update(self.truths)  # this unwraps the injected parameters
        return result_summary_dict


def get_results_summary_dataframe(root_path: str):
    # load results
    result_files = get_filepaths(root_path, file_regex=rkeys.RESULT_FILE_REGEX)
    results_list = [ResultSummary(f).to_dict() for f in result_files]
    results_dict = list_dicts_to_dict_lists(results_list)

    # saving data into a dataframe
    results_df = pd.DataFrame(results_dict)
    results_df.sort_values(by=[rkeys.LOG_BF], na_position="first", inplace=True)
    results_df.dropna(inplace=True)
    results_df.to_csv(os.path.join(root_path, "result_summary.csv"))
    return results_df


def plot_results_page(results_dir: str, df: pd.DataFrame):
    import plotly.graph_objs as go
    import plotly as py

    df = add_url_from_path_to_dataframe(df)

    df_keys = [
        rkeys.URL,
        ikeys.MASS_RATIO,
        rkeys.SNR,
        rkeys.LOG_BF,
        ikeys.LUMINOSITY_DISTANCE,
        ikeys.REDSHIFT,
    ]

    # Data summary table
    headers = ["i#", "q", "SNR", "LnBF", "Dl", "z"]
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

    # mass scatter plot
    mass_scat = go.Scatter(
        x=df[ikeys.MASS_1],
        y=df[ikeys.MASS_2],
        text=[
            "Inj{}: {:.2f},{:.2f}".format(
                df[rkeys.INJECTION_NUMBER],
                df[ikeys.MASS_1].values[i],
                df[ikeys.MASS_2].values[i],
            )
            for i in range(len(df))
        ],
        mode="markers",
        xaxis="x1",
        yaxis="y1",
        hoverinfo="text",
        name="mass",
    )

    # mass ratio histogram
    hist_q = go.Histogram(
        x=df[ikeys.MASS_RATIO], xaxis="x2", yaxis="y2", opacity=0.75, name="q count"
    )

    # log bayes factor ratio histogram
    hist_lbf = go.Histogram(
        x=df[rkeys.LOG_BF], xaxis="x4", yaxis="y4", opacity=0.75, name="LnBF count"
    )

    # SNR histogram
    hist_snr = go.Histogram(
        x=df[rkeys.SNR], xaxis="x3", yaxis="y3", opacity=0.75, name="snr count"
    )

    # Data presentation
    axis = dict(
        showline=True,
        zeroline=False,
        showgrid=True,
        mirror=True,
        ticklen=4,
        gridcolor="#ffffff",
        tickfont=dict(size=10),
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

    # final plotting command
    save_dir = os.path.join(results_dir, "result_summary.html")
    py.offline.plot(plotting_dict, filename=save_dir, auto_open=False)
    print("File saved at : " + save_dir)


def add_url_from_path_to_dataframe(df: pd.DataFrame):
    base_path = "/home/avi.vajpeyi/public_html/"
    url = '<a href="https://ldas-jobs.ligo.caltech.edu/~avi.vajpeyi/{}">{}</a>'
    df[rkeys.URL] = df[rkeys.PATH].split(base_path)[-1]
    df[rkeys.URL] = url.format(df[rkeys.URL], df[rkeys.INJECTION_NUMBER])
    return df
