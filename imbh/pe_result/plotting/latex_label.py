import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys

# ikeys
LATEX_LABEL_DICT = {
    ikeys.MASS_1: "$M_1$",
    ikeys.MASS_2: "$M_2$",
    ikeys.CHIRP_MASS: "$M$",
    ikeys.MASS_RATIO: "$q$",
    ikeys.DEC: "$\\mathrm{DEC}$",
    ikeys.RA: "$\\mathrm{RA}$",
    ikeys.THETA_JN: "$\\theta_{JN}$",
    ikeys.PSI: "$\\psi$",
    ikeys.PHASE: "$\\phi$",
    ikeys.A_1: "$a_1$",
    ikeys.A_2: "$a_2$",
    ikeys.TILT_1: "$\\theta_1$",
    ikeys.TILT_2: "$\\theta_2$",
    ikeys.PHI_12: "$\\Delta\\phi$",
    ikeys.PHI_JL: "$\\phi_{JL}$",
}


# rkeys
LATEX_LABEL_DICT.update(
    {
        rkeys.INJECTION_NUMBER: "InjNum",
        rkeys.LOG_BF: "$\\log \\text{BF}$",
        rkeys.SNR: "SNR",
        rkeys.URL: "Inj #",
    }
)
