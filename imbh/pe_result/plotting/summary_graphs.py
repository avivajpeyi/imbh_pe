import os

import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from pe_result.plotting.latex_label import LATEX_LABEL_DICT
from plotly import graph_objs as go, tools
from plotly.offline import plot

matplotlib.use("Agg")


def plot_mass_scatter(df: pd.DataFrame, filename="mass_scatter.html", title=None):
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
            colorbar=dict(title="q"),
        ),
        hoverinfo="text",
        name="$M_2 \\text{ vs } M_1$",
    )

    # Edit the layout
    layout = dict(
        title=title,
        xaxis=dict(title=LATEX_LABEL_DICT[ikeys.MASS_1]),
        yaxis=dict(title=LATEX_LABEL_DICT[ikeys.MASS_2]),
        showlegend=False,
    )
    fig = dict(data=[mass_scat_trace], layout=layout)
    graph_url = plot(fig, filename=filename, auto_open=False, include_mathjax="cdn")
    return os.path.basename(graph_url)


def plot_mass_distribution(df: pd.DataFrame, filename="mass_scatter.html", title=None):
    num_bins = 20
    f, (ax2, ax3) = plt.subplots(1, 2)
    histogram_data(df[ikeys.MASS_RATIO], num_bins, label="$\\pi(q)$", ax=ax2)
    histogram_data(df[ikeys.CHIRP_MASS], num_bins, label="$\\pi(M_c)$", ax=ax3)
    f.tight_layout()
    plotly_fig = tools.mpl_to_plotly(f)

    # formatting fixes
    for trace in plotly_fig["data"]:
        if trace.name == "_line0":
            trace.name = "Best Fit"
        else:
            trace.name = "PDF"
            trace["marker"].update(line=None, opacity=0.75)

    graph_url = plot(
        plotly_fig, filename=filename, auto_open=False, include_mathjax="cdn"
    )
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


def histogram_data(x: list, num_bins, label, ax):
    # plot the histogram of the data (and get bins)
    _, bins, _ = ax.hist(x, num_bins, density=1)

    # add a 'best fit' line
    mu, sigma = stats.norm.fit(x)
    y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(
        -0.5 * (1 / sigma * (bins - mu)) ** 2
    )
    ax.plot(bins, y)

    ax.set_xlabel(label)
    ax.set_ylabel("Probability density")
    ax.set_title("$\\mu={:.2f}, \\sigma={:.2f}$".format(mu, sigma))
