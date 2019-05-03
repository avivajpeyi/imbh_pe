#!/usr/bin/env python3
import os
from typing import List

import matplotlib

matplotlib.use("PS")

MASS_PLOT_FNAME = "m1_m2.png"


def plot_mass_distribution(mass1: List, mass2: List, out_dir: str):
    import matplotlib.pyplot as plt

    plt.hist2d(mass1, mass2, bins=100, cmap="Blues")
    plt.xlabel("$m_1$")
    plt.ylabel("$m_2$")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, MASS_PLOT_FNAME))
