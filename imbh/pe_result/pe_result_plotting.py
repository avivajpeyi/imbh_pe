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


def plot_results_page_old(results_dir: str, df: pd.DataFrame):
    table_url = ""

    # mass scatter plot
    mass_scat = go.Scatter(
        x=df[ikeys.MASS_1],
        y=df[ikeys.MASS_2],
        text=[
            "Inj{}: {:.2f},{:.2f}".format(
                df[rkeys.INJECTION_NUMBER].values[i],
                df[ikeys.MASS_1].values[i],
                df[ikeys.MASS_2].values[i],
            )
            for i in range(len(df))
        ],
        mode="markers",
        marker=dict(
            color=df[ikeys.MASS_RATIO],  # set color equal to a variable
            colorscale="Ice",
            showscale=True,
        ),
        xaxis="x1",
        yaxis="y1",
        hoverinfo="text",
        name="mass",
    )

    # mass ratio histogram
    hist_q = go.Histogram(
        x=df[ikeys.MASS_RATIO],
        xaxis="x2",
        yaxis="y2",
        opacity=0.75,
        name="q count",
        histnorm="probability",
    )

    # log bayes factor ratio histogram
    hist_lbf = go.Histogram(
        x=df[rkeys.LOG_BF],
        xaxis="x3",
        yaxis="y3",
        opacity=0.75,
        name="LnBF count",
        histnorm="probability",
    )

    # SNR histogram
    hist_snr = go.Histogram(
        x=df[rkeys.SNR],
        xaxis="x3",
        yaxis="y3",
        opacity=0.75,
        name="snr count",
        histnorm="probability",
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
    logger.info("File saved at : " + save_dir)
