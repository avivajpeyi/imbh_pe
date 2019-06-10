import os

import bilby
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import scipy.stats as stats
from imbh_pe_calculator import results_keys as rkeys
from injection_parameter_generator import injection_keys as ikeys
from pe_result.plotting.latex_label import LATEX_LABEL_DICT
from plotly import graph_objs as go
from plotly.offline import plot
from tools.file_utils import get_filepaths

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


def plot_mass_distribution(df: pd.DataFrame, filename="mass_scatter", title=None):
    num_bins = 20
    f, (ax1, ax2) = plt.subplots(1, 2)
    histogram_data(df[ikeys.MASS_RATIO], num_bins, label="$\\pi(q)$", ax=ax1)
    histogram_data(df[ikeys.CHIRP_MASS], num_bins, label="$\\pi(M_c)$", ax=ax2)
    f.tight_layout()

    try:
        plotly_fig = plotly.tools.mpl_to_plotly(f)
        plotly_fig["layout"]["bargap"] = 0
        # formatting fixes
        for trace in plotly_fig["data"]:
            if trace.name == "_line0":
                trace.name = "Best Fit"
            else:
                trace.name = "PDF"
                trace["marker"].update(line=None, opacity=0.75)

        graph_url = plot(
            plotly_fig,
            filename=filename + ".html",
            auto_open=False,
            include_mathjax="cdn",
        )
    except ValueError:
        graph_url = filename + ".png"
        plt.savefig(filename)
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
    fig = plotly.tools.make_subplots(
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


def plot_pp_test(results_dir: str, keys=None):
    """

    :param results_dir:
    :param keys: A list of keys to use, if None defaults to search_parameter_keys
    :return:
    """
    filename = os.path.join(results_dir, "pp")
    result_files = get_filepaths(results_dir, file_regex=rkeys.RESULT_FILE_REGEX)
    results = [bilby.core.result.read_in_result(f) for f in result_files]
    fig, pvals = bilby.core.result.make_pp_plot(results, save=False)
    try:
        # Layout formatting
        plotly_fig = plotly.tools.mpl_to_plotly(fig)
        plotly_fig["layout"]["annotations"] = None
        plotly_fig["layout"]["showlegend"] = True
        plotly_fig["layout"]["xaxis"]["title"] = "Credible Level"
        plotly_fig["layout"]["yaxis"]["title"] = "Fraction of Data"
        plotly_fig["layout"]["title"] = f"Combined p-value: {pvals.combined_pvalue:.3f}"

        # plotting confidence area
        confidence_interval = 0.9
        x_values = np.linspace(0, 1, 1001)
        num_pp = len(plotly_fig["data"])
        edge_of_bound = (1.0 - confidence_interval) / 2.0
        lower = stats.binom.ppf(1 - edge_of_bound, num_pp, x_values) / num_pp
        upper = stats.binom.ppf(edge_of_bound, num_pp, x_values) / num_pp
        # The binomial point percent function doesn't always return 0 @ 0,
        # so set those bounds explicitly to be sure
        lower[0] = 0
        upper[0] = 0

        trace_upper = go.Scatter(
            x=x_values,
            y=upper,
            fill=None,
            opacity=0.2,
            hoverinfo="none",
            mode="lines",
            showlegend=False,
            line=dict(color="rgb(211,211,211)"),
        )
        trace_lower = go.Scatter(
            x=x_values,
            y=lower,
            fill="tonexty",
            opacity=0.2,
            hoverinfo="none",
            mode="lines",
            showlegend=False,
            line=dict(color="rgb(211,211,211)"),
        )

        graph_url = plot(
            dict(
                data=[trace_upper, trace_lower] + list(plotly_fig["data"]),
                layout=plotly_fig["layout"],
            ),
            filename=filename + ".html",
            auto_open=False,
            include_mathjax="cdn",
        )

    except ValueError as e:

        print(f"ERROR {e}")
        graph_url = filename + ".png"
        fig.savefig(graph_url, dpi=500)

    return os.path.basename(graph_url)
