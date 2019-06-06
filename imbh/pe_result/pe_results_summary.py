import math
import os
import re

import bilby
import imbh_pe_calculator.results_keys as rkeys
import injection_parameter_generator.injection_keys as ikeys
import numpy as np
import pandas as pd
from bilby.core.utils import logger
from tools.file_utils import get_filepaths
from tools.utils import flatten_dict, list_dicts_to_dict_lists

bilby.utils.setup_logger(log_level="info")


class ResultSummary(object):
    def __init__(self, results_filepath: str):
        self.path = results_filepath
        self.inj_num = self._get_injection_number(results_filepath)

        # PE data
        pe_result = bilby.core.result.read_in_result(filename=results_filepath)
        self.log_bayes_factor = pe_result.log_bayes_factor
        self.log_evidence = pe_result.log_evidence
        self.log_noise_evidence = pe_result.log_noise_evidence

        # Injection data
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
            logger.warn(
                f"Cant find inj number\n{file_path}, regexresult:{numbers_in_filepath}"
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
    result_summary_list = [ResultSummary(f).to_dict() for f in result_files]
    results_dict = list_dicts_to_dict_lists(result_summary_list)

    # saving data into a dataframe
    results_df = pd.DataFrame(results_dict)
    results_df.sort_values(by=[rkeys.LOG_BF], na_position="first", inplace=True)
    results_df.dropna(inplace=True)
    results_df.to_csv(os.path.join(root_path, "result_summary.csv"))
    return results_df
