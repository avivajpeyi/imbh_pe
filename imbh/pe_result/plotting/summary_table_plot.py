import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import pandas as pd
import plotly.graph_objs as go
from numpy import np
from pe_result.plotting import colors
from pe_result.plotting.latex_label import LATEX_LABEL_DICT
from plotly.offline import plot


def plot_data_table(df: pd.DataFrame, filename="summary_table.html", title=None) -> str:
    """
    :return:
        string url relative-path of the plot.
    """

    df[rkeys.URL] = get_url_from_path(
        df[rkeys.PATH].values, df[rkeys.INJECTION_NUMBER].values
    )

    # columns to include in table
    df_keys = [
        rkeys.URL,
        rkeys.LOG_BF,
        rkeys.SNR,
        ikeys.MASS_RATIO,
        ikeys.LUMINOSITY_DISTANCE,
        ikeys.REDSHIFT,
    ]

    num_col = len(df_keys)
    headers = [LATEX_LABEL_DICT[k] for k in df_keys]

    # Data summary table formatting
    table_trace = go.Table(
        columnwidth=[5] + [10] * (num_col - 1),
        header=dict(
            values=headers,
            align=["left"] * num_col,
            font=dict(size=14, color=[colors.BLACK] * num_col),
            fill=dict(color=colors.DARK_BLUE),
        ),
        cells=dict(
            values=[df[k] for k in df_keys],
            align=["left"] * num_col,
            font=dict(size=12, color=[colors.GRAY] * num_col),
            format=[None] + [".2f"] * (num_col - 1),
            fill=dict(color=[colors.BLUE, colors.LIGHT_BLUE]),
        ),
    )
    layout = dict(autosize=True, title=title, margin=dict(t=100), showlegend=False)
    table_url = plot(
        data=[table_trace],
        layout=layout,
        filename=filename,
        auto_open=False,
        include_mathjax="cdn",
    )
    return table_url


@np.vectorize
def get_url_from_path(paths, injection_numbers):
    base_path = "/home/avi.vajpeyi/public_html/"
    url_template = '<a href="https://ldas-jobs.ligo.caltech.edu/~avi.vajpeyi/{}">{}</a>'
    url = paths.split(base_path)[-1].replace("result.json", "corner.png")
    url = url_template.format(url, injection_numbers)
    return url
