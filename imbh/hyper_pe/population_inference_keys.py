from injection_parameter_generator import injection_keys as ikeys

MASS_KEYS = [ikeys.MASS_RATIO, ikeys.CHIRP_MASS]

# keys
Q_MU = "q_mu"
Q_SIGMA = "q_sigma"
Q_MIN = "q_min"
Q_MAX = "q_max"

MCHIRP_MU = "mchirp_mu"
MCHIRP_SIGMA = "mchirp_sigma"
MCHIRP_MIN = "mchirp_min"
MCHIRP_MAX = "mchirp_max"

LATEX_LABELS = dict(
    Q_MU="$q_{\\mu}$",
    Q_SIGMA="$q_{\\sigma}$",
    Q_MIN="$q_{{min}}$",
    Q_MAX="$q_{{max}}$",
    MCHIRP_MU="$\\mathcal{M}_{\\mu}$",
    MCHIRP_SIGMA="\\mathcal{M}_{\\sigma}",
    MCHIRP_MIN="$\\mathcal{M}_{{min}}$",
    MCHIRP_MAX="$\\mathcal{M}_{{max}}$",
)
