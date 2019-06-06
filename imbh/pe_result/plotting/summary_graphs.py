import os

import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import pandas as pd
from pe_result.plotting.latex_label import LATEX_LABEL_DICT
from plotly import graph_objs as go, tools
from plotly.offline import plot


def plot_mass_data(df: pd.DataFrame, filename="mass_distibution.html", title=None):

    # unpack labels
    m2_label = LATEX_LABEL_DICT[ikeys.MASS_2]
    m1_label = LATEX_LABEL_DICT[ikeys.MASS_1]
    q_label = LATEX_LABEL_DICT[ikeys.MASS_RATIO]
    subplot_mass_scat_title = "$M_2 \\text{ vs } M_1$"
    subplot_q_hist = "$q \\text{ Histogram}$"

    # make figure
    fig = tools.make_subplots(
        rows=1, cols=2, subplot_titles=(subplot_q_hist, subplot_mass_scat_title)
    )
    fig["layout"].update(title=title, showlegend=False)

    # ADD Q HISTOGRAM
    fig["layout"]["xaxis1"].update(title=q_label)
    fig["layout"]["yaxis1"].update(title="Density")
    hist_q_trace = go.Histogram(
        x=df[ikeys.MASS_RATIO], opacity=0.75, name="q count", histnorm="probability"
    )
    fig.append_trace(hist_q_trace, 1, 1)

    # ADD MASS SCATTER PLOT
    fig["layout"]["xaxis2"].update(title=m2_label)
    fig["layout"]["yaxis2"].update(title=m1_label)
    colorbar = q_label
    mass_scat_trace = go.Scatter(
        x=df[ikeys.MASS_2],
        y=df[ikeys.MASS_1],
        text=[
            "Inj {}: {:.2f},{:.2f}".format(
                df[rkeys.INJECTION_NUMBER].values[i],
                df[ikeys.MASS_2].values[i],
                df[ikeys.MASS_1].values[i],
            )
            for i in range(len(df))
        ],
        mode="markers",
        marker=dict(
            color=df[ikeys.MASS_RATIO],  # set color equal to a variable
            colorscale="Blues",
            showscale=True,
            colorbar=dict(title=colorbar),
        ),
        hoverinfo="text",
        name=subplot_mass_scat_title,
    )
    fig.append_trace(mass_scat_trace, 1, 2)

    graph_url = plot(fig, filename=filename, auto_open=False, include_mathjax="cdn")

    return os.path.basename(graph_url)


def plot_analysis_statistics_data(
    df: pd.DataFrame, filename="analysis_statistics.html", title=None
):
    # unpack labels
    snr_label = LATEX_LABEL_DICT[rkeys.SNR]
    lnbf_label = LATEX_LABEL_DICT[rkeys.LOG_BF]
    subplot_hist_snr = "$SNR \\text{ Histogram}$"
    subplot_hist_logbf = "$\\log \\text{BF} \\text{ Histogram}$"

    # make figure
    fig = tools.make_subplots(
        rows=1, cols=2, subplot_titles=(subplot_hist_snr, subplot_hist_logbf)
    )
    fig["layout"].update(title=title, showlegend=False)

    # SNR histogram
    hist_snr_trace = go.Histogram(
        x=df[rkeys.SNR],
        xaxis="x3",
        yaxis="y3",
        opacity=0.75,
        name="snr count",
        histnorm="probability",
    )
    fig.append_trace(hist_snr_trace, 1, 1)
    fig["layout"]["xaxis1"].update(title=snr_label)
    fig["layout"]["yaxis1"].update(title="Density")

    # log bayes factor ratio histogram
    hist_lbf_trace = go.Histogram(
        x=df[rkeys.LOG_BF],
        xaxis="x3",
        yaxis="y3",
        opacity=0.75,
        name="LnBF count",
        histnorm="probability",
    )
    fig.append_trace(hist_lbf_trace, 1, 2)
    fig["layout"]["xaxis2"].update(title=lnbf_label)
    # fig["layout"]["yaxis2"].update(title="Density")

    graph_url = plot(fig, filename=filename, auto_open=False, include_mathjax="cdn")

    return os.path.basename(graph_url)
