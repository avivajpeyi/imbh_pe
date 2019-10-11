import logging
import math
import os
import re

import bilby
import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import numpy as np
import pandas as pd
import pe_result.regex as regex
from tools import file_utils
from tools.utils import flatten_dict, list_dicts_to_dict_lists

NUMBER_OF_POSTERIOR_SAMPLES = 500


class ResultSummary(object):
    def __init__(self, results_filepath: str):
        self.path = results_filepath
        self.inj_num = self._get_injection_number(results_filepath)

        # PE data
        pe_result = bilby.core.result.read_in_result(filename=results_filepath)
        self.log_bayes_factor = pe_result.log_bayes_factor
        self.log_evidence = pe_result.log_evidence
        self.log_noise_evidence = pe_result.log_noise_evidence
        self.log_gh_evidence = self._get_detector_log_evidence(
            detector_string="H1", filepath=results_filepath
        )
        self.log_gl_evidence = self._get_detector_log_evidence(
            detector_string="L1", filepath=results_filepath
        )

        self.posterior = pe_result.posterior

        # Injection data
        try:
            self.truths = flatten_dict(pe_result.injection_parameters)
            self.truths = self.__set_mass1_mass2_from_mchirp_q(self.truths)
            self.snr = self._get_snr(pe_result.meta_data)
        except Exception:
            self.truths = None
            self.snr = None

    @property
    def posterior(self):
        return self.__posterior

    @posterior.setter
    def posterior(self, df):
        """
        Downsample the posterior samples
        :param df:
        :return:
        """
        if len(df) >= NUMBER_OF_POSTERIOR_SAMPLES:
            self.__posterior = df.sample(n=NUMBER_OF_POSTERIOR_SAMPLES)
        else:
            self.__posterior = df

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
        numbers_in_filepath = re.findall(re.compile(regex.INJECTION_NUM), file_path)
        if numbers_in_filepath:
            inj_num = int(numbers_in_filepath.pop())
        else:
            inj_num = -1
            logging.warning(
                f"Cant find inj number\n{file_path}, regexresult:{numbers_in_filepath}"
            )
        return inj_num

    @staticmethod
    def get_q(data_dict):
        if data_dict.get(ikeys.MASS_RATIO):
            return data_dict.get(ikeys.MASS_RATIO)
        else:
            data_dict.get(ikeys.MASS_1) / data_dict.get(ikeys.MASS_2)

    @staticmethod
    def __set_mass1_mass2_from_mchirp_q(param: dict):
        if {ikeys.MASS_1, ikeys.MASS_2}.issubset(set(param)):
            q = param[ikeys.MASS_RATIO]
            mchirp = param[ikeys.CHIRP_MASS]
            param[ikeys.MASS_1] = (
                (q ** (2.0 / 5.0)) * ((1.0 + q) ** (1.0 / 5.0)) * mchirp
            )
            param[ikeys.MASS_2] = (
                (q ** (-3.0 / 5.0)) * ((1.0 + q) ** (1.0 / 5.0)) * mchirp
            )
        return param

    @staticmethod
    def _get_detector_log_evidence(detector_string, filepath):
        log_evidence = 0
        dir_name = os.path.dirname(filepath)
        base_name = os.path.basename(filepath)
        base_name = base_name.replace("_H1L1_", "_{}_".format(detector_string), 1)
        result_filename = os.path.join(dir_name, base_name)
        try:
            result = bilby.core.result.read_in_result(filename=result_filename)
            log_evidence = result.log_evidence
        except OSError:
            logging.warning(f"{result_filename} not found")
        return log_evidence

    def to_dict(self):
        result_summary_dict = {
            rkeys.INJECTION_NUMBER: self.inj_num,
            rkeys.SNR: self.snr,
            rkeys.LOG_BF: self.log_bayes_factor,
            rkeys.LOG_EVIDENCE: self.log_evidence,
            rkeys.LOG_NOISE_EVIDENCE: self.log_noise_evidence,
            rkeys.LOG_GLITCH_H_EVIDENCE: self.log_gh_evidence,
            rkeys.LOG_GLITCH_L_EVIDENCE: self.log_gl_evidence,
            rkeys.PATH: self.path,
            rkeys.POSTERIOR: self.posterior,
        }
        if self.snr:
            result_summary_dict.update({rkeys.SNR: self.snr})
        if self.truths:
            result_summary_dict.update(self.truths)  # unwraps injected parameters
        return result_summary_dict


def get_results_summary_dataframe(root_path: str):
    # load ALL results
    result_files = file_utils.get_filepaths(root_path, file_regex=regex.RESULT_FILE)

    assert len(result_files) != 0

    h1l1_result_files = file_utils.filter_list(
        result_files, filter_regex=regex.H1L1_RESULT_FILE
    )

    result_summary_list = []
    for f in h1l1_result_files:
        try:
            result_summary_list.append(ResultSummary(f).to_dict())
        except ValueError as e:
            logging.warning(f"Result file {f} Error: {e}. Skipping file.")
            # os.remove(f)
    results_dict = list_dicts_to_dict_lists(result_summary_list)

    # saving data into a dataframe
    results_df = pd.DataFrame(results_dict)
    results_df.sort_values(by=[rkeys.LOG_BF], na_position="first", inplace=True)
    results_df.dropna(inplace=True)
    # results_df.to_csv(os.path.join(root_path, "result_summary.csv"))
    return results_df
