import math
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
        self.posterior = pe_result.posterior

        # Injection data
        self.truths = flatten_dict(pe_result.injection_parameters)
        self.truths = self.__set_mass1_mass2_from_mchirp_q(self.truths)
        self.snr = self._get_snr(pe_result.meta_data)

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

    def to_dict(self):
        result_summary_dict = {
            rkeys.INJECTION_NUMBER: self.inj_num,
            rkeys.SNR: self.snr,
            rkeys.LOG_BF: self.log_bayes_factor,
            rkeys.LOG_EVIDENCE: self.log_evidence,
            rkeys.LOG_NOISE_EVIDENCE: self.log_noise_evidence,
            rkeys.PATH: self.path,
            rkeys.POSTERIOR: self.posterior,
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
    # results_df.to_csv(os.path.join(root_path, "result_summary.csv"))
    return results_df
